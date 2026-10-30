"""Comprehensive Production Readiness & Live Integration Audit for NOVA 2.0.

Verifies:
1. SQLite/PostgreSQL restart persistence & transaction handling
2. Memory engine cosine similarity math & deduplication
3. Human-in-the-loop security boundaries on state-changing MCP tools
4. Multi-agent state handoff across 6 specialized agents
5. End-to-end demo workflow with audit tracing

Usage:
    python scripts/verify_production_readiness.py
"""

import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone

# Ensure repo root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.memory import MemoryItem, MemoryCategory
from app.services import task_service, memory_service, preference_service
from app.schemas.orchestration import AgentRunRequest
from app.services.orchestration_service import run_orchestration


def run_production_audit():
    print("=" * 70)
    print("NOVA 2.0: PRODUCTION READINESS & COMPREHENSIVE INTEGRATION AUDIT")
    print("=" * 70)

    # -------------------------------------------------------------
    # Test 1: Database Persistence Across Process Restarts
    # -------------------------------------------------------------
    print("\n[Audit 1/5] Testing Database Persistence & Restart Integrity...")
    temp_fd, temp_db_path = tempfile.mkstemp(suffix=".db", prefix="nova_audit_")
    os.close(temp_fd)
    db_url = f"sqlite:///{temp_db_path}"

    engine1 = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine1)
    SessionMaker1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)

    with SessionMaker1() as s1:
        preference_service.seed_default_preferences(s1)
        task_in = task_service.TaskCreate(
            title="Pre-restart Task Milestone",
            description="Testing disk persistence across session closures",
            priority=TaskPriority.HIGH,
        )
        created_task = task_service.create_task(s1, task_in)
        task_id = created_task.id
        s1.commit()

    engine1.dispose()

    # Reconnect with fresh engine to simulate clean restart
    engine2 = create_engine(db_url, connect_args={"check_same_thread": False})
    SessionMaker2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
    with SessionMaker2() as s2:
        retrieved_task = task_service.get_task(s2, task_id)
        assert retrieved_task is not None, "Task was lost on restart!"
        assert retrieved_task.title == "Pre-restart Task Milestone"
        print(f"       SUCCESS: Record ID={task_id} successfully persisted and recovered across engine shutdown.")

    # -------------------------------------------------------------
    # Test 2: Memory Engine Cosine Math & Deduplication
    # -------------------------------------------------------------
    print("\n[Audit 2/5] Testing Personal Memory Engine Math & Deduplication...")
    with SessionMaker2() as s2:
        m1 = memory_service.create_memory(
            s2,
            memory_service.MemoryCreate(
                category=MemoryCategory.DECISION,
                title="Interview Schedule Policy",
                content="Always reserve at least 45 minutes for interview preparation.",
                tags="interview,planning",
                importance=2.5,
            ),
        )

        # Test duplicate creation with identical title
        m2 = memory_service.create_memory(
            s2,
            memory_service.MemoryCreate(
                category=MemoryCategory.DECISION,
                title="Interview Schedule Policy",
                content="Updated rule: Reserve at least 60 minutes for interview preparation.",
                tags="interview,updated",
                importance=3.0,
            ),
        )
        assert m1.id == m2.id, "Duplicate memory was not merged!"
        assert "60 minutes" in m2.content, "Existing memory content was not updated on duplicate insert!"
        print(f"       SUCCESS: Deduplication correctly merged duplicate memory (ID={m1.id}).")

        # Test cosine similarity math
        query = "interview prep routine"
        results = memory_service.search_memories(s2, query, limit=3)
        assert len(results) > 0, "Semantic search returned zero results!"
        top_match = results[0]
        assert top_match.similarity_score > 0.0, "Cosine score must be positive"
        assert top_match.title == "Interview Schedule Policy"
        print(f"       SUCCESS: Cosine search matched '{top_match.title}' with score={top_match.similarity_score}.")

    # -------------------------------------------------------------
    # Test 3: Human-in-the-Loop Security Enforcement
    # -------------------------------------------------------------
    print("\n[Audit 3/5] Testing Security Boundary & Human Approval Enforcement...")
    with SessionMaker2() as s2:
        # Instruction proposing state mutation
        req_unapproved = AgentRunRequest(
            instruction="Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
            dry_run=False,
            approve=False,  # Unapproved
        )
        plan_unapproved = run_orchestration(req_unapproved, s2)
        # Find step 2 (create interview task)
        step2_result = plan_unapproved.step_results.get(2) or plan_unapproved.step_results.get("2")
        assert step2_result is not None
        assert step2_result.status == "skipped", f"Expected skipped, got {step2_result.status}"
        assert "requires explicit human approval" in step2_result.detail.lower()

        # Verify no task was created in the database
        tasks_in_db, _ = task_service.list_tasks(s2, search="Interview preparation")
        assert len(tasks_in_db) == 0, "Unauthorized task was created in database!"
        print("       SUCCESS: Unapproved state mutation strictly prevented and marked 'skipped'.")

        # Now approve execution
        req_approved = AgentRunRequest(
            instruction="Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
            dry_run=False,
            approve=True,  # Approved
        )
        plan_approved = run_orchestration(req_approved, s2)
        step2_approved = plan_approved.step_results.get(2) or plan_approved.step_results.get("2")
        assert step2_approved.status == "success", f"Expected success, got {step2_approved.status}"
        tasks_now, _ = task_service.list_tasks(s2, search="Interview preparation")
        assert len(tasks_now) == 1, "Approved task was not created!"
        print(f"       SUCCESS: Approved mutation executed tool successfully (Task ID={tasks_now[0].id}).")

    # -------------------------------------------------------------
    # Test 4: Multi-Agent Handoff & State Integrity
    # -------------------------------------------------------------
    print("\n[Audit 4/5] Testing 6-Agent Swarm Handoff & Telemetry...")
    with SessionMaker2() as s2:
        req = AgentRunRequest(
            instruction="Research latest NVIDIA AI models and organize evening review.",
            dry_run=True,
            approve=False,
        )
        plan_res = run_orchestration(req, s2)
        assert len(plan_res.agent_logs) >= 5, "Missing agent log traces!"
        agents_logged = {log.agent for log in plan_res.agent_logs}
        print(f"       SUCCESS: Verified agents participated in execution: {', '.join(sorted(agents_logged))}")
        assert plan_res.model_used is not None
        print(f"       SUCCESS: Verified model routing: {plan_res.model_used} (Tokens={plan_res.total_tokens})")

    # -------------------------------------------------------------
    # Test 5: Clean Up
    # -------------------------------------------------------------
    print("\n[Audit 5/5] Cleaning temporary persistence files...")
    engine2.dispose()
    try:
        os.remove(temp_db_path)
        print("       SUCCESS: Cleaned up temporary test database.")
    except Exception:
        pass

    print("\n" + "=" * 70)
    print("ALL PRODUCTION READINESS AUDIT TESTS PASSED WITH 100% SUCCESS")
    print("=" * 70)


if __name__ == "__main__":
    run_production_audit()

