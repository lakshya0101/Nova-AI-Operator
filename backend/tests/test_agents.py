"""Automated tests for NOVA Specialized Agents."""

import pytest
from app.agents.base import AgentState
from app.agents.memory_agent import MemoryAgent
from app.agents.research_agent import ResearchAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.critic_agent import CriticAgent
from app.agents.execution_agent import ExecutionAgent
from app.agents.reflection_agent import ReflectionAgent
from app.schemas.orchestration import AgentRunRequest
from app.services.orchestration_service import run_orchestration


@pytest.mark.asyncio
async def test_specialized_agents_pipeline_flow(db_session):
    state = AgentState(
        session_id="test-session-123",
        instruction="Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
        dry_run=True,
        approve=False,
    )

    # 1. Memory Agent
    mem_agent = MemoryAgent()
    state = await mem_agent.run(state, db_session)
    assert len(state.agent_logs) >= 1
    assert state.agent_logs[0].agent == "MemoryAgent"

    # 2. Research Agent
    res_agent = ResearchAgent()
    state = await res_agent.run(state, db_session)
    assert state.research_evidence is not None

    # 3. Planner Agent
    plan_agent = PlannerAgent()
    state = await plan_agent.run(state, db_session)
    assert len(state.plan_steps) >= 2

    # 4. Critic Agent
    critic_agent = CriticAgent()
    state = await critic_agent.run(state, db_session)
    assert state.critic_evaluation is not None

    # 5. Execution Agent
    exec_agent = ExecutionAgent()
    state = await exec_agent.run(state, db_session)
    assert len(state.execution_results) == len(state.plan_steps)

    # 6. Reflection Agent
    refl_agent = ReflectionAgent()
    state = await refl_agent.run(state, db_session)
    assert state.reflection_summary is not None


def test_end_to_end_orchestration_telemetry(client, db_session):
    payload = {
        "instruction": "Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
        "dry_run": True,
        "approve": False,
    }
    response = client.post("/api/agent/run", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "agent_logs" in data
    assert len(data["agent_logs"]) >= 5
    assert "memory_context" in data
    assert "research_evidence" in data
    assert "critic_evaluation" in data
    assert "reflection_summary" in data
    assert "model_used" in data
    assert "nemotron" in data["model_used"].lower()

