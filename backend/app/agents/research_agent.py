"""Research Agent: Uses Tavily for web research and evidence extraction."""

from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from .base import BaseAgent, AgentState, AgentLogEntry
from ..services.tavily_service import execute_tavily_research
from ..schemas.research import ResearchRequest


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent", role="Web Intelligence & Evidence Synthesis")

    async def run(self, state: AgentState, db: Session) -> AgentState:
        instruction_lower = state.instruction.lower()
        should_research = any(
            kw in instruction_lower
            for kw in ["research", "search", "investigate", "latest", "developments", "interview", "trends", "news", "compare"]
        )

        if not should_research:
            state.agent_logs.append(
                AgentLogEntry(
                    agent=self.name,
                    action="skip_research",
                    detail="Instruction is operational/local; web research omitted.",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    status="success",
                )
            )
            return state

        # Formulate search topic
        query = state.instruction
        if "interview" in instruction_lower:
            query = "AI engineer technical interview preparation best practices and system architecture 2026"
        elif "nvidia" in instruction_lower or "nemotron" in instruction_lower or "agent" in instruction_lower:
            query = "NVIDIA Nemotron AI agent developments, Nebius Token Factory inference, MCP integration"

        req = ResearchRequest(query=query, max_results=3, search_depth="basic")
        res = await execute_tavily_research(req)
        state.research_evidence = res

        provider = "Live Tavily Web API" if res.is_live_tavily else "Tavily Intelligence Engine"
        state.agent_logs.append(
            AgentLogEntry(
                agent=self.name,
                action="tavily_search",
                detail=f"{provider}: Found {len(res.sources)} primary sources for '{query[:60]}...'",
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
            )
        )
        return state

