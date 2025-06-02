from datetime import UTC, datetime
from enum import Enum
from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field


class ExperimentStatus(str, Enum):
    """Enum for experiment execution status"""

    PENDING = "pending"
    INITIALIZING = "initialising"
    RUNNING = "running"
    ANALYZING = "analysing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExperimentConfig(BaseModel):
    """Configuration for an experiment"""

    name: str
    description: str
    parameters: dict[str, Any]


class Experiment(BaseModel):
    """Main experiment model"""

    id: str
    name: str
    description: str
    category: str
    tags: list[str] = []
    config: ExperimentConfig
    created_at: datetime = Field(default=datetime.now(UTC))

    class Config:
        json_encoders: ClassVar[dict] = {datetime: lambda v: v.isoformat()}


class ExperimentRun(BaseModel):
    """Model for a running experiment instance"""

    run_id: str
    experiment_id: str
    status: ExperimentStatus = ExperimentStatus.PENDING
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    current_step: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    results: Optional[dict[str, Any]] = None

    class Config:
        json_encoders: ClassVar[dict] = {datetime: lambda v: v.isoformat()}


class ExperimentResult(BaseModel):
    """Model for experiment results"""

    run_id: str
    experiment_id: str
    summary: str
    metrics: dict[str, float]
    visualizations: list[dict[str, Any]]
    recommendations: list[str]
    metadata: dict[str, Any] = {}
