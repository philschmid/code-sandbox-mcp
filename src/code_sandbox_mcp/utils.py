import os
from typing import Literal

from code_sandbox_mcp.const import (
    DEFAULT_BACKEND,
    DEFAULT_ENVIRONMENT_MAP,
    DEFAULT_LANGUAGE,
    EXECUTION_TIMEOUT,
    VERBOSE,
)
from llm_sandbox import (
    SandboxBackend,
    SandboxSession,
)
from llm_sandbox.session import _check_dependency


def _get_backend() -> SandboxBackend:
    """Get the backend to use for the sandbox session."""
    backend = SandboxBackend(DEFAULT_BACKEND)
    _check_dependency(backend)
    return backend


def run_code(
    code: str,
    language: Literal["python", "javascript"] = DEFAULT_LANGUAGE,
    image: str | None = None,
    libraries: list[str] | None = None,
    timeout: int = EXECUTION_TIMEOUT,
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
    if language not in DEFAULT_ENVIRONMENT_MAP:
        raise ValueError(f"Language {language} not supported")

    session_args = {
        "lang": language,
        "keep_template": True,
        "verbose": VERBOSE,
        "backend": _get_backend(),
        "session_timeout": timeout,
        "image": DEFAULT_ENVIRONMENT_MAP[language]["image"],
    }

    if os.getenv("PASSTHROUGH_ENV", None):
        env_vars = {}
        for var in os.getenv("PASSTHROUGH_ENV", None).split(","):
            env_vars[var] = os.getenv(var)
        session_args["runtime_configs"] = {"environment": env_vars}

    if os.getenv("CONTAINER_IMAGE", None) and os.getenv("CONTAINER_LANGUAGE", None):
        session_args["lang"] = os.getenv("CONTAINER_LANGUAGE")
        session_args["image"] = os.getenv("CONTAINER_IMAGE")

    if libraries:
        session_args["libraries"] = libraries

    with SandboxSession(**session_args) as session:
        result = session.run(
            code=code,
            libraries=libraries or [],
            timeout=timeout,
        )
    if result.exit_code != 0:
        raise Exception(result.stderr.strip())
    return result.stdout.strip()
