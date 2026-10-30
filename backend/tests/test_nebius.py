"""Automated tests for Nebius Token Factory and NVIDIA Nemotron client."""

import pytest
from app.core.nebius_client import NebiusClient, LLMResponse, ModelUsage


@pytest.mark.asyncio
async def test_nebius_client_model_routing():
    client = NebiusClient()
    lightning_model = client.select_model("lightning")
    super_model = client.select_model("super")

    assert "nemotron" in lightning_model.lower()
    assert "nemotron" in super_model.lower()
    assert lightning_model != super_model


@pytest.mark.asyncio
async def test_nebius_client_offline_simulation():
    client = NebiusClient(api_key=None)
    assert not client.is_live

    # Test planner simulation
    messages = [
        {"role": "system", "content": "You are the NOVA Planner Agent."},
        {"role": "user", "content": "Organize my evening and research AI agents."},
    ]
    response = await client.chat_completion(messages, tier="super")
    assert isinstance(response, LLMResponse)
    assert response.usage.latency_ms > 0
    assert response.usage.total_tokens > 0
    assert response.structured_data is not None
    assert "subtasks" in response.structured_data
    assert len(response.structured_data["subtasks"]) >= 3


@pytest.mark.asyncio
async def test_nebius_critic_and_reflection_simulation():
    client = NebiusClient(api_key=None)

    critic_msgs = [
        {"role": "system", "content": "You are the NOVA Critic Agent."},
        {"role": "user", "content": "Evaluate plan feasibility."},
    ]
    critic_res = await client.chat_completion(critic_msgs, tier="lightning")
    assert critic_res.structured_data["status"] == "approved"

    refl_msgs = [
        {"role": "system", "content": "You are the NOVA Reflection Agent."},
        {"role": "user", "content": "Analyze workflow completion."},
    ]
    refl_res = await client.chat_completion(refl_msgs, tier="lightning")
    assert "memory_updates" in refl_res.structured_data

