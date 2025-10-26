# Copyright (c) 2025 Mikheil Tabidze
import streamlit as st

st.set_page_config(page_icon="🛠", layout="wide")

homepage_page = st.Page(
    page="./pages/home_page.py", title="Home", icon=":material/home:", url_path="/", default=True
)
json_tools_page = st.Page(
    page="./pages/json_tools_page.py",
    title="JSON tools",
    icon=":material/data_object:",
    url_path="/json-tools",
)

pg = st.navigation(pages=[homepage_page, json_tools_page], position="sidebar", expanded=True)

pg.run()
