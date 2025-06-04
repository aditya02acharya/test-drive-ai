from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_dashboard(results: dict[str, Any]) -> None:
    """Render the dashboard with experiment results."""
    # Add Barclays-themed dashboard styling
    st.markdown(
        """
        <style>
        .dashboard-title {
            color: #0086BF;
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3 {
            color: #0086BF;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #00AEEF;
            padding-left: 12px;
        }

        .stInfo {
            background-color: #E6F4FF;
            border-left: 4px solid #00AEEF;
            border-radius: 4px;
        }

        .stMetric {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }

        .stMetric:hover {
            box-shadow: 0 4px 12px rgba(0, 134, 191, 0.15);
            transform: translateY(-2px);
        }

        .recommendations li {
            color: #1a1a1a;
            margin-bottom: 10px;
            padding-left: 20px;
        }

        .recommendations li::marker {
            color: #00AEEF;
        }

        .streamlit-expanderHeader {
            background-color: #f8f9fa !important;
            color: #0086BF !important;
        }

        .streamlit-expanderHeader:hover {
            color: #00AEEF !important;
        }

        button:hover, a:hover {
            color: #00AEEF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h2 class="dashboard-title">📊 Experiment Dashboard</h2>', unsafe_allow_html=True)

    # Summary section
    st.markdown("### Experiment Summary")
    st.info(results.get("summary", "No summary available."))

    # Metrics section
    st.markdown("### 🎯 Key Metrics")
    metrics = results.get("metrics", {})

    # Display metrics in columns
    metrics_cols = st.columns(len(metrics) if metrics else 1)
    for i, (metric_name, metric_value) in enumerate(metrics.items()):
        with metrics_cols[i % len(metrics_cols)]:
            st.metric(label=metric_name, value=metric_value)

    # Visualizations section
    st.markdown("### 📈 Visualizations")
    visualizations = results.get("visualizations", [])

    for viz in visualizations:
        _render_visualization(viz)

    st.markdown("### 💡 Recommendations")
    recommendations = results.get("recommendations", [])

    for i, recommendation in enumerate(recommendations):
        st.markdown(f"{i + 1}. {recommendation}")

    with st.expander("📋 Experiment Metadata"):
        metadata = results.get("metadata", {})
        st.json(metadata)


def _render_visualization(viz: dict[str, Any]) -> None:
    """Render a single visualization based on its type."""
    viz_type = viz.get("type")
    title = viz.get("title", "Visualization")
    data = viz.get("data", {})

    if viz_type == "line_chart":
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data.get("x", []),
                y=data.get("y", []),
                mode="lines+markers",
                name="Conversion Rate",
                line={"color": "#1f77b4", "width": 3},
                marker={"size": 8},
            )
        )
        fig.update_layout(
            title=title, xaxis_title=data.get("xlabel", "X"), yaxis_title=data.get("ylabel", "Y"), hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "bar_chart":
        categories = data.get("categories", [])
        control = data.get("control", [])
        intervention_a = data.get("intervention_a", [])
        intervention_b = data.get("intervention_b", [])

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control", x=categories, y=control))
        fig.add_trace(go.Bar(name="Intervention A", x=categories, y=intervention_a))
        fig.add_trace(go.Bar(name="Intervention B", x=categories, y=intervention_b))

        fig.update_layout(
            title=title, barmode="group", xaxis_title="Customer Segment", yaxis_title="Conversion Rate (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "heatmap":
        rows = data.get("rows", [])
        columns = data.get("columns", [])
        values = data.get("values", [])

        fig = go.Figure(
            data=go.Heatmap(
                z=values,
                x=columns,
                y=rows,
                colorscale="Blues",
                text=[[f"{val:.2f}" for val in row] for row in values],
                texttemplate="%{text}",
                textfont={"size": 12},
            )
        )

        fig.update_layout(title=title, xaxis_title="Company Size", yaxis_title="Industry")
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "pie_chart":
        labels = data.get("labels", [])
        values = data.get("values", [])

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels, values=values, hole=0.3, marker_colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
                )
            ]
        )

        fig.update_layout(title=title)
        st.plotly_chart(fig, use_container_width=True)
