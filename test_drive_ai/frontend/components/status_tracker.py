import time
from typing import Any, Optional

import streamlit as st


def render_status_tracker(
    api_client,
    run_id: str,
    placeholder: Any,
) -> Optional[dict[str, Any]]:
    """Render a status tracker for an experiment run."""
    status_style = """
    <style>
    .status-container {
        border: 2px solid #00AEEF;
        border-radius: 10px;
        padding: 24px;
        margin: 20px 0;
        background-color: #f8fcff;
        box-shadow: 0 4px 12px rgba(0, 174, 239, 0.1);
    }
    .status-header {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 15px;
        color: #0086BF;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .status-step {
        font-size: 1.1em;
        color: #666666;
        margin: 15px 0;
        padding: 10px;
        background-color: white;
        border-radius: 6px;
        border-left: 4px solid #00AEEF;
    }
    .status-icon {
        display: inline-block;
        margin-right: 10px;
        font-size: 1.2em;
    }
    .stProgress > div > div > div > div {
        background-color: #00AEEF !important;
    }
    .status-info {
        color: #1a1a1a;
        font-weight: 500;
        margin-top: 10px;
    }

    [data-testid="stProgress"] > div {
        background-color: #e0e0e0;
    }
    [data-testid="stProgress"] > div > div {
        background-color: #00AEEF !important;
    }
    </style>
    """
    last_status = None

    # Stream status updates
    for update in api_client.stream_run_status(run_id):
        with placeholder.container():
            st.markdown(status_style, unsafe_allow_html=True)

            # Handle different event types
            if "status" in update:
                status = update.get("status", "unknown")
                progress = update.get("progress", 0)
                current_step = update.get("current_step", "Processing...")

                status_icon = _get_status_icon(status)
                st.markdown(
                    f"<div class='status-container'>"
                    f"<div class='status-header'>"
                    f"<span class='status-icon'>{status_icon}</span>"
                    f"Experiment Status: {status.upper()}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # Progress bar
                st.progress(progress / 100.0)

                # Current step
                st.markdown(f"<div class='status-step'>Current Step: {current_step}</div>", unsafe_allow_html=True)

                # Additional information
                if update.get("started_at"):
                    st.markdown(f"**Started at:** {update['started_at']}")

                if status == "completed" and update.get("completed_at"):
                    st.markdown(f"**Completed at:** {update['completed_at']}")

                st.markdown("</div>", unsafe_allow_html=True)

                last_status = update

            elif "status" in update and update["status"] in ["completed", "failed"]:
                return last_status

        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    return last_status


def _get_status_icon(status: str) -> str:
    """Return an HTML icon based on the status."""
    icons = {
        "initialising": "🔄",
        "completed": "✅",
        "failed": "❌",
        "pending": "⏳",
        "running": "▶️",
        "analysing": "🔍",
    }
    return icons.get(status.lower(), "❓")
