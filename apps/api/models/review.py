import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class HumanReview(Base):
    """Optional human annotation that can override or supplement an automated score."""

    __tablename__ = "human_reviews"

    result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_results.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    # Human-assigned score (0.0–1.0), overrides automated score in reports.
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # agree | disagree | unclear
    verdict: Mapped[str] = mapped_column(String(20), nullable=False, default="agree")
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewer_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
