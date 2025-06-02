from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from test_drive_ai.backend.background_tasks import experiment_task_manager
from test_drive_ai.backend.config import settings
from test_drive_ai.backend.experiment_service import ExperimentService
from test_drive_ai.backend.router import router
from test_drive_ai.backend.simulation_service import SimulationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    app.state.experiment_service = ExperimentService()
    app.state.simulation_service = SimulationService()
    app.state.task_manager = experiment_task_manager

    print("Starting up experiment dashboard backend...")
    yield
    # Shutdown
    print("Shutting down experiment dashboard backend...")


app = FastAPI(
    title="Experiment Dashboard API",
    description="API for running and managing experiments",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Experiment Dashboard API", "version": "1.0.0", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
