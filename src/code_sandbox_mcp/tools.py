from code_sandbox_mcp.const import DEFAULT_ENVIRONMENT_MAP
from pydantic import Field
from typing import Annotated
from .utils import run_code

from mcp.types import TextContent
from llm_sandbox.data import ExecutionResult


def run_python_code(
    code: Annotated[
        str,
        Field(
            description=f"The Python code to execute, included libraries are {DEFAULT_ENVIRONMENT_MAP['python']['installed_libraries']}",
        ),
    ],
) -> TextContent:
    """Execute Python code in the sandbox environment and captures the standard output and error."""
    try:
        result = run_code(code, language="python")
        return TextContent(text=result.to_json(), type="text")
    except Exception as e:
        return [
            TextContent(
                text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text"
            )
        ]


def run_javascript_code(
    code: Annotated[
        str,
        Field(
            description=f"The JavaScript code to execute, included libraries are {DEFAULT_ENVIRONMENT_MAP['javascript']['installed_libraries']}",
        ),
    ],
) -> TextContent:
    """Execute JavaScript code in the sandbox environment and captures the standard output and error."""
    try:
        result = run_code(code, language="javascript")
        return TextContent(text=result.to_json(), type="text")
    except Exception as e:
        return [
            TextContent(
                text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text"
            )
        ]
