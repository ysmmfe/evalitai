from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.run import EvaluationRun
    from models.suite import EvaluationSuite


class Project(Base):
    """A project groups evaluation suites and runs under a single namespace."""

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    suites: Mapped[list[EvaluationSuite]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    runs: Mapped[list[EvaluationRun]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
