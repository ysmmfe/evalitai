from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.event import Event
    from models.project import Project


class EvaluationSuite(Base):
    """A named collection of evaluation cases belonging to a project."""

    __tablename__ = "evaluation_suites"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[Project] = relationship(back_populates="suites")
    cases: Mapped[list[EvaluationCase]] = relationship(
        back_populates="suite", cascade="all, delete-orphan"
    )


class EvaluationCase(Base):
    """A single test case: a fixed input/context pair with expected behaviour."""

    __tablename__ = "evaluation_cases"

    suite_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_suites.id", ondelete="CASCADE"),
        nullable=False,
    )
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    context_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    expected_output: Mapped[str | None] = mapped_column(Text, nullable=True)

    suite: Mapped[EvaluationSuite] = relationship(back_populates="cases")
    events: Mapped[list[Event]] = relationship(back_populates="case")
