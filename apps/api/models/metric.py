from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.run import EvaluationRun


class MetricDefinition(Base):
    """A built-in or user-registered metric (e.g. faithfulness, answer_relevancy)."""

    __tablename__ = "metric_definitions"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_deterministic: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    configurations: Mapped[list[MetricConfiguration]] = relationship(
        back_populates="metric"
    )


class MetricConfiguration(Base):
    """Associates a metric with an evaluation run and stores its config."""

    __tablename__ = "metric_configurations"

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    metric_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("metric_definitions.id"), nullable=False
    )
    config: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    run: Mapped[EvaluationRun] = relationship(back_populates="metric_configurations")
    metric: Mapped[MetricDefinition] = relationship(back_populates="configurations")
