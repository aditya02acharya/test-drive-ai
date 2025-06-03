import asyncio
import json
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from test_drive_ai.backend.experiment_schema import (
    Experiment,
    ExperimentResult,
    ExperimentRun,
    ExperimentRunRequest,
    ExperimentStatus,
)

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("/", response_model=list[Experiment])
async def get_experiments(request: Request):
    """Get all available experiments"""
    experiment_service = request.app.state.experiment_service
    return experiment_service.get_all_experiments()


@router.get("/{experiment_id}", response_model=Experiment)
async def get_experiment(experiment_id: str, request: Request):
    """Get a specific experiment by ID"""
    experiment_service = request.app.state.experiment_service
    experiment = experiment_service.get_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.post("/{experiment_id}/run", response_model=ExperimentRun)
async def run_experiment(
    experiment_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    run_request: Optional[ExperimentRunRequest] = None,
):
    """Start running an experiment with optional custom parameters"""
    experiment_service = request.app.state.experiment_service
    simulation_service = request.app.state.simulation_service
    task_manager = request.app.state.task_manager

    experiment = experiment_service.get_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Extract custom parameters if provided
    custom_params = None
    if run_request and run_request.custom_parameters:
        custom_params = run_request.custom_parameters

    # Create a new run with custom parameters
    run = experiment_service.create_experiment_run(experiment_id, custom_params)

    # Merge custom parameters with default config
    config = experiment.config.dict()
    if custom_params:
        # Create a deep copy to avoid modifying the original
        import copy

        config = copy.deepcopy(config)

        # Update only the parameters that exist in the original config
        for key, value in custom_params.items():
            if key in config["parameters"] and key != "parameters":
                # Handle special cases like interventions
                if key == "interventions" and isinstance(config["parameters"][key], list):
                    # If original interventions were list of dicts, extract names
                    if config["parameters"][key] and isinstance(config["parameters"][key][0], dict):
                        # Keep the dict structure but filter based on selected names
                        original_interventions = config["parameters"][key]
                        if isinstance(value, list) and all(isinstance(v, str) for v in value):
                            # Filter original interventions by selected names
                            config["parameters"][key] = [
                                inter for inter in original_interventions if inter.get("name") in value
                            ]
                        else:
                            config["parameters"][key] = value
                    else:
                        config["parameters"][key] = value
                else:
                    config["parameters"][key] = value

        # Add custom context fields
        config["custom_context"] = {
            "additional_context": custom_params.get("additional_context", ""),
            "success_criteria": custom_params.get("success_criteria", ""),
            "old_portal_info": custom_params.get("old_portal_info", ""),
            "new_portal_info": custom_params.get("new_portal_info", ""),
            "random_seed": custom_params.get("random_seed", 42),
            "confidence_level": custom_params.get("confidence_level", 0.95),
        }

    # Start the experiment in background
    background_tasks.add_task(
        task_manager.run_experiment, experiment_id, run.run_id, config, experiment_service, simulation_service
    )

    return run


@router.get("/run/{run_id}/status", response_model=ExperimentRun)
async def get_run_status(run_id: str, request: Request):
    """Get the status of an experiment run"""
    experiment_service = request.app.state.experiment_service
    run = experiment_service.get_run_status(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/run/{run_id}/stream")
async def stream_run_status(run_id: str, request: Request):
    """Stream real-time status updates for an experiment run using SSE"""
    experiment_service = request.app.state.experiment_service

    async def event_generator():
        """Generate server-sent events"""
        previous_state = None
        error_count = 0
        max_errors = 5

        while error_count < max_errors:
            try:
                run = experiment_service.get_run_status(run_id)
                print(f"Checking status for run ID: {run_id} - Current Status: {run.status if run else 'None'}")

                if not run:
                    yield {"event": "error", "data": json.dumps({"message": "Run not found"})}
                    break

                # Create a state tuple for comparison
                current_state = (run.status, run.progress, run.current_step)

                # Send update if state changed
                if current_state != previous_state:
                    data = {
                        "run_id": run.run_id,
                        "status": run.status,
                        "progress": run.progress,
                        "current_step": run.current_step,
                        "started_at": run.started_at.isoformat() if run.started_at else None,
                        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                    }

                    # Debug log
                    print(f"SSE Update: Status={run.status}, Progress={run.progress}%, Step={run.current_step}")

                    yield {"event": "update", "data": json.dumps(data)}

                    previous_state = current_state

                # Check if experiment is complete
                if run.status in [ExperimentStatus.COMPLETED, ExperimentStatus.FAILED]:
                    yield {"event": "complete", "data": json.dumps({"status": run.status})}
                    break

                # Wait before next check
                await asyncio.sleep(0.5)

            except Exception as e:
                error_count += 1
                yield {"event": "error", "data": json.dumps({"message": str(e)})}
                await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


@router.get("/run/{run_id}/results", response_model=ExperimentResult)
async def get_run_results(run_id: str, request: Request):
    """Get the results of a completed experiment run"""
    experiment_service = request.app.state.experiment_service
    results = experiment_service.get_results(run_id)
    if not results:
        raise HTTPException(status_code=404, detail="Results not found")
    return results
