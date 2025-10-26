# Copyright (c) 2025 Mikheil Tabidze
from streamlit.testing.v1 import AppTest


def test_json_tool_page():
    app = AppTest.from_file(script_path="../../../src/pages/json_tools_page.py")
    app.run()

    assert "JSON tools" in app.title[0].body, "JSON tools page title should contain 'JSON tools'"
