""" Thank you, Daniel Jordan => jsontopydantic

https://github.com/brokenloop/jsontopydantic
"""
import os
import json
import requests
from typing import Dict, Union


def json_to_model(JSON: Union[Dict, str]) -> str:
    if JSON is None or JSON == "":
        return ""
    URL = "https://ufgjji253b.execute-api.us-east-1.amazonaws.com/prod"
    payload = {
        "data": json.dumps(JSON),
        "options": {
            "forceOptional": False,
            "snakeCased": True,
        },
    }
    response = requests.post(URL, json=payload)
    # Use datamodel-codegen instead of web service we don't control
    if not response.ok:
        raise Exception(f"Unable to parse JSON to model with API Request: {response.text}")
    model = response.json()["model"]
    return model


def write_model_to_file(model: str, file_path: str = "model.py") -> str:
    """Write the Pydantic Model string to a Python file.

    Args:
        model: The Pydantic Model string.
        file_path: The path must include the .py file extension.

    * The file_path is relative to the Workspace Root.

    Returns:
        The path to the Model Python file.
    """
    root = os.path.join(os.path.dirname(__file__), "../")
    fp = os.path.join(root, file_path)
    with open(fp, "w") as f:
        f.write(model)
    return fp
