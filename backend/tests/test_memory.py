"""Automated tests for NOVA Personal Memory Engine."""

import pytest
from app.models.memory import MemoryCategory
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services import memory_service


def test_memory_embedding_and_similarity():
    text1 = "Prepare for technical AI agent architecture interview"
    text2 = "Practice system design for AI agents and interviews"
    text3 = "Buy groceries milk eggs and bread"

    emb1 = memory_service.compute_embedding(text1)
    emb2 = memory_service.compute_embedding(text2)
    emb3 = memory_service.compute_embedding(text3)

    assert len(emb1) == 64
    assert len(emb2) == 64
    assert len(emb3) == 64

    sim_related = memory_service.cosine_similarity(emb1, emb2)
    sim_unrelated = memory_service.cosine_similarity(emb1, emb3)

    assert sim_related > sim_unrelated


def test_memory_crud_and_deduplication(db_session):
    mem_in = MemoryCreate(
        category=MemoryCategory.PROJECT,
        title="Hackathon Goal",
        content="Deliver NOVA AI Operating System for Nebius x NVIDIA Hackathon",
        tags="hackathon,nvidia,nova",
        importance=2.0,
    )
    created = memory_service.create_memory(db_session, mem_in)
    assert created.id is not None
    assert created.title == "Hackathon Goal"

    # Search
    results = memory_service.search_memories(db_session, query="nvidia hackathon", limit=5)
    assert len(results) >= 1
    assert any("Hackathon Goal" in r.title for r in results)

    # Deduplication check: re-creating same title should update existing
    mem_in_dup = MemoryCreate(
        category=MemoryCategory.PROJECT,
        title="Hackathon Goal",
        content="Updated content for Nebius x NVIDIA Hackathon",
        tags="hackathon,nvidia,updated",
        importance=3.0,
    )
    re_created = memory_service.create_memory(db_session, mem_in_dup)
    assert re_created.id == created.id
    assert "Updated content" in re_created.content

    # Update
    updated = memory_service.update_memory(
        db_session, created.id, MemoryUpdate(title="Updated Hackathon Goal")
    )
    assert updated.title == "Updated Hackathon Goal"

    # Delete
    deleted = memory_service.delete_memory(db_session, created.id)
    assert deleted is True
    assert memory_service.get_memory(db_session, created.id) is None


def test_memory_api_endpoints(client):
    # Test POST /api/memories
    res = client.post(
        "/api/memories",
        json={
            "category": "decision",
            "title": "Evening Routine Rule",
            "content": "Dedicate 45 minutes to interview prep every evening.",
            "tags": "evening,interview",
            "importance": 2.5,
        },
    )
    assert res.status_code == 201
    mem_data = res.json()
    mem_id = mem_data["id"]

    # Test GET /api/memories
    list_res = client.get("/api/memories?search=Evening")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # Test POST /api/memories/search
    search_res = client.post(
        "/api/memories/search",
        json={"query": "interview evening preparation", "limit": 3},
    )
    assert search_res.status_code == 200
    search_items = search_res.json()
    assert len(search_items) >= 1

    # Test DELETE /api/memories/{id}
    del_res = client.delete(f"/api/memories/{mem_id}")
    assert del_res.status_code == 204

