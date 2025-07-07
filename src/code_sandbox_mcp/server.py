import argparse
import json
from code_sandbox_mcp.const import DEFAULT_ENVIRONMENT_MAP
from fastmcp import FastMCP
import inspect
from gemini_mcp import tools
from fastmcp.tools import FunctionTool

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="code-sandbox",
    instructions="This MCP server allows you to execute code in a secure sandbox environment and automatically capture visualizations.",
)

# Dynamically add all async functions from the tools module
for name, func in inspect.getmembers(tools):
    if inspect.isasyncgenfunction(func) or inspect.iscoroutinefunction(func):
        if hasattr(func, "__module__") and func.__module__ == tools.__name__:
            mcp.add_tool(tool=FunctionTool.from_function(func, name=name))


@mcp.resource("sandbox://environments")
def environment_details() -> str:
    """Resource containing detailed information about the environments.

    Returns:
        str: The details of the languages

    """
    return json.dumps(DEFAULT_ENVIRONMENT_MAP, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Run Gemini MCP Server.")
    parser.add_argument(
        "--env",
        help="Key value environment variables to set in the sandbox",
        default=None,
        type=str,
        nargs="+",
        action="append",
        metavar="KEY=VALUE",
        help="Set environment variables in the format KEY=VALUE",
    )
    args = parser.parse_args()

    environment = {}
    if args.env:
        for env_var in args.env:
            key, value = env_var.split("=")
            environment[key] = value

    mcp.run(
        transport="stdio",
    )


if __name__ == "__main__":
    main()
