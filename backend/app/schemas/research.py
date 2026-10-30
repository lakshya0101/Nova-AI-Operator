"""Pydantic schemas for NOVA Tavily Research capability."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchSource(BaseModel):
    title: str
    url: str
    content: str
    score: Optional[float] = None


class ResearchRequest(BaseModel):
    query: str = Field(..., description="Research query or topic to investigate")
    max_results: int = Field(default=5, ge=1, le=10)
    search_depth: str = Field(default="basic", description="basic or advanced")
    include_answer: bool = Field(default=True)


class ResearchResponse(BaseModel):
    query: str
    answer: Optional[str] = None
    sources: List[ResearchSource] = Field(default_factory=list)
    summary: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_live_tavily: bool = False

