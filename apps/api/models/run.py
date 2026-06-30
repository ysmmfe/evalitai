import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.metric import MetricConfiguration
    from models.project import Project
    from models.result import EvaluationResult


class EvaluationRun(Base):
    """A single execution of the evaluation pipeline over a suite."""

    __tablename__ = "evaluation_runs"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    # pending | running | completed | failed
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    # The system version being evaluated (matches Event.system_version).
    system_version: Mapped[str] = mapped_column(String(255), nullable=False)

    project: Mapped["Project"] = relationship(back_populates="runs")
    results: Mapped[list["EvaluationResult"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )
    metric_configurations: Mapped[list["MetricConfiguration"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )
