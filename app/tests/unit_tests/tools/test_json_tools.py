# Copyright (c) 2025 Mikheil Tabidze
import pytest
from tools.json_tools import (
    convert_json_to_csv,
    convert_json_to_yaml,
    format_json,
    deserialize_json,
)


def test_deserialize_json():
    deserialized_object = deserialize_json(input_text='{"a": 1, "b": 2}')
    assert deserialized_object == {"a": 1, "b": 2}


def test_deserialize_json_exception_handling():
    with pytest.raises(ValueError):
        deserialize_json(input_text="invalid json")


@pytest.mark.parametrize(
    "input_text, indent_spaces, sort_keys, expected_output",
    (
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            None,
            False,
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
        ),
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            None,
            True,
            '{"a": 1, "b": 2, "c": 3, "d": [4, 5]}',
        ),
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            0,
            False,
            '{\n"a": 1,\n"c": 3,\n"b": 2,\n"d": [\n4,\n5\n]\n}',
        ),
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            0,
            True,
            '{\n"a": 1,\n"b": 2,\n"c": 3,\n"d": [\n4,\n5\n]\n}',
        ),
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            2,
            False,
            '{\n  "a": 1,\n  "c": 3,\n  "b": 2,\n  "d": [\n    4,\n    5\n  ]\n}',
        ),
        (
            '{"a": 1, "c": 3, "b": 2, "d": [4, 5]}',
            2,
            True,
            '{\n  "a": 1,\n  "b": 2,\n  "c": 3,\n  "d": [\n    4,\n    5\n  ]\n}',
        ),
    ),
)
def test_format_json(input_text, indent_spaces, sort_keys, expected_output):
    result = format_json(input_text=input_text, indent_spaces=indent_spaces, sort_keys=sort_keys)
    assert result == expected_output, f"Expected {expected_output}, got {result}"


@pytest.mark.parametrize(
    "input_text",
    (
        "0",
        "1.0",
        '"a"',
        "true",
        "false",
        "[]",
        "{}",
        "null",
        '{\n  "a": 1\n}',
        '{\n  "a": 1,\n  "b": 2\n}',
    ),
)
def test_format_json_no_change_needed(input_text):
    result = format_json(input_text=input_text, indent_spaces=2, sort_keys=True)
    assert result == input_text, f"Expected no change, got {result}"


@pytest.mark.parametrize(
    "input_text, expected_output",
    (
        ("0", "0\n"),
        ("1.0", "1.0\n"),
        ('"a"', "a\n"),
        ("true", "true\n"),
        ("false", "false\n"),
        ("[]", "[]\n"),
        ("{}", "{}\n"),
        ("null", "null\n"),
        ('{\n  "a": 1\n}', "a: 1\n"),
        ('{\n  "a": 1,\n  "b": 2\n}', "a: 1\nb: 2\n"),
        ('{"a": 1, "c": 3, "b": 2, "d": [4, 5]}', "a: 1\nc: 3\nb: 2\nd:\n- 4\n- 5\n"),
    ),
)
def test_convert_json_to_yaml(input_text, expected_output):
    result = convert_json_to_yaml(input_text=input_text)
    assert result == expected_output, f"Expected {expected_output}, got {result}"


def test_convert_json_to_csv():
    expected_output = "Model,Year\nCorolla,2024\nCamry,2025\n"
    result = convert_json_to_csv(
        input_text='[{"Model": "Corolla", "Year": 2024},{"Model": "Camry", "Year": 2025}]'
    )
    assert result == expected_output, f"Expected {expected_output}, got {result}"


def test_convert_json_to_csv_exception_handling():
    with pytest.raises(ValueError):
        convert_json_to_csv(input_text='{"Brand": "Toyota", "Model": "Corolla", "Year": 2020}')
