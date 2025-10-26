# Copyright (c) 2025 Mikheil Tabidze
import json
from typing import Any

import pandas as pd
import yaml


def deserialize_json(input_text: str) -> Any:  # noqa: ANN401
    """
    Deserialize JSON.

    Args:
        input_text: The JSON string to deserialize.

    Returns:
        The deserialized JSON object.

    Raises:
        ValueError: If the JSON is invalid. Any exception from json.loads.

    """
    try:
        deserialized_object: Any = json.loads(s=input_text)
    except json.JSONDecodeError as exc:
        error_message = f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        raise ValueError(error_message) from None
    return deserialized_object


def format_json(
    input_text: str, *, indent_spaces: int | None = None, sort_keys: bool = False
) -> str:
    """
    Format JSON.

    Args:
        input_text: The JSON string to format.
        indent_spaces: The number of spaces to indent the JSON.
        sort_keys: Whether to sort the keys of the JSON object.

    Returns:
        The formatted JSON string.

    """
    deserialized_object: Any = deserialize_json(input_text=input_text)
    return json.dumps(
        obj=deserialized_object, indent=indent_spaces, sort_keys=sort_keys, ensure_ascii=False
    )


def convert_json_to_yaml(input_text: str) -> str:
    """
    Convert JSON to YAML.

    Args:
        input_text: The JSON string to convert.

    Returns:
        The converted YAML string.

    """
    deserialized_object: Any = deserialize_json(input_text=input_text)
    return yaml.dump(data=deserialized_object, sort_keys=False).removesuffix("...\n")


def convert_json_to_csv(input_text: str) -> str:
    """
    Convert JSON to CSV.

    Args:
        input_text: The JSON string to convert.

    Returns:
        The converted CSV string.

    Raises:
        ValueError: If the JSON is invalid.

    """
    deserialized_object: Any = deserialize_json(input_text=input_text)

    try:
        df = pd.DataFrame(data=deserialized_object)
        result: str = df.to_csv(index=False)
    except Exception:  # noqa: BLE001
        error_message = "Invalid JSON for CSV conversion"
        raise ValueError(error_message) from None
    return result
