from typing import Any

import streamlit as st


def render_experiment_card(experiment: dict[str, Any], selected: bool = False) -> bool:
    """Render a card for an experiment."""
    card_style = """
    <style>
    .experiment-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .experiment-card:hover {
        box-color: #1f77b4;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .experiment-card.selected {
        border-color: #1f77b4;
        background-color: #f0f8ff;
    }
    .experiment-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
        marin-bottom: 8px;
    }
    .experiment-category {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-bottom: 8px;
    }
    .experiment-description {
        color: #666;
        margin-bottom: 12px;
    }
    .experiment-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 12px;
    }
    .experiment-tag {
        background-color: #e0e0e0;
        color: #333;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
    }
    .experiment-meta {
        display: flex;
        justify-content: space-between;
        color: #999;
        font-size: 0.9em;
    }
    </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    # card container
    col1, col2 = st.columns([1, 20])

    with col2:
        card_class = "experiment-card selected" if selected else "experiment-card"

        card_html = f"""
        <div class="{card_class}">
            <div class="experiment-category">{experiment["category"]}</div>
            <div class="experiment-title">{experiment["name"]}</div>
            <div class="experiment-description">{experiment["description"]}</div>
            <div class="experiment-tags">
                {"".join([f'<span class="experiment-tag">{tag}</span>' for tag in experiment.get("tags", [])])}
            </div>
        </div>
        """
        clicked = st.button(
            "Run experiment",
            key=f"select_{experiment['id']}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        )
        st.markdown(card_html, unsafe_allow_html=True)

        return clicked
