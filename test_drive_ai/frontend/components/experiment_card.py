from typing import Any

import streamlit as st


def render_experiment_card(experiment: dict[str, Any], selected: bool = False, key_prefix: str = "") -> bool:
    """
    Render a clickable experiment card with Barclays branding

    Args:
        experiment: Experiment data
        selected: Whether this experiment is currently selected
        key_prefix: Prefix for unique keys

    Returns:
        bool: True if the card was clicked
    """

    # Create container with custom styling
    with st.container():
        # Add custom CSS for Barclays-themed card appearance
        st.markdown(
            """
        <style>
        .experiment-card {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
            min-height: 180px;
            position: relative;
        }
        .experiment-card:hover {
            border-color: #00AEEF;
            box-shadow: 0 8px 20px rgba(0, 174, 239, 0.15);
            transform: translateY(-3px);
            background-color: #f8fcff;
        }
        .experiment-category {
            color: #00AEEF;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .experiment-title {
            color: #1a1a1a;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 12px;
            line-height: 1.2;
        }
        .experiment-description {
            color: #666666;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        .experiment-tags {
            margin-bottom: 20px;
        }
        .experiment-tag {
            display: inline-block;
            background-color: #f0f8ff;
            color: #0086BF;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        .select-button {
            background-color: #00AEEF;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            float: right;
            margin-top: 8px;
        }
        .select-button:hover {
            background-color: #0086BF;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 134, 191, 0.3);
        }
        div.stButton > button {
            background-color: #00AEEF;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #0086BF;
            box-shadow: 0 4px 12px rgba(0, 134, 191, 0.3);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Create card container
        card_html = f"""
        <div class="experiment-card">
            <div class="experiment-category">{experiment["category"]}</div>
            <div class="experiment-title">{experiment["name"]}</div>
            <div class="experiment-description">{experiment["description"]}</div>
            <div class="experiment-tags">
                {"".join([f'<span class="experiment-tag">#{tag}</span>' for tag in experiment.get("tags", [])])}
            </div>
        </div>
        """

        st.markdown(card_html, unsafe_allow_html=True)

        # Add Select button at the bottom of the card
        col1, col2, col3 = st.columns([3, 1, 0.5])
        with col2:
            if st.button(
                "Select",
                key=f"{key_prefix}select_{experiment['id']}",
                help="Click to configure and run this experiment",
            ):
                return True

    return False
