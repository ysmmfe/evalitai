from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.run import EvaluationRun


class ComparisonReport(Base):
    """Diff between a candidate run and its baseline across all metrics."""

    __tablename__ = "comparison_reports"

    baseline_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluation_runs.id"), nullable=False
    )
    candidate_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluation_runs.id"), nullable=False
    )
    verdict: Mapped[str] = mapped_column(String(20), nullable=False, default="neutral")
    score_delta: Mapped[float | None] = mapped_column(Float, nullable=True)
    improved_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    regressed_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    neutral_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    metric_deltas: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    baseline_run: Mapped[EvaluationRun] = relationship(foreign_keys=[baseline_run_id])
    candidate_run: Mapped[EvaluationRun] = relationship(foreign_keys=[candidate_run_id])
