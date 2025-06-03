from typing import Any

import streamlit as st


def render_experiment_card(experiment: dict[str, Any], selected: bool = False, key_prefix: str = "") -> bool:
    """
    Render a clickable experiment card with information

    Args:
        experiment: Experiment data
        selected: Whether this experiment is currently selected
        key_prefix: Prefix for unique keys

    Returns:
        bool: True if the card was clicked
    """

    # Create container with custom styling
    with st.container():
        # Add custom CSS for better card appearance
        st.markdown(
            """
        <style>
        div.row-widget.stButton > button {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            width: 100%;
            text-align: left;
            transition: all 0.3s ease;
            min-height: 150px;
        }
        div.row-widget.stButton > button:hover {
            border-color: #1f77b4;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
            background-color: #f8fbff;
        }
        div.row-widget.stButton > button:active {
            transform: translateY(0);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Create formatted button content
        tags_html = " ".join([f"#{tag}" for tag in experiment.get("tags", [])])

        button_content = f"""
{experiment["category"]}

**{experiment["name"]}**

{experiment["description"]}

{tags_html}
        """

        # Create clickable card button
        if st.button(
            button_content,
            key=f"{key_prefix}card_{experiment['id']}",
            help="Click to configure and run this experiment",
        ):
            return True

    return False
