"""Base classes and structured state for NOVA Specialized Agent System."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

from ..core.nebius_client import NebiusClient, get_nebius_client
from ..schemas.memory import MemoryRead
from ..schemas.research import ResearchResponse
from ..schemas.orchestration import PlanStep, ExecutionResult


class AgentLogEntry(BaseModel):
    agent: str
    action: str
    detail: str
    timestamp: str
    status: str = "success"  # success, warning, failed, waiting_approval


class AgentState(BaseModel):
    """Unified validated state passed across the NOVA multi-agent orchestration pipeline."""

    session_id: str
    instruction: str
    dry_run: bool = False
    approve: bool = False

    # Intelligence contexts
    memory_context: List[MemoryRead] = Field(default_factory=list)
    research_evidence: Optional[ResearchResponse] = None

    # Planning & Safety
    plan_steps: List[PlanStep] = Field(default_factory=list)
    critic_evaluation: Optional[Dict[str, Any]] = None

    # Execution & Auditing
    execution_results: Dict[int, ExecutionResult] = Field(default_factory=dict)
    reflection_summary: Optional[Dict[str, Any]] = None
    agent_logs: List[AgentLogEntry] = Field(default_factory=list)

    # Telemetry
    model_used: str = "nvidia/llama-3.1-nemotron-70b-instruct"
    total_tokens: int = 0
    total_latency_ms: float = 0.0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseAgent:
    """Base interface for specialized NOVA intelligence agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = get_nebius_client()

    async def run(self, state: AgentState, db: Any) -> AgentState:
        """Execute agent's specific responsibility over the shared state."""
        raise NotImplementedError
