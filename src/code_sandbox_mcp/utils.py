import json
import logging
import os
from typing import Literal

from code_sandbox_mcp.const import DEFAULT_BACKEND, DEFAULT_LANGUAGE, EXECUTION_TIMEOUT
from llm_sandbox import (
    SandboxBackend,
    SandboxSession,
)
from llm_sandbox.session import _check_dependency


def _get_backend() -> SandboxBackend:
    """Get the backend to use for the sandbox session."""
    backend = SandboxBackend(os.environ.get("BACKEND", "podman"))
    _check_dependency(backend)
    return backend


def run_code(
    code: str,
    language: Literal["python", "javascript"] = DEFAULT_LANGUAGE,
    image: str = None,
    libraries: list[str] | None = None,
    timeout: int = EXECUTION_TIMEOUT,
    environment: dict[str, str] = {},
) -> str:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, go)
        libraries: List of libraries/packages to install
        image: Docker image to use for the sandbox session
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    session_args = {
        "lang": language,
        "keep_template": True,
        "verbose": False,
        "backend": _get_backend(),
        "session_timeout": timeout,
    }

    if environment:
        session_args["runtime_config"] = {"environment": environment}

    if image:
        session_args["image"] = image

    if libraries:
        session_args["libraries"] = libraries

    with SandboxSession(**session_args) as session:
        result = session.run(
            code=code,
            libraries=libraries or [],
            timeout=timeout,
        )
    return result
