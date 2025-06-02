import asyncio
from datetime import UTC, datetime
from typing import Any, Callable

from test_drive_ai.backend.experiment_schema import ExperimentResult, ExperimentStatus


class SimulationService:
    """Service to handle experiment simulations"""

    @staticmethod
    async def run_experiment(
        experiment_id: str,
        run_id: str,
        config: dict[str, Any],
        status_callback: Callable[[str, ExperimentStatus, float, str], None],
    ) -> ExperimentResult:
        """
        Mock simulation of a long-running experiment

        Args:
            experiment_id: ID of the experiment
            config: Experiment configuration
            status_callback: Callback to update status

        Returns:
            ExperimentResult with mock data
        """

        # Simulation phases with progress percentages
        phases = [
            ("Initializing experiment environment", 10),
            ("Loading historical data", 20),
            ("Preprocessing customer segments", 30),
            ("Running intervention simulations", 50),
            ("Analyzing customer responses", 70),
            ("Calculating statistical significance", 85),
            ("Generating visualizations", 95),
            ("Finalizing results", 100),
        ]

        try:
            for phase, progress in phases:
                # Update status
                status_callback(run_id, ExperimentStatus.RUNNING, progress, phase)
                # Simulate processing time
                await asyncio.sleep(3.0)

            # Generate mock results
            results = SimulationService._generate_mock_results(experiment_id, run_id)

            status_callback(run_id, ExperimentStatus.COMPLETED, 100, "Experiment completed successfully")

            return results  # noqa: TRY300

        except Exception as e:
            status_callback(run_id, ExperimentStatus.FAILED, 0, f"Error: {e!s}")
            raise

    @staticmethod
    def _generate_mock_results(experiment_id: str, run_id: str) -> ExperimentResult:
        """Generate mock experiment results"""

        # Mock visualizations data
        visualizations = [
            {
                "type": "line_chart",
                "title": "Conversion Rate Over Time",
                "data": {
                    "x": ["Week 1", "Week 2", "Week 3", "Week 4"],
                    "y": [15.2, 18.5, 22.3, 25.8],
                    "xlabel": "Time Period",
                    "ylabel": "Conversion Rate (%)",
                },
            },
            {
                "type": "bar_chart",
                "title": "Intervention Effectiveness by Customer Segment",
                "data": {
                    "categories": ["Small Business", "Medium Business", "Enterprise"],
                    "control": [12.5, 15.3, 18.2],
                    "intervention_a": [18.7, 22.5, 24.8],
                    "intervention_b": [16.3, 19.8, 21.5],
                },
            },
            {
                "type": "heatmap",
                "title": "Customer Engagement by Industry and Size",
                "data": {
                    "rows": ["Retail", "Manufacturing", "Technology", "Healthcare"],
                    "columns": ["Small", "Medium", "Large"],
                    "values": [[0.82, 0.75, 0.68], [0.71, 0.83, 0.79], [0.88, 0.91, 0.85], [0.76, 0.80, 0.77]],
                },
            },
            {
                "type": "pie_chart",
                "title": "Portal Migration Status",
                "data": {"labels": ["Migrated", "In Progress", "Not Started", "Declined"], "values": [45, 25, 20, 10]},
            },
        ]

        return ExperimentResult(
            run_id=run_id,
            experiment_id=experiment_id,
            summary="""
            The experiment successfully tested three intervention strategies for encouraging
            business customers to migrate from the old portal to the new one. Intervention A
            (personalized onboarding with dedicated support) showed the highest conversion rate
            at 22.5%, compared to 15.3% for the control group. Statistical significance was
            achieved with p < 0.01. Small businesses responded particularly well to email
            campaigns, while enterprise customers preferred direct account manager outreach.
            """,
            metrics={
                "control_conversion_rate": 15.3,
                "intervention_a_conversion_rate": 22.5,
                "intervention_b_conversion_rate": 19.8,
                "statistical_significance": 0.008,
                "sample_size": 2500,
                "experiment_duration_days": 28,
                "cost_per_conversion_reduction": 32.5,
            },
            recommendations=[
                "Implement personalized onboarding for all new portal migrations",
                "Assign dedicated support staff for enterprise customers during transition",
                "Create segment-specific email campaigns targeting small businesses",
                "Develop video tutorials for the top 5 most-used features",
                "Schedule follow-up calls 7 days after initial migration invitation",
            ],
            visualizations=visualizations,
            metadata={"experiment_version": "1.0", "simulation_timestamp": datetime.now(UTC).isoformat()},
        )
