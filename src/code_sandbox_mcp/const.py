import os
from typing import Literal


EXECUTION_TIMEOUT: int = 30
DEFAULT_BACKEND: str = os.getenv("BACKEND", "podman")
DEFAULT_LANGUAGE: Literal["python", "javascript", "go"] = "python"


DEFAULT_ENVIRONMENT_MAP = {
    "python": {
        "image": "philschmi/code-sandbox-python:latest",
        "installed_libraries": "numpy, pandas, matplotlib, scikit-learn, requests, google-genai",
    },
    "javascript": {
        "image": "philschmi/code-sandbox-js:latest",
        "installed_libraries": "@google/genai",
    },
    # "bash": {
    #     "image": "bash:latest",
    #     "installed_libraries": "",
    # },
    # "go": {
    #     "image": "golang:1.22",
    #     "installed_libraries": DEFAULT_GO_LIBRARIES,
    # },
}
