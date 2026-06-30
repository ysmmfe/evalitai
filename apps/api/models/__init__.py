# Import all models here so Alembic can detect them during autogenerate.
from models.artifact import Artifact
from models.audit import AuditLog
from models.baseline import Baseline
from models.comparison import ComparisonReport
from models.criterion import CustomCriterion
from models.evaluator import EvaluatorModelVersion
from models.event import Event, EventVersion
from models.metric import MetricConfiguration, MetricDefinition
from models.project import Project
from models.result import EvaluationResult
from models.review import HumanReview
from models.run import EvaluationRun
from models.suite import EvaluationCase, EvaluationSuite

__all__ = [
    "Project",
    "EvaluationSuite",
    "EvaluationCase",
    "Event",
    "EventVersion",
    "MetricDefinition",
    "MetricConfiguration",
    "CustomCriterion",
    "EvaluatorModelVersion",
    "EvaluationRun",
    "EvaluationResult",
    "Baseline",
    "ComparisonReport",
    "HumanReview",
    "Artifact",
    "AuditLog",
]
