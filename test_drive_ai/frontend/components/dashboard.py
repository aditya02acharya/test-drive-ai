from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_dashboard(results: dict[str, Any]) -> None:
    """Render the dashboard with experiment results."""
    st.title("## 📊 Experiment Dashboard")

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
