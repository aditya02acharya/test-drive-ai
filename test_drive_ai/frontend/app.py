import streamlit as st

from test_drive_ai.frontend.components.dashboard import render_dashboard
from test_drive_ai.frontend.components.experiment_card import render_experiment_card
from test_drive_ai.frontend.components.status_tracker import render_status_tracker
from test_drive_ai.frontend.services.api_client import APIClient

st.set_page_config(
    page_title="Test Drive AI",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "selected_experiment" not in st.session_state:
    st.session_state.selected_experiment = None
if "current_run" not in st.session_state:
    st.session_state.current_run = None
if "show_results" not in st.session_state:
    st.session_state.show_results = False

api_client = APIClient()

st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #333;
        margin: 20px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-header">Test Drive AI</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.selected_experiment = None
        st.session_state.current_run = None
        st.session_state.show_results = False

    if st.session_state.selected_experiment:
        st.markdown("---")
        st.markdown("### Selected Experiment")
        st.markdown(f"**{st.session_state.selected_experiment['name']}**")

        if st.session_state.current_run:
            st.markdown(f"**Run ID:** {st.session_state.current_run['run_id'][:8]}...")

    st.markdown("---")
    st.markdown("### About")
    st.info(
        "This dashboard allows you to run and monitor experiments "
        "with real-time status updates and comprehensive result visualization."
    )

if not st.session_state.show_results:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="section-header">Select an Experiment</div>', unsafe_allow_html=True)

        # Fetch experiments
        experiments = api_client.get_experiments()

        if not experiments:
            st.warning("No experiments available. Please check the backend connection.")
        else:
            for experiment in experiments:
                is_selected = (
                    st.session_state.selected_experiment
                    and st.session_state.selected_experiment["id"] == experiment["id"]
                )

                if render_experiment_card(experiment, selected=is_selected):
                    st.session_state.selected_experiment = experiment
                    st.rerun()
    with col2:
        if st.session_state.selected_experiment:
            st.markdown('<div class="section-header">Experiment Details</div>', unsafe_allow_html=True)

            experiment = st.session_state.selected_experiment

            st.markdown("### Configuration")
            config = experiment["config"]
            st.json({
                "Parameters": config["parameters"],
            })

            st.markdown("### Actions")
            if st.button(
                "🚀 Run Experiment",
                use_container_width=True,
                type="primary",
                disabled=st.session_state.current_run is not None,
            ):
                # Start the experiment
                run = api_client.run_experiment(experiment["id"])
                if run:
                    st.session_state.current_run = run
                    st.rerun()

# Running experiment view
if st.session_state.current_run and not st.session_state.show_results:
    st.markdown('<div class="section-header">Experiment Progress</div>', unsafe_allow_html=True)

    # Create placeholder for status updates
    status_placeholder = st.empty()

    # Track experiment status
    final_status = render_status_tracker(api_client, st.session_state.current_run["run_id"], status_placeholder)

    # If experiment completed, fetch and show results
    if final_status and final_status.get("status") == "completed":
        results = api_client.get_run_results(st.session_state.current_run["run_id"])
        if results:
            st.session_state.results = results
            st.session_state.show_results = True
            st.rerun()

# Results view
if st.session_state.show_results and "results" in st.session_state:
    render_dashboard(st.session_state.results)

    # Option to run another experiment
    st.markdown("---")
    if st.button("🔄 Run Another Experiment", use_container_width=True):
        st.session_state.current_run = None
        st.session_state.show_results = False
        st.rerun()
