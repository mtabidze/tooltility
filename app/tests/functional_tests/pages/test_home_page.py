# Copyright (c) 2025 Mikheil Tabidze
from streamlit.testing.v1 import AppTest


def test_home_page():
    app = AppTest.from_file(script_path="../../../src/pages/home_page.py")
    app.run()

    assert "Tooltility" in app.title[0].body, "Home page title should contain 'Tooltility'"
