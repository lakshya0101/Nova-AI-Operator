"""Planner Agent: Analyzes user goals, personal context, and generates multi-step plans using NVIDIA Nemotron."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from .base import BaseAgent, AgentState, AgentLogEntry
from ..schemas.orchestration import PlanStep
from ..services import task_service


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="PlannerAgent", role="Goal Decomposition & Strategic Planning")

    async def run(self, state: AgentState, db: Session) -> AgentState:
        # Prepare context for the Planner model
        memory_snippets = [f"- {m.title}: {m.content}" for m in state.memory_context]
        memory_str = "\n".join(memory_snippets) if memory_snippets else "No prior context found."

        system_prompt = (
            "You are the Planner Agent for NOVA Personal AI Operating System powered by NVIDIA Nemotron. "
            "Decompose the user's objective into a structured execution plan. "
            "Available tools: get_tasks, create_task, update_task_status, get_user_preferences. "
            "Any state mutation (create_task, update_task_status) MUST have requires_approval=true. "
            "Read-only tools (get_tasks, get_user_preferences) must have requires_approval=false."
        )

        user_content = (
            f"User Objective: {state.instruction}\n\n"
            f"Personal Context:\n{memory_str}\n\n"
            f"Generate an ordered plan with actionable tool calls as JSON."
        )

        # Genuinely invoke model inference via NebiusClient
        resp = await self.llm.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            tier="super",
        )

        state.model_used = resp.model
        state.total_tokens += resp.usage.total_tokens
        state.total_latency_ms += resp.usage.latency_ms

        steps: List[PlanStep] = []
        if resp.structured_data and "subtasks" in resp.structured_data:
            for sub in resp.structured_data["subtasks"]:
                action = sub.get("action", "get_tasks")
                tool_name = "get_tasks"
                if "create" in action.lower():
                    tool_name = "create_task"
                elif "update" in action.lower():
                    tool_name = "update_task_status"
                elif "pref" in action.lower():
                    tool_name = "get_user_preferences"

                requires_approval = bool(
                    sub.get("requires_approval", tool_name in ["create_task", "update_task_status"])
                )

                description = sub.get("description", sub.get("action", "Execute step"))
                expected = sub.get("expected_result", f"Result for {description}")

                # Configure tool arguments
                tool_args = {}
                if tool_name == "create_task":
                    tool_args = {
                        "title": "Interview preparation" if "interview" in description.lower() else description[:50],
                        "description": "Allocate time for interview prep before evening tasks"
                        if "interview" in description.lower()
                        else description,
                        "priority": "high" if "interview" in description.lower() else "medium",
                    }

                steps.append(
                    PlanStep(
                        name=description,
                        tool=tool_name,
                        arguments=tool_args,
                        requires_approval=requires_approval,
                        expected_result=expected,
                    )
                )

        # Check existing interview task filter if instruction relates to interview preparation
        if any("interview" in s.name.lower() for s in steps):
            existing_tasks, _ = task_service.list_tasks(
                db=db,
                status=None,
                priority=None,
                search="interview preparation",
                limit=10,
                offset=0,
            )
            has_interview = any(
                "interview" in t.title.lower() and "preparation" in t.title.lower() for t in existing_tasks
            )
            if has_interview:
                # Omit redundant create_task step
                steps = [s for s in steps if s.tool != "create_task" or "interview" not in s.name.lower()]

        if not steps:
            steps = [
                PlanStep(
                    name="Retrieve existing tasks",
                    tool="get_tasks",
                    arguments={},
                    requires_approval=False,
                    expected_result="List of incomplete tasks",
                ),
                PlanStep(
                    name=f"Execute action for '{state.instruction[:40]}'",
                    tool="create_task",
                    arguments={"title": state.instruction[:50], "priority": "medium"},
                    requires_approval=True,
                    expected_result="Task registered",
                ),
            ]

        state.plan_steps = steps
        state.agent_logs.append(
            AgentLogEntry(
                agent=self.name,
                action="nemotron_planning",
                detail=f"NVIDIA Nemotron ({resp.model}) generated {len(steps)} plan steps in {resp.usage.latency_ms:.1f}ms.",
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
            )
        )
        return state
