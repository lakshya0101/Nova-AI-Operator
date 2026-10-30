"""NOVA FastAPI Application entrypoint with integrated MCP Streamable HTTP server."""

import logging
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings

from .config import get_settings
from .database import get_db, init_db, SessionLocal
from .models.task import TaskPriority, TaskStatus
from .models.memory import MemoryCategory
from .schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskRead,
    TaskListResponse,
)
from .schemas.preference import (
    UserPreferenceRead,
    UserPreferenceSet,
    UserPreferencesResponse,
)
from .schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryRead,
    MemoryQuery,
    MemoryListResponse,
)
from .schemas.research import (
    ResearchRequest,
    ResearchResponse,
)
from .services import task_service, preference_service, memory_service
from .services.tavily_service import execute_tavily_research
from .tools.mcp_server import mcp_server
from .schemas.orchestration import AgentRunRequest, PlanResponse
from .services.orchestration_service import run_orchestration

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("nova.api")


class DynamicMCPASGIApp:
    """ASGI application adapter allowing safe dynamic session manager recreation across lifespans."""

    def __init__(self, server):
        self.server = server
        self.session_manager: Optional[StreamableHTTPSessionManager] = None

    async def __call__(self, scope, receive, send):
        if self.session_manager is None:
            raise RuntimeError("MCP Streamable HTTP session manager is not active.")
        await self.session_manager.asgi_app(scope, receive, send)


mcp_dynamic_app = DynamicMCPASGIApp(mcp_server)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: initialize persistence and run MCP session manager."""
    logger.info("Initializing NOVA persistence and database schema...")
    init_db()

    # Seed default preferences and memory
    with SessionLocal() as db:
        preference_service.seed_default_preferences(db)
        memory_service.seed_default_memories(db)

    security_settings = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"],
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"],
    )

    session_manager = StreamableHTTPSessionManager(
        app=mcp_server._lowlevel_server,
        security_settings=security_settings,
    )
    mcp_dynamic_app.session_manager = session_manager

    logger.info("Starting MCP Streamable HTTP session manager...")
    async with session_manager.run():
        logger.info("NOVA application online and ready.")
        yield

    mcp_dynamic_app.session_manager = None
    logger.info("NOVA application and MCP session manager shut down.")


app = FastAPI(
    title=settings.product_full_name,
    description="NOVA – Personal AI Operating System. Think. Remember. Orchestrate. Execute.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP Streamable HTTP endpoint
app.mount("/mcp", mcp_dynamic_app)


# --- Health & Inspection Routes ---

@app.get("/health", tags=["System"])
def get_health() -> Dict[str, Any]:
    """Health check endpoint reporting system status and MCP discovery point."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "product_name": settings.product_name,
        "product_full_name": settings.product_full_name,
        "tagline": settings.tagline,
        "version": "0.1.0",
        "nova_version": "2.0.0",
        "environment": settings.environment,
        "mcp_endpoint": "/mcp",
        "nebius_configured": bool(settings.nebius_api_key),
        "tavily_configured": bool(settings.tavily_api_key),
    }


# --- Task Management Routes ---

@app.get(
    "/api/tasks",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="List tasks with filters",
)
def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by urgency"),
    search: Optional[str] = Query(None, description="Keyword search in title and description"),
    limit: int = Query(50, ge=1, le=100, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    """Retrieve persistent tasks filtered by status, priority, or search query."""
    tasks, total = task_service.list_tasks(
        db=db,
        status=status,
        priority=priority,
        search=search,
        limit=limit,
        offset=offset,
    )
    return TaskListResponse(
        tasks=[TaskRead.model_validate(t) for t in tasks],
        total=total,
        filters={
            "status": status.value if status else None,
            "priority": priority.value if priority else None,
            "search": search,
            "limit": limit,
            "offset": offset,
        },
    )


@app.post(
    "/api/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
):
    """Create a new action task in SQLite persistence."""
    task = task_service.create_task(db=db, task_in=task_in)
    logger.info("Created task id=%d: '%s'", task.id, task.title)
    return TaskRead.model_validate(task)


@app.get(
    "/api/tasks/{task_id}",
    response_model=TaskRead,
    tags=["Tasks"],
    summary="Get task details",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve details for a specific task."""
    task = task_service.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return TaskRead.model_validate(task)


@app.patch(
    "/api/tasks/{task_id}",
    response_model=TaskRead,
    tags=["Tasks"],
    summary="Update task",
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
):
    """Update status, title, description, priority, or due date of an existing task."""
    task = task_service.update_task(db=db, task_id=task_id, task_in=task_in)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    logger.info("Updated task id=%d: status=%s, priority=%s", task.id, task.status, task.priority)
    return TaskRead.model_validate(task)


@app.delete(
    "/api/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Delete a task from persistent storage."""
    deleted = task_service.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    logger.info("Deleted task id=%d", task_id)
    return None


# --- User & Operator Preferences Routes ---

@app.get(
    "/api/preferences",
    response_model=UserPreferencesResponse,
    tags=["Preferences"],
    summary="Get stored user preferences",
)
def get_preferences(
    category: Optional[str] = Query(None, description="Optional category filter"),
    db: Session = Depends(get_db),
):
    """Retrieve operator preferences and safety flags."""
    prefs = preference_service.get_preferences(db=db, category=category)
    return UserPreferencesResponse(preferences=prefs, category=category)


@app.put(
    "/api/preferences/{key}",
    response_model=UserPreferenceRead,
    tags=["Preferences"],
    summary="Update or set a preference",
)
def set_preference(
    key: str,
    pref_in: UserPreferenceSet,
    db: Session = Depends(get_db),
):
    """Create or update a configuration setting or user preference."""
    pref = preference_service.set_preference(
        db=db,
        key=key,
        value=pref_in.value,
        category=pref_in.category or "general",
        description=pref_in.description,
    )
    return UserPreferenceRead.model_validate(pref)


# --- Personal Memory Engine Routes ---

@app.get(
    "/api/memories",
    response_model=MemoryListResponse,
    tags=["Memory"],
    summary="List stored personal memories",
)
def list_memories(
    category: Optional[MemoryCategory] = Query(None, description="Filter by memory category"),
    search: Optional[str] = Query(None, description="Keyword search in memory title or content"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Retrieve persistent memories from the Personal Memory Engine."""
    items, total = memory_service.list_memories(
        db=db,
        category=category,
        search=search,
        limit=limit,
        offset=offset,
    )
    return MemoryListResponse(
        memories=[MemoryRead.model_validate(m) for m in items],
        total=total,
    )


@app.post(
    "/api/memories",
    response_model=MemoryRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Memory"],
    summary="Store a new memory record",
)
def create_memory(
    memory_in: MemoryCreate,
    db: Session = Depends(get_db),
):
    """Save structured memory context with semantic embedding."""
    item = memory_service.create_memory(db=db, memory_in=memory_in)
    return MemoryRead.model_validate(item)


@app.post(
    "/api/memories/search",
    response_model=List[MemoryRead],
    tags=["Memory"],
    summary="Semantic memory retrieval",
)
def search_memories(
    query_in: MemoryQuery,
    db: Session = Depends(get_db),
):
    """Perform cosine-similarity semantic search across stored memories."""
    return memory_service.search_memories(
        db=db,
        query=query_in.query,
        category=query_in.category,
        limit=query_in.limit,
        min_score=query_in.min_score,
    )


@app.get(
    "/api/memories/{memory_id}",
    response_model=MemoryRead,
    tags=["Memory"],
    summary="Get memory details",
)
def get_memory(
    memory_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve details for a specific memory record."""
    item = memory_service.get_memory(db=db, memory_id=memory_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory with ID {memory_id} not found",
        )
    return MemoryRead.model_validate(item)


@app.patch(
    "/api/memories/{memory_id}",
    response_model=MemoryRead,
    tags=["Memory"],
    summary="Update memory record",
)
def update_memory(
    memory_id: int,
    update_in: MemoryUpdate,
    db: Session = Depends(get_db),
):
    """Update title, content, or category of a memory record."""
    item = memory_service.update_memory(db=db, memory_id=memory_id, update_in=update_in)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory with ID {memory_id} not found",
        )
    return MemoryRead.model_validate(item)


@app.delete(
    "/api/memories/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Memory"],
    summary="Delete a memory record",
)
def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db),
):
    """Delete a memory record permanently."""
    deleted = memory_service.delete_memory(db=db, memory_id=memory_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory with ID {memory_id} not found",
        )
    return None


# --- Web Research Routes ---

@app.post(
    "/api/research",
    response_model=ResearchResponse,
    tags=["Research"],
    summary="Execute web research via Tavily",
)
async def conduct_research(request: ResearchRequest) -> ResearchResponse:
    """Execute live web research using Tavily API with source URL extraction."""
    return await execute_tavily_research(request)


# --- Orchestration Agent Route ---

@app.post(
    "/api/agent/run",
    response_model=PlanResponse,
    tags=["Agent"],
    summary="Run orchestration agent",
)
def run_agent(request: AgentRunRequest, db: Session = Depends(get_db)) -> PlanResponse:
    """Execute multi-agent orchestration based on natural language request.
    Coordinates Memory, Research, Planning, Critic, Execution, and Reflection.
    """
    try:
        return run_orchestration(request, db)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Orchestration execution failed: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.host, port=settings.port, reload=True)
