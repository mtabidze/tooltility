# Copyright (c) 2025 Mikheil Tabidze
from streamlit.testing.v1 import AppTest


def test_streamlit_app():
    app = AppTest.from_file(script_path="../../src/streamlit_app.py")
    app.run()

    assert "Tooltility" in app.title[0].body, "Default page should be the home page"
