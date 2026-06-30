from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.suite import EvaluationCase


class Event(Base):
    """A captured LLM call emitted by the system under test."""

    __tablename__ = "events"

    case_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluation_cases.id"), nullable=True
    )
    system_version: Mapped[str] = mapped_column(String(255), nullable=False)
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=False)
    context_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    metadata_payload: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    case: Mapped[EvaluationCase | None] = relationship(back_populates="events")
    versions: Mapped[list[EventVersion]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


class EventVersion(Base):
    """Snapshot of an event's output at a specific system version (for diffing)."""

    __tablename__ = "event_versions"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    system_version: Mapped[str] = mapped_column(String(255), nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=False)

    event: Mapped[Event] = relationship(back_populates="versions")
