import os
import uuid
from datetime import UTC, datetime
from typing import Any, Optional

import yaml

from test_drive_ai.backend.experiment_schema import (
    Experiment,
    ExperimentConfig,
    ExperimentResult,
    ExperimentRun,
    ExperimentStatus,
)


class ExperimentService:
    """Service to manage experiments"""

    def __init__(self):
        self.experiments: dict[str, Experiment] = {}
        self.active_runs: dict[str, ExperimentRun] = {}
        self.completed_results: dict[str, ExperimentResult] = {}
        self.load_experiments()

    def load_experiments(self) -> None:
        """Load experiments from YAML files"""
        experiments_dir = "data/experiments"

        # Mock experiments if directory doesn't exist
        if not os.path.exists(experiments_dir):
            self._create_mock_experiments()
            return

        for filename in os.listdir(experiments_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(experiments_dir, filename)
                with open(filepath) as f:
                    data = yaml.safe_load(f)
                    experiment = self._parse_experiment(data)
                    self.experiments[experiment.id] = experiment

    def _create_mock_experiments(self) -> None:
        """Create mock experiments for demo"""
        mock_experiments = [
            {
                "id": "bank-portal-migration",
                "name": "Bank Portal Migration Strategy",
                "description": "Test interventions to encourage business customers to migrate from old to new portal",
                "category": "Customer Migration",
                "tags": ["banking", "migration", "b2b"],
                "config": {
                    "name": "Portal Migration A/B Test",
                    "description": "Compare different intervention strategies",
                    "parameters": {
                        "segments": ["small_business", "medium_business", "enterprise"],
                        "interventions": ["control", "email_campaign", "personal_outreach", "incentive_based"],
                        "duration_days": 30,
                        "sample_size": 2500,
                    },
                    "estimated_duration": 15,
                },
            },
            {
                "id": "loan-approval-optimization",
                "name": "Loan Approval Process Optimization",
                "description": "Optimize loan approval rates while maintaining risk standards",
                "category": "Risk Management",
                "tags": ["loans", "risk", "optimization"],
                "config": {
                    "name": "Loan Approval ML Model Test",
                    "description": "Test new ML model against current approval process",
                    "parameters": {
                        "model_versions": ["current", "ml_v1", "ml_v2"],
                        "risk_categories": ["low", "medium", "high"],
                        "test_period_days": 60,
                        "sample_size": 5000,
                    },
                    "estimated_duration": 20,
                },
            },
            {
                "id": "customer-churn-prediction",
                "name": "Customer Churn Prevention",
                "description": "Identify and prevent high-value customer churn",
                "category": "Customer Retention",
                "tags": ["churn", "retention", "predictive"],
                "config": {
                    "name": "Churn Prevention Strategies",
                    "description": "Test different retention strategies for at-risk customers",
                    "parameters": {
                        "strategies": ["control", "proactive_support", "loyalty_rewards", "service_upgrade"],
                        "customer_tiers": ["bronze", "silver", "gold", "platinum"],
                        "intervention_timing": ["30_days", "60_days", "90_days"],
                        "sample_size": 3000,
                    },
                    "estimated_duration": 25,
                },
            },
        ]

        for exp_data in mock_experiments:
            experiment = self._parse_experiment(exp_data)
            self.experiments[experiment.id] = experiment

    def _parse_experiment(self, data: dict[str, Any]) -> Experiment:
        """Parse experiment data into Experiment model"""
        config = ExperimentConfig(**data["config"])
        return Experiment(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            tags=data.get("tags", []),
            config=config,
        )

    def get_all_experiments(self) -> list[Experiment]:
        """Get all available experiments"""
        return list(self.experiments.values())

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Get a specific experiment by ID"""
        return self.experiments.get(experiment_id)

    def create_experiment_run(self, experiment_id: str) -> ExperimentRun:
        """Create a new experiment run"""
        run = ExperimentRun(
            run_id=str(uuid.uuid4()),
            experiment_id=experiment_id,
            status=ExperimentStatus.PENDING,
            started_at=datetime.now(UTC),
        )
        self.active_runs[run.run_id] = run
        return run

    def update_run_status(
        self, run_id: str, status: ExperimentStatus, progress: float, current_step: str
    ) -> Optional[ExperimentRun]:
        """Update the status of an experiment run"""
        if run_id not in self.active_runs:
            return None

        self.active_runs[run_id].status = status
        self.active_runs[run_id].progress = progress
        self.active_runs[run_id].current_step = current_step

        if status == ExperimentStatus.COMPLETED:
            self.active_runs[run_id].completed_at = datetime.now(UTC)

        print("exp_service: ", self.active_runs[run_id])
        return self.active_runs[run_id]

    def get_run_status(self, run_id: str) -> Optional[ExperimentRun]:
        """Get the current status of an experiment run"""
        return self.active_runs.get(run_id)

    def save_results(self, results: ExperimentResult) -> None:
        """Save experiment results"""
        self.completed_results[results.run_id] = results

        # Mark run as completed
        if results.run_id in self.active_runs:
            run = self.active_runs[results.run_id]
            run.status = ExperimentStatus.COMPLETED
            run.progress = 100
            run.completed_at = datetime.now(UTC)

    def get_results(self, run_id: str) -> Optional[ExperimentResult]:
        """Get results for a completed experiment run"""
        return self.completed_results.get(run_id)
