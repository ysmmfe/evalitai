from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.run import EvaluationRun


class Baseline(Base):
    """Marks a specific run as the reference point for future comparisons."""

    __tablename__ = "baselines"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_runs.id"),
        nullable=False,
        unique=True,
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    run: Mapped[EvaluationRun] = relationship()
