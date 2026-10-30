"""Reflection Agent: Analyzes workflow execution, records insights, and updates memory using NVIDIA Nemotron."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session

from .base import BaseAgent, AgentState, AgentLogEntry
from ..services import memory_service
from ..schemas.memory import MemoryCreate, MemoryCategory


class ReflectionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ReflectionAgent", role="Post-Execution Analysis & Continuous Learning")

    async def run(self, state: AgentState, db: Session) -> AgentState:
        total_steps = len(state.plan_steps)
        results = state.execution_results.values()
        successes = sum(1 for r in results if r.status == "success")
        skipped = sum(1 for r in results if r.status == "skipped")
        failed = sum(1 for r in results if r.status == "failed")

        # Genuinely invoke model inference for post-execution analysis
        system_prompt = (
            "You are the Reflection Agent for NOVA Personal AI Operating System. "
            "Analyze the completed workflow, assess execution efficiency, and determine "
            "what learned context should be saved to long-term memory. Output JSON."
        )
        user_content = (
            f"Instruction: {state.instruction}\n"
            f"Dry Run: {state.dry_run}, Approved: {state.approve}\n"
            f"Total Steps: {total_steps}, Successes: {successes}, Skipped: {skipped}, Failed: {failed}"
        )

        resp = await self.llm.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            tier="lightning",
        )

        state.total_tokens += resp.usage.total_tokens
        state.total_latency_ms += resp.usage.latency_ms

        insights_text = "Workflow analysis completed."
        if resp.structured_data and "insights" in resp.structured_data:
            insights_text = resp.structured_data["insights"]

        # If execution succeeded on live mutations, update persistent memory
        if successes > 0 and not state.dry_run and state.approve:
            try:
                mem = MemoryCreate(
                    category=MemoryCategory.WORKFLOW,
                    title=f"Workflow Execution: {state.instruction[:40]}",
                    content=f"Executed workflow for objective: '{state.instruction}'. Actions confirmed and completed with {successes} successful step(s).",
                    tags="workflow,execution,success",
                    source="reflection_agent",
                    importance=1.2,
                )
                memory_service.create_memory(db, mem)
            except Exception:
                pass

        summary_data = {
            "total_steps": total_steps,
            "successes": successes,
            "skipped": skipped,
            "failed": failed,
            "insights": insights_text,
            "model": resp.model,
        }
        state.reflection_summary = summary_data

        state.agent_logs.append(
            AgentLogEntry(
                agent=self.name,
                action="reflect",
                detail=f"Nemotron Reflection: {insights_text}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
            )
        )
        return state
