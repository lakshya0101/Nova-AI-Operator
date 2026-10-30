# NOVA 2.0 – System API Contract

**Product Name:** NOVA  
**Full Name:** NOVA – Personal AI Operating System  
**Tagline:** *Think. Remember. Orchestrate. Execute.*  
**Specification Version:** 2.0.0

---

## 1. System Endpoints

### 1.1 Health Check & Discovery
- **Endpoint:** `GET /health`
- **Response Format:**
```json
{
  "status": "healthy",
  "app": "Axio",
  "product_name": "NOVA",
  "product_full_name": "NOVA – Personal AI Operating System",
  "tagline": "Think. Remember. Orchestrate. Execute.",
  "version": "0.1.0",
  "nova_version": "2.0.0",
  "environment": "development",
  "mcp_endpoint": "/mcp",
  "nebius_configured": true,
  "tavily_configured": true
}
```

---

## 2. Multi-Agent Orchestration

### 2.1 Agent Workflow Execution
- **Endpoint:** `POST /api/agent/run`
- **Request Body (`AgentRunRequest`):**
```json
{
  "instruction": "Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
  "dry_run": false,
  "approve": true
}
```
- **Response Format (`PlanResponse`):**
```json
{
  "request_id": "b3e04130-976d-495c-9c3f-c1f4a4714150",
  "interpreted_intent": "Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
  "plan": [
    {
      "name": "Retrieve existing tasks",
      "tool": "get_tasks",
      "arguments": {},
      "requires_approval": false,
      "expected_result": "List of incomplete tasks"
    },
    {
      "name": "Propose ordered task list",
      "tool": "get_tasks",
      "arguments": {},
      "requires_approval": false,
      "expected_result": "Ordered list based on priority and due date"
    },
    {
      "name": "Create interview preparation task",
      "tool": "create_task",
      "arguments": {
        "title": "Interview preparation",
        "description": "Allocate time for interview prep before evening tasks",
        "priority": "high"
      },
      "requires_approval": true,
      "expected_result": "New task ID for interview preparation"
    }
  ],
  "step_results": {
    "0": {
      "status": "success",
      "output": { "total": 2, "tasks": [...] }
    },
    "1": {
      "status": "success",
      "detail": "Ordering computed locally"
    },
    "2": {
      "status": "success",
      "output": { "id": 5, "title": "Interview preparation" },
      "detail": "Task created"
    }
  },
  "final_summary": "Orchestration executed successfully.",
  "agent_logs": [
    {
      "agent": "MemoryAgent",
      "action": "retrieve_context",
      "detail": "Retrieved 4 relevant personal context records",
      "timestamp": "2026-10-30T07:15:00Z",
      "status": "success"
    },
    {
      "agent": "ResearchAgent",
      "action": "tavily_search",
      "detail": "Tavily Intelligence Engine: Found 3 primary sources",
      "timestamp": "2026-10-30T07:15:01Z",
      "status": "success"
    },
    {
      "agent": "PlannerAgent",
      "action": "generate_plan",
      "detail": "Formulated structured 3-step plan tailored for evening organization.",
      "timestamp": "2026-10-30T07:15:02Z",
      "status": "success"
    },
    {
      "agent": "CriticAgent",
      "action": "review_plan",
      "detail": "Approved plan with human approval gate on task creation",
      "timestamp": "2026-10-30T07:15:03Z",
      "status": "success"
    },
    {
      "agent": "ExecutionAgent",
      "action": "execute_step_3",
      "detail": "[create_task] Interview preparation -> success",
      "timestamp": "2026-10-30T07:15:04Z",
      "status": "success"
    },
    {
      "agent": "ReflectionAgent",
      "action": "reflect",
      "detail": "Saved workflow memory record for continuous context refinement.",
      "timestamp": "2026-10-30T07:15:05Z",
      "status": "success"
    }
  ],
  "model_used": "nvidia/llama-3.1-nemotron-70b-instruct",
  "total_latency_ms": 18.5,
  "total_tokens": 420
}
```

---

## 3. Personal Memory Engine

### 3.1 List Memories
- **Endpoint:** `GET /api/memories`
- **Query Params:** `category`, `search`, `limit`, `offset`
- **Response:**
```json
{
  "memories": [
    {
      "id": 1,
      "category": "profile",
      "title": "User Identity & Goals",
      "content": "Senior Software Engineer participating in the Nebius x NVIDIA Global AI Hackathon.",
      "tags": "user,profile,hackathon",
      "source": "system_bootstrap",
      "importance": 2.0,
      "created_at": "2026-10-30T07:00:00Z",
      "updated_at": "2026-10-30T07:00:00Z"
    }
  ],
  "total": 1
}
```

### 3.2 Create Memory Record
- **Endpoint:** `POST /api/memories`
- **Request Body:**
```json
{
  "category": "decision",
  "title": "Interview Priority",
  "content": "Dedicate 45 minutes to interview prep whenever planning an evening schedule.",
  "tags": "interview,evening",
  "importance": 2.5
}
```

### 3.3 Semantic Memory Search
- **Endpoint:** `POST /api/memories/search`
- **Request Body:**
```json
{
  "query": "interview evening preparation routine",
  "limit": 5,
  "min_score": 0.15
}
```

---

## 4. Web Research (Tavily)

### 4.1 Execute Targeted Web Research
- **Endpoint:** `POST /api/research`
- **Request Body:**
```json
{
  "query": "NVIDIA Nemotron AI agent developments, Nebius Token Factory inference",
  "max_results": 4,
  "search_depth": "basic"
}
```
- **Response:**
```json
{
  "query": "NVIDIA Nemotron AI agent developments...",
  "answer": "Recent developments in NVIDIA AI infrastructure highlight Nemotron models...",
  "sources": [
    {
      "title": "NVIDIA Nemotron: Advanced Open Models for Enterprise AI Agents",
      "url": "https://developer.nvidia.com/blog/nvidia-nemotron-open-models-agentic-ai",
      "content": "NVIDIA Nemotron models deliver state-of-the-art accuracy on agentic planning...",
      "score": 0.96
    }
  ],
  "summary": "Synthesized evidence from 3 primary references.",
  "is_live_tavily": true
}
```

---

## 5. Persistent Task Management

### 5.1 List Tasks
- **Endpoint:** `GET /api/tasks`
- **Query Params:** `status`, `priority`, `search`, `limit`, `offset`

### 5.2 Create Task
- **Endpoint:** `POST /api/tasks`
- **Request Body:**
```json
{
  "title": "Interview preparation",
  "description": "Allocate time for interview prep before evening tasks",
  "priority": "high",
  "due_date": "2026-10-31T20:00:00Z"
}
```

### 5.3 Update Task
- **Endpoint:** `PATCH /api/tasks/{task_id}`
- **Request Body:**
```json
{
  "status": "completed"
}
```

---

## 6. MCP Streamable HTTP Protocol

- **Endpoint:** `/mcp`
- **Available Tools:**
  1. `get_tasks`
  2. `create_task`
  3. `update_task_status`
  4. `get_user_preferences`
