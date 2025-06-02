import json
from typing import Any, Optional

import requests
import streamlit as st
from sseclient import SSEClient


class APIClient:
    """A client for interacting with the Test Drive AI API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_experiments(self) -> list[dict[str, Any]]:
        try:
            response = self.session.get(f"{self.base_url}/experiments/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Failed to fetch experiments: {e!s}")
            return []

    def get_experiment(self, experiment_id: str) -> Optional[dict[str, Any]]:
        """Fetch a specific experiment"""
        try:
            response = self.session.get(f"{self.base_url}/experiments/{experiment_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch experiment: {e!s}")
            return None

    def run_experiment(self, experiment_id: str) -> Optional[dict[str, Any]]:
        """Start running an experiment"""
        try:
            response = self.session.post(f"{self.base_url}/experiments/{experiment_id}/run")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to start experiment: {e!s}")
            return None

    def get_run_status(self, run_id: str) -> Optional[dict[str, Any]]:
        """Get the status of an experiment run"""
        try:
            response = self.session.get(f"{self.base_url}/experiments/run/{run_id}/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch run status: {e!s}")
            return None

    def stream_run_status(self, run_id: str):
        """Stream real-time status updates using SSE"""
        print(f"Starting to stream status updates for run ID: {run_id}")
        try:
            response = self.session.get(
                f"{self.base_url}/experiments/run/{run_id}/stream", stream=True, headers={"Accept": "text/event-stream"}
            )
            response.raise_for_status()

            client = SSEClient(response)
            for event in client.events():
                print(event.event, event.data)
                if event.event == "update":
                    yield json.loads(event.data)
                elif event.event == "complete":
                    yield json.loads(event.data)
                    break
                elif event.event == "error":
                    error_data = json.loads(event.data)
                    st.error(f"Error: {error_data.get('message', 'Unknown error')}")
                    break
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to stream status updates: {e!s}")

    def get_run_results(self, run_id: str) -> Optional[dict[str, Any]]:
        """Get the results of a completed experiment run"""
        try:
            response = self.session.get(f"{self.base_url}/experiments/run/{run_id}/results")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch results: {e!s}")
            return None
