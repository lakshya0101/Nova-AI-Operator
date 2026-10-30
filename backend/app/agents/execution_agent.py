"""Execution Agent: Executes approved actions through validated MCP tool functions."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.orm import Session

from .base import BaseAgent, AgentState, AgentLogEntry
from ..schemas.orchestration import PlanStep, ExecutionResult
from ..services import task_service, preference_service
from ..models.task import TaskPriority, TaskStatus


class ExecutionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ExecutionAgent", role="MCP Tool Invocation & Action Execution")

    async def run(self, state: AgentState, db: Session) -> AgentState:
        step_results: Dict[int, ExecutionResult] = {}

        for idx, step in enumerate(state.plan_steps):
            result = self._execute_step(step, db, state.dry_run, state.approve)
            step_results[idx] = result

            log_status = (
                "success"
                if result.status == "success"
                else ("waiting_approval" if result.status == "skipped" else "failed")
            )
            state.agent_logs.append(
                AgentLogEntry(
                    agent=self.name,
                    action=f"execute_step_{idx + 1}",
                    detail=f"[{step.tool}] {step.name} -> {result.status} ({result.detail or 'OK'})",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    status=log_status,
                )
            )

        state.execution_results = step_results
        return state

    def _execute_step(self, step: PlanStep, db: Session, dry_run: bool, approve: bool) -> ExecutionResult:
        # Handle virtual steps (e.g. proposing ordering locally)
        if step.tool == "get_tasks" and step.name.startswith("Propose"):
            return ExecutionResult(status="success", detail="Ordering computed locally")

        # Security boundary: State-changing tools strictly require human approval
        is_mutation = step.tool in {"create_task", "update_task_status"}

        if (step.requires_approval or is_mutation) and not approve:
            return ExecutionResult(status="skipped", detail="Step requires explicit human approval")

        if dry_run and is_mutation:
            return ExecutionResult(status="skipped", detail="Dry‑run mode – mutation not performed")

        try:
            if step.tool == "get_tasks":
                tasks, total = task_service.list_tasks(
                    db=db,
                    status=None,
                    priority=None,
                    search=None,
                    limit=100,
                    offset=0,
                )
                result = {
                    "total": total,
                    "tasks": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "priority": t.priority,
                            "status": t.status,
                            "due_date": t.due_date.isoformat() if t.due_date else None,
                        }
                        for t in tasks
                    ],
                }
                return ExecutionResult(status="success", output=result)

            elif step.tool == "create_task":
                args = step.arguments
                title = str(args.get("title", "")).strip()
                if not title:
                    return ExecutionResult(status="failed", detail="Task title cannot be empty")

                # Duplicate prevention: if a task with this exact title already exists, reuse it
                existing = None
                try:
                    tasks, _ = task_service.list_tasks(
                        db=db,
                        status=None,
                        priority=None,
                        search=title,
                        limit=10,
                        offset=0,
                    )
                    for t in tasks:
                        if t.title.strip().lower() == title.lower():
                            existing = t
                            break
                except Exception:
                    existing = None

                if existing:
                    return ExecutionResult(
                        status="success",
                        output={"id": existing.id, "title": existing.title},
                        detail="Task already exists – reused",
                    )

                priority_str = str(args.get("priority", "medium")).lower()
                valid_priorities = {p.value for p in TaskPriority}
                if priority_str not in valid_priorities:
                    priority_str = "medium"

                task_in = task_service.TaskCreate(
                    title=title,
                    description=args.get("description"),
                    priority=TaskPriority(priority_str),
                    due_date=args.get("due_date"),
                )
                task = task_service.create_task(db=db, task_in=task_in)
                return ExecutionResult(
                    status="success",
                    output={"id": task.id, "title": task.title},
                    detail="Task created",
                )

            elif step.tool == "update_task_status":
                args = step.arguments
                task_id = args.get("task_id")
                if not task_id or not isinstance(task_id, int) or task_id <= 0:
                    return ExecutionResult(status="failed", detail="Invalid task_id: must be positive integer")

                status_val = str(args.get("status", "")).lower().strip()
                valid_statuses = {s.value for s in TaskStatus}
                if status_val not in valid_statuses:
                    return ExecutionResult(status="failed", detail=f"Invalid status '{status_val}'")

                task = task_service.update_task_status(
                    db=db,
                    task_id=task_id,
                    status=TaskStatus(status_val),
                )
                if not task:
                    return ExecutionResult(status="failed", detail="Task not found")
                return ExecutionResult(
                    status="success",
                    output={"id": task.id, "status": task.status},
                    detail="Status updated",
                )

            elif step.tool == "get_user_preferences":
                prefs = preference_service.get_preferences(db=db)
                return ExecutionResult(status="success", output={"preferences": prefs})

            else:
                return ExecutionResult(status="failed", detail=f"Unsupported tool {step.tool}")

        except Exception as exc:
            return ExecutionResult(status="failed", detail=str(exc))
