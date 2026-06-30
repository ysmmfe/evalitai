from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class EvaluatorModelVersion(Base):
    """Tracks which LLM model version was used as the judge in each evaluation."""

    __tablename__ = "evaluator_model_versions"

    # LiteLLM model identifier, e.g. "openai/gpt-4o", "anthropic/claude-3-5-sonnet".
    model_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    # The system prompt used for this judge version.
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Semantic version tag so score history stays reproducible when prompt changes.
    version_tag: Mapped[str] = mapped_column(String(50), nullable=False)
