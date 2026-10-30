"""Pydantic schemas for NOVA Personal Memory Engine."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from ..models.memory import MemoryCategory


class MemoryCreate(BaseModel):
    category: MemoryCategory = Field(default=MemoryCategory.LEARNED, description="Category of the memory record")
    title: str = Field(..., max_length=255, description="Short descriptive title")
    content: str = Field(..., description="Detailed memory context or learned knowledge")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    source: str = Field(default="user_instruction", description="Source of memory origin")
    importance: float = Field(default=1.0, ge=0.0, le=5.0, description="Importance multiplier 0-5")


class MemoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[MemoryCategory] = None
    tags: Optional[str] = None
    importance: Optional[float] = None


class MemoryRead(BaseModel):
    id: int
    category: MemoryCategory
    title: str
    content: str
    tags: Optional[str] = None
    source: str
    importance: float
    created_at: datetime
    updated_at: datetime
    similarity_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class MemoryQuery(BaseModel):
    query: str = Field(..., description="Natural language search term for semantic retrieval")
    category: Optional[MemoryCategory] = None
    limit: int = Field(default=5, ge=1, le=50)
    min_score: float = Field(default=0.1, ge=0.0, le=1.0)


class MemoryListResponse(BaseModel):
    memories: List[MemoryRead]
    total: int
