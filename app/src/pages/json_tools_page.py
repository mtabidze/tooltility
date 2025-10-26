# Copyright (c) 2025 Mikheil Tabidze
from datetime import UTC, datetime

import streamlit as st
from tools.json_tools import convert_json_to_csv, convert_json_to_yaml, format_json

st.title("JSON tools")
st.caption("JSON tools are a collection of tools for working with JSON data.")


format_tab, convert_tab = st.tabs(["Format", "Convert"])
with format_tab:
    if "json_format_result" not in st.session_state:
        st.session_state["json_format_result"] = None
        st.session_state["json_format_file_name"] = None

    with st.form(key="json_format_form"):
        input_text = st.text_area(
            label="JSON input", placeholder="Paste your JSON here...", height=180
        )
        indent_spaces = st.slider(label="Indent", min_value=2, max_value=8, value=2, step=1)
        sort_keys = st.checkbox(label="Sort keys")
        format_submitted = st.form_submit_button(label="Format")

    if format_submitted:
        if not input_text.strip():
            st.warning("Please paste JSON to format.")
        else:
            try:
                formatted_json_str = format_json(
                    input_text,
                    indent_spaces=indent_spaces,
                    sort_keys=sort_keys,
                )
                st.session_state["json_format_result"] = formatted_json_str
                st.session_state["json_format_file_name"] = (
                    f"formatted_{int(datetime.now(tz=UTC).timestamp())}.json"
                )
            except ValueError as e:
                st.error(str(e))
                st.session_state["json_format_result"] = None
                st.session_state["json_format_file_name"] = None

    if st.session_state.get("json_format_result"):
        st.success("Formatted successfully")
        st.code(
            body=st.session_state["json_format_result"],
            language="json",
            line_numbers=True,
            height=450,
        )
        st.download_button(
            label="Download formatted JSON",
            data=st.session_state["json_format_result"],
            file_name=st.session_state.get("json_format_file_name") or "formatted.json",
            mime="application/json",
        )

with convert_tab:
    if "json_convert_result" not in st.session_state:
        st.session_state["json_convert_result"] = None
        st.session_state["json_convert_file_name"] = None

    with st.form(key="json_convert_form"):
        input_text = st.text_area(
            label="JSON input", placeholder="Paste your JSON here...", height=180
        )
        extension = st.radio(label="To", options=["YAML", "CSV"], horizontal=True)
        convert_submitted = st.form_submit_button(label="Convert")

    if convert_submitted:
        if not input_text.strip():
            st.warning("Please paste JSON to convert.")
        else:
            try:
                if extension == "YAML":
                    converted_json_str = convert_json_to_yaml(input_text=input_text)
                elif extension == "CSV":
                    converted_json_str = convert_json_to_csv(input_text=input_text)
                st.session_state["json_convert_result"] = converted_json_str
                st.session_state["json_convert_file_name"] = (
                    f"converted_{int(datetime.now(tz=UTC).timestamp())}.{extension.lower()}"
                )
            except ValueError as e:
                st.error(str(e))
                st.session_state["json_convert_result"] = None
                st.session_state["json_convert_file_name"] = None

    if st.session_state.get("json_convert_result"):
        st.success("Converted successfully")
        st.code(
            body=st.session_state["json_convert_result"],
            language=extension.lower(),
            line_numbers=True,
            height=450,
        )
        st.download_button(
            label="Download converted file",
            data=st.session_state["json_convert_result"],
            file_name=st.session_state.get("json_convert_file_name")
            or f"converted.{extension.lower()}",
        )
