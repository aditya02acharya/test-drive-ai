import asyncio
import json

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from test_drive_ai.backend.experiment_schema import Experiment, ExperimentResult, ExperimentRun, ExperimentStatus

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
async def run_experiment(experiment_id: str, request: Request, background_tasks: BackgroundTasks):
    """Start running an experiment"""
    experiment_service = request.app.state.experiment_service
    simulation_service = request.app.state.simulation_service
    task_manager = request.app.state.task_manager

    experiment = experiment_service.get_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Create a new run
    run = experiment_service.create_experiment_run(experiment_id)

    # Start the experiment in background
    background_tasks.add_task(
        task_manager.run_experiment,
        experiment_id,
        run.run_id,
        experiment.config.dict(),
        experiment_service,
        simulation_service,
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
