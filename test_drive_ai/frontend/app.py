import streamlit as st

from test_drive_ai.frontend.components.dashboard import render_dashboard
from test_drive_ai.frontend.components.experiment_card import render_experiment_card
from test_drive_ai.frontend.components.experiment_form import render_experiment_form
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
    /* Global Barclays Theme */
    :root {
        --barclays-blue: #00AEEF;
        --barclays-dark-blue: #0086BF;
        --barclays-light-blue: #E6F4FF;
        --barclays-text: #1a1a1a;
        --barclays-gray: #666666;
    }

    /* Main header styling */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
        padding: 20px 0;
        border-bottom: 3px solid var(--barclays-blue);
    }

    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .barclays-logo {
        height: 50px;
        width: auto;
    }

    .header-text {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--barclays-dark-blue);
        margin: 0;
    }

    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: var(--barclays-dark-blue);
        margin: 30px 0 20px 0;
        border-left: 4px solid var(--barclays-blue);
        padding-left: 15px;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    .sidebar-logo {
        height: 40px;
        width: auto;
        margin: 0 auto;
        display: block;
    }

    /* Button styling - fix red colors */
    .stButton > button {
        background-color: var(--barclays-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--barclays-dark-blue) !important;
        box-shadow: 0 4px 12px rgba(0, 134, 191, 0.3) !important;
        color: white !important;
    }

    .stButton > button:focus {
        background-color: var(--barclays-dark-blue) !important;
        color: white !important;
        box-shadow: 0 0 0 0.2rem rgba(0, 174, 239, 0.25) !important;
    }

    /* Info box styling */
    .stAlert {
        background-color: var(--barclays-light-blue);
        border-left: 4px solid var(--barclays-blue);
        color: var(--barclays-text);
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: var(--barclays-blue);
    }

    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    [data-testid="metric-container"] label {
        color: var(--barclays-gray);
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--barclays-dark-blue);
        font-weight: 700;
    }

    /* Responsive grid for cards */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    /* Back button alignment */
    .back-button-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }

    /* Override any default red colors */
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"],
    .stDownloadButton > button,
    button[type="submit"],
    .stFormSubmitButton > button {
        background-color: #00AEEF !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="secondary"]:hover,
    .stDownloadButton > button:hover,
    button[type="submit"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #0086BF !important;
        color: white !important;
    }

    /* Fix any red text on hover */
    a:hover, button:hover, [role="button"]:hover {
        color: #00AEEF !important;
    }

    /* Fix select/dropdown colors */
    .stSelectbox [data-baseweb="select"] [data-baseweb="menu"] [role="option"]:hover,
    .stMultiSelect [data-baseweb="menu"] [role="option"]:hover {
        background-color: #E6F4FF !important;
        color: #0086BF !important;
    }

    /* Remove any red error colors */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background-color: #FFF0F0;
        border-left-color: #E74C3C;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="main-header">
        <div class="logo-container">
            <img src="https://barcpensnw.org/wp-content/uploads/2015/11/barclays-eagle-logo.jpg" alt="Barclays Logo" class="barclays-logo">
            <h1 class="header-text">Test Drive AI</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    # Add Barclays logo to sidebar
    # Replace SIDEBAR_LOGO_URL_HERE with your actual Barclays logo URL
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://www.barclays.co.uk/content/dam/icons/favicons/barclays/Wordmark_RGB_Cyan_Large.svg" alt="Barclays" class="sidebar-logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        "This Barclays Test Drive AI dashboard allows you to run and monitor experiments "
        "with real-time status updates and comprehensive result visualization."
    )

# Main content area
if not st.session_state.show_results:
    # Experiment selection view
    if not st.session_state.selected_experiment:
        st.markdown('<div class="section-header">Select an Experiment</div>', unsafe_allow_html=True)

        # Fetch experiments
        experiments = api_client.get_experiments()

        if not experiments:
            st.warning("No experiments available. Please check the backend connection.")
        else:
            # Create responsive layout
            # Use single column layout for better mobile experience
            use_single_column = st.checkbox("Single column view", value=False, key="single_column_toggle")

            if use_single_column or len(experiments) == 1:
                # Single column layout
                for i, exp in enumerate(experiments):
                    if render_experiment_card(exp, selected=False, key_prefix=f"main_{i}_"):
                        st.session_state.selected_experiment = exp
                        st.rerun()
            else:
                # Two column layout for desktop
                cols = st.columns(2, gap="medium")
                for i, exp in enumerate(experiments):
                    with cols[i % 2]:
                        if render_experiment_card(exp, selected=False, key_prefix=f"main_{i}_"):
                            st.session_state.selected_experiment = exp
                            st.rerun()

    else:
        # Experiment configuration view
        exp = st.session_state.selected_experiment

        # Create properly aligned header with back button
        header_col1, header_col2 = st.columns([1, 11])

        with header_col1:
            if st.button("← Back", use_container_width=False):
                st.session_state.selected_experiment = None
                st.rerun()

        with header_col2:
            st.markdown(
                f'<div class="section-header" style="margin-top: 0;">{exp["name"]}</div>', unsafe_allow_html=True
            )

        # Show the configuration form
        form_data = render_experiment_form(exp)

        if form_data:
            # User submitted the form, run the experiment with custom parameters
            # Structure the parameters correctly
            custom_params = {}

            # Add all form fields directly to custom_params
            for key, value in form_data.items():
                custom_params[key] = value

            run = api_client.run_experiment(exp["id"], custom_params)
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
