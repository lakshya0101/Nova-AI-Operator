"""Memory Agent: Retrieves relevant personal context and updates persistent memory."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session

from .base import BaseAgent, AgentState, AgentLogEntry
from ..services import memory_service
from ..schemas.memory import MemoryCreate, MemoryCategory


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MemoryAgent", role="Personal Context & Semantic Retrieval")

    async def run(self, state: AgentState, db: Session) -> AgentState:
        # Retrieve context semantically matching user instruction
        memories = memory_service.search_memories(
            db=db,
            query=state.instruction,
            limit=5,
            min_score=0.1,
        )

        state.memory_context = memories
        titles = [m.title for m in memories]
        detail_msg = f"Retrieved {len(memories)} relevant personal context records: {', '.join(titles) if titles else 'None'}"

        state.agent_logs.append(
            AgentLogEntry(
                agent=self.name,
                action="retrieve_context",
                detail=detail_msg,
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
            )
        )
        return state

