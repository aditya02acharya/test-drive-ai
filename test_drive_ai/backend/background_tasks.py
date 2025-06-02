import asyncio
from typing import Any

from test_drive_ai.backend.experiment_schema import ExperimentStatus


class ExperimentTaskManager:
    """Manager for background experiment tasks"""

    def __init__(self):
        self.running_tasks: dict[str, asyncio.Task] = {}

    async def run_experiment(
        self,
        experiment_id: str,
        run_id: str,
        config: dict[str, Any],
        experiment_service,
        simulation_service,
    ):
        """Run an experiment in the background"""

        def status_callback(run_id: str, status: ExperimentStatus, progress: float, current_step: str):
            """Callback to update experiment status"""
            print(f"Updating status for run {run_id}: {status}, progress: {progress}, step: {current_step}")
            run = experiment_service.update_run_status(run_id, status, progress, current_step)
            print(f"Status updated for run {run_id} - {run}")

        try:
            print(f"Starting experiment {experiment_id} with run ID {run_id}")
            # Update initial status
            status_callback(run_id, ExperimentStatus.INITIALIZING, 0, "Starting experiment")
            print("Experiment initialization done")

            # Run the simulation
            print(f"Running experiment {experiment_id} with config: {config}")
            results = await simulation_service.run_experiment(experiment_id, run_id, config, status_callback)

            # Save results
            experiment_service.save_results(results)

        except Exception as e:
            # Handle errors
            status_callback(run_id, ExperimentStatus.FAILED, 0, f"Error: {e!s}")
            raise

        finally:
            # Clean up
            if run_id in self.running_tasks:
                del self.running_tasks[run_id]

    def cancel_experiment(self, run_id: str) -> bool:
        """Cancel a running experiment"""
        if run_id in self.running_tasks:
            task = self.running_tasks[run_id]
            task.cancel()
            del self.running_tasks[run_id]
            return True
        return False


# Global instance
experiment_task_manager = ExperimentTaskManager()
