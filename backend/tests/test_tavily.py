"""Automated tests for NOVA Tavily Research Service."""

import pytest
from app.schemas.research import ResearchRequest
from app.services.tavily_service import execute_tavily_research


@pytest.mark.asyncio
async def test_tavily_research_execution():
    req = ResearchRequest(
        query="NVIDIA Nemotron AI agent developments on Nebius",
        max_results=3,
        search_depth="basic",
    )
    res = await execute_tavily_research(req)
    assert res.query == req.query
    assert len(res.sources) >= 1
    assert res.sources[0].url.startswith("http")
    assert res.summary is not None


def test_research_api_endpoint(client):
    res = client.post(
        "/api/research",
        json={"query": "AI Engineer interview prep", "max_results": 2},
    )
    assert res.status_code == 200
    data = res.json()
    assert "sources" in data
    assert len(data["sources"]) >= 1
    assert "answer" in data

