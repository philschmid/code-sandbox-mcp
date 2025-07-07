import argparse
import json
from code_sandbox_mcp.const import DEFAULT_ENVIRONMENT_MAP
from fastmcp import FastMCP
from code_sandbox_mcp.const import DEFAULT_ENVIRONMENT_MAP
from pydantic import Field
from typing import Annotated
from .utils import run_code

from mcp.types import TextContent
from llm_sandbox.data import ExecutionResult

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="code-sandbox",
    instructions="This MCP server allows you to execute code in a secure sandbox environment and automatically capture visualizations.",
)


@mcp.tool()
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
        return TextContent(text=result, type="text")
    except Exception as e:
        result = ExecutionResult(exit_code=1, stderr=str(e)).to_json()
        return TextContent(text=result, type="text")


@mcp.tool()
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


@mcp.resource("sandbox://environments")
def environment_details() -> str:
    """Resource containing detailed information about the environments.

    Returns:
        str: The details of the languages

    """
    return json.dumps(DEFAULT_ENVIRONMENT_MAP, indent=2)


def main():
    # parser = argparse.ArgumentParser(description="Run Gemini MCP Server.")
    # parser.add_argument(
    #     "--env",
    #     help="Key value environment variables to set in the sandbox",
    #     default=None,
    #     type=str,
    #     nargs="+",
    #     action="append",
    #     metavar="KEY=VALUE",
    #     help="Set environment variables in the format KEY=VALUE",
    # )
    # args = parser.parse_args()

    # environment = {}
    # if args.env:
    #     for env_var in args.env:
    #         key, value = env_var.split("=")
    #         environment[key] = value

    mcp.run(
        transport="stdio",
    )


if __name__ == "__main__":
    main()
