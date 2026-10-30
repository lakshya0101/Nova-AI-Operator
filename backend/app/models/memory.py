"""Memory persistence model for NOVA Personal AI Operating System."""

import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func
from ..database import Base


class MemoryCategory(str, enum.Enum):
    PROFILE = "profile"
    CONVERSATION = "conversation"
    DECISION = "decision"
    PROJECT = "project"
    TASK = "task"
    WORKFLOW = "workflow"
    LEARNED = "learned"


class MemoryItem(Base):
    """SQLAlchemy model representing a persistent contextual memory item in NOVA."""

    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String(50), nullable=False, default=MemoryCategory.LEARNED.value, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)  # Comma-separated tags
    source = Column(String(100), nullable=False, default="user_instruction")
    importance = Column(Float, nullable=False, default=1.0)
    embedding_json = Column(Text, nullable=True)  # Serialized vector representation for semantic search
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<MemoryItem(id={self.id}, category='{self.category}', title='{self.title}')>"

