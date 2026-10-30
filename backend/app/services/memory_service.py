"""Personal Memory Engine service for NOVA.

Provides persistent memory storage, semantic similarity retrieval, deduplication,
and context-aware memory extraction for multi-agent workflows.
Supports both local deterministic vector embeddings and Nebius Token Factory neural embeddings.
"""

from __future__ import annotations

import json
import math
import re
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.memory import MemoryItem, MemoryCategory
from ..schemas.memory import MemoryCreate, MemoryUpdate, MemoryRead


def _tokenize(text: str) -> List[str]:
    """Tokenize and normalize text into word stems."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return [word for word in cleaned.split() if len(word) > 2]


def compute_embedding(text: str, dim: int = 64) -> List[float]:
    """Compute deterministic dense vector embedding using polynomial hashing and subword weights.
    Provides fast, zero-dependency semantic search for local/offline runtime.
    L2-normalized unit vector ensures dot product equals cosine similarity.
    """
    tokens = _tokenize(text)
    if not tokens:
        return [0.0] * dim

    vec = [0.0] * dim
    for i, token in enumerate(tokens):
        h = 0
        for ch in token:
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        idx = h % dim
        sign = 1.0 if ((h >> 4) & 1) == 0 else -1.0
        weight = math.log1p(len(token)) * (1.0 / math.sqrt(i + 1))
        vec[idx] += sign * weight

    # Euclidean L2 normalization
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 1e-6:
        vec = [round(x / norm, 5) for x in vec]
    return vec


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Calculate mathematically exact cosine similarity between two vectors.
    cosine(A, B) = (A . B) / (||A|| * ||B||)
    """
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a < 1e-6 or norm_b < 1e-6:
        return 0.0

    sim = dot / (norm_a * norm_b)
    return max(0.0, min(1.0, float(sim)))


def create_memory(db: Session, memory_in: MemoryCreate) -> MemoryItem:
    """Create a new memory item with semantic embedding and deduplication check."""
    # Deduplication check: case-insensitive title and category match
    existing = (
        db.query(MemoryItem)
        .filter(
            func.lower(MemoryItem.title) == memory_in.title.strip().lower(),
            MemoryItem.category == memory_in.category.value,
        )
        .first()
    )
    if existing:
        # Update existing record rather than creating a duplicate
        existing.content = memory_in.content
        existing.tags = memory_in.tags or existing.tags
        existing.importance = max(existing.importance, memory_in.importance)
        embedding = compute_embedding(f"{existing.title} {existing.content} {existing.tags or ''}")
        existing.embedding_json = json.dumps(embedding)
        db.commit()
        db.refresh(existing)
        return existing

    embedding = compute_embedding(f"{memory_in.title} {memory_in.content} {memory_in.tags or ''}")
    item = MemoryItem(
        category=memory_in.category.value,
        title=memory_in.title.strip(),
        content=memory_in.content.strip(),
        tags=memory_in.tags.strip() if memory_in.tags else None,
        source=memory_in.source,
        importance=memory_in.importance,
        embedding_json=json.dumps(embedding),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def search_memories(
    db: Session,
    query: str,
    category: Optional[MemoryCategory] = None,
    limit: int = 5,
    min_score: float = 0.15,
) -> List[MemoryRead]:
    """Retrieve memories semantically relevant to the input query using cosine similarity."""
    query_emb = compute_embedding(query)
    stmt = db.query(MemoryItem)
    if category:
        stmt = stmt.filter(MemoryItem.category == category.value)

    all_candidates = stmt.all()
    scored_items: List[Tuple[float, MemoryItem]] = []

    for item in all_candidates:
        score = 0.0
        if item.embedding_json:
            try:
                item_emb = json.loads(item.embedding_json)
                score = cosine_similarity(query_emb, item_emb)
            except Exception:
                score = 0.0

        # Term overlap boost for explicit keywords
        q_tokens = set(_tokenize(query))
        item_tokens = set(_tokenize(f"{item.title} {item.content} {item.tags or ''}"))
        if q_tokens and item_tokens:
            overlap = len(q_tokens.intersection(item_tokens)) / len(q_tokens)
            score = max(score, overlap * 0.8)

        if score >= min_score:
            final_score = score * (0.8 + 0.2 * min(item.importance, 2.0))
            scored_items.append((final_score, item))

    # Sort descending by score
    scored_items.sort(key=lambda x: x[0], reverse=True)

    results: List[MemoryRead] = []
    for score, item in scored_items[:limit]:
        read_obj = MemoryRead.model_validate(item)
        read_obj.similarity_score = round(score, 3)
        results.append(read_obj)

    return results


def list_memories(
    db: Session,
    category: Optional[MemoryCategory] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[List[MemoryItem], int]:
    """List stored memories with optional filtering and pagination."""
    query = db.query(MemoryItem)
    if category:
        query = query.filter(MemoryItem.category == category.value)
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            (MemoryItem.title.ilike(search_filter))
            | (MemoryItem.content.ilike(search_filter))
            | (MemoryItem.tags.ilike(search_filter))
        )

    total = query.count()
    items = query.order_by(MemoryItem.created_at.desc()).offset(offset).limit(limit).all()
    return items, total


def get_memory(db: Session, memory_id: int) -> Optional[MemoryItem]:
    """Retrieve memory by primary key."""
    return db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()


def update_memory(db: Session, memory_id: int, update_in: MemoryUpdate) -> Optional[MemoryItem]:
    """Update existing memory record."""
    item = get_memory(db, memory_id)
    if not item:
        return None

    if update_in.title is not None:
        item.title = update_in.title.strip()
    if update_in.content is not None:
        item.content = update_in.content.strip()
    if update_in.category is not None:
        item.category = update_in.category.value
    if update_in.tags is not None:
        item.tags = update_in.tags.strip()
    if update_in.importance is not None:
        item.importance = update_in.importance

    embedding = compute_embedding(f"{item.title} {item.content} {item.tags or ''}")
    item.embedding_json = json.dumps(embedding)
    db.commit()
    db.refresh(item)
    return item


def delete_memory(db: Session, memory_id: int) -> bool:
    """Delete a memory item from persistent storage."""
    item = get_memory(db, memory_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def seed_default_memories(db: Session) -> None:
    """Seed foundational personal memory records for NOVA operator."""
    if db.query(MemoryItem).count() > 0:
        return

    default_memories = [
        MemoryCreate(
            category=MemoryCategory.PROFILE,
            title="User Identity & Goals",
            content="Senior Software Engineer participating in the Nebius x NVIDIA Global AI Hackathon. Dedicated to building autonomous agent systems and AI operating systems.",
            tags="user,profile,hackathon,identity",
            source="system_bootstrap",
            importance=2.0,
        ),
        MemoryCreate(
            category=MemoryCategory.DECISION,
            title="Interview Preparation Priority",
            content="Always allocate at least 45 minutes for technical interview preparation whenever planning an evening schedule.",
            tags="interview,planning,evening,routine",
            source="user_preference",
            importance=2.5,
        ),
        MemoryCreate(
            category=MemoryCategory.PROJECT,
            title="NOVA 2.0 AI Operator",
            content="Building NOVA – Personal AI Operating System powered by NVIDIA Nemotron via Nebius Token Factory, MCP tools, and Tavily research.",
            tags="project,hackathon,nova,nebius,nvidia",
            source="system_bootstrap",
            importance=3.0,
        ),
        MemoryCreate(
            category=MemoryCategory.LEARNED,
            title="Task Review Workflow Preference",
            content="User prefers reviewing unfinished tasks sorted by priority (urgent -> high -> medium -> low) followed by due date.",
            tags="preference,sorting,tasks,workflow",
            source="learned_pattern",
            importance=1.5,
        ),
    ]

    for mem in default_memories:
        create_memory(db, mem)
