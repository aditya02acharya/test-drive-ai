# frontend/components/experiment_form.py
from typing import Any

import streamlit as st


def render_experiment_form(experiment: dict[str, Any]) -> dict[str, Any]:  # noqa: C901
    """
    Render a dynamic form based on experiment parameters

    Args:
        experiment: Experiment data with configuration

    Returns:
        Dict containing the form values
    """

    st.markdown("### ⚙️ Experiment Configuration")

    # Initialize form data in session state if not exists
    form_key = f"form_{experiment['id']}"
    if form_key not in st.session_state:
        st.session_state[form_key] = experiment["config"]["parameters"].copy()

    # Create form
    with st.form(key=f"experiment_form_{experiment['id']}"):
        # Display experiment info
        st.info(f"**{experiment['name']}**\n\n{experiment['config']['description']}")

        # Create dynamic form fields based on parameter types
        form_data = {}
        parameters = experiment["config"]["parameters"]

        # Organize parameters by type for better UI
        st.markdown("#### Parameters")

        for param_name, param_value in parameters.items():
            # Convert parameter name to readable format
            readable_name = param_name.replace("_", " ").title()

            # Determine input type based on value type and content
            if isinstance(param_value, bool):
                form_data[param_name] = st.checkbox(
                    readable_name,
                    value=st.session_state[form_key].get(param_name, param_value),
                    help=f"Enable/disable {readable_name.lower()}",
                )

            elif isinstance(param_value, int) and param_name.endswith(("days", "size", "count")):
                form_data[param_name] = st.number_input(
                    readable_name,
                    value=st.session_state[form_key].get(param_name, param_value),
                    min_value=1,
                    step=1,
                    help=f"Set {readable_name.lower()}",
                )

            elif isinstance(param_value, (int, float)):
                form_data[param_name] = st.number_input(
                    readable_name,
                    value=st.session_state[form_key].get(param_name, param_value),
                    help=f"Set {readable_name.lower()}",
                )

            elif isinstance(param_value, str):
                form_data[param_name] = st.text_input(
                    readable_name,
                    value=st.session_state[form_key].get(param_name, param_value),
                    help=f"Enter {readable_name.lower()}",
                )

            elif isinstance(param_value, list):
                if not param_value:  # Empty list
                    form_data[param_name] = []
                elif all(isinstance(item, str) for item in param_value):
                    # For list of strings, use multiselect
                    selected = st.multiselect(
                        readable_name,
                        options=param_value,
                        default=st.session_state[form_key].get(param_name, param_value),
                        help=f"Select {readable_name.lower()} to include",
                    )
                    form_data[param_name] = selected

                elif all(isinstance(item, dict) for item in param_value):
                    # For list of dicts (like interventions with name/description)
                    st.markdown(f"**{readable_name}**")
                    selected_items = []

                    for i, item in enumerate(param_value):
                        if isinstance(item, dict) and "name" in item:
                            # Checkbox for each intervention
                            include = st.checkbox(
                                f"{item.get('name')} - {item.get('description', '')}",
                                value=True,
                                key=f"{param_name}_{i}_include",
                            )
                            if include:
                                selected_items.append(item.get("name"))
                        else:
                            selected_items.append(item)

                    form_data[param_name] = selected_items if selected_items else param_value
                else:
                    # For other list types, convert to multiselect
                    form_data[param_name] = st.multiselect(
                        readable_name, options=param_value, default=param_value, help=f"Select {readable_name.lower()}"
                    )

            elif isinstance(param_value, dict):
                # For nested dictionaries, create an expandable section
                with st.expander(f"{readable_name} (Advanced)"):
                    nested_data = {}
                    for nested_key, nested_value in param_value.items():
                        nested_name = nested_key.replace("_", " ").title()
                        if isinstance(nested_value, (str, int, float)):
                            nested_data[nested_key] = st.text_input(
                                nested_name,
                                value=str(st.session_state[form_key].get(param_name, {}).get(nested_key, nested_value)),
                                key=f"{param_name}_{nested_key}",
                            )
                    form_data[param_name] = nested_data

        # Additional information section
        st.markdown("#### Additional Information")

        col1, col2 = st.columns(2)

        with col1:
            form_data["additional_context"] = st.text_area(
                "Context & Background",
                placeholder="Provide any additional context about your business, customers, or specific requirements...",
                height=120,
                help="This information will help tailor the experiment to your specific needs",
            )

        with col2:
            form_data["success_criteria"] = st.text_area(
                "Success Criteria",
                placeholder="Define what success looks like for this experiment...",
                height=120,
                help="Specify your goals and KPIs",
            )

        # Portal-specific information (if this is a portal migration experiment)
        if "portal" in experiment["id"].lower() or "migration" in experiment["name"].lower():
            st.markdown("#### Portal Information")

            col1, col2 = st.columns(2)

            with col1:
                form_data["old_portal_info"] = st.text_area(
                    "Old Portal Details",
                    placeholder="Describe the current portal (features, pain points, usage patterns)...",
                    height=100,
                    help="Information about the existing portal",
                )

            with col2:
                form_data["new_portal_info"] = st.text_area(
                    "New Portal Details",
                    placeholder="Describe the new portal (improvements, new features, benefits)...",
                    height=100,
                    help="Information about the new portal",
                )

        # Advanced options
        with st.expander("Advanced Options"):
            form_data["random_seed"] = st.number_input(
                "Random Seed", value=42, help="Set a seed for reproducible results"
            )

            form_data["confidence_level"] = st.slider(
                "Statistical Confidence Level",
                min_value=0.90,
                max_value=0.99,
                value=0.95,
                step=0.01,
                format="%.2f",
                help="Confidence level for statistical tests",
            )

        # Submit button
        submitted = st.form_submit_button(
            "🚀 Run Experiment with Custom Parameters", type="primary", use_container_width=True
        )

        if submitted:
            # Update session state
            st.session_state[form_key] = form_data
            return form_data

    return None
