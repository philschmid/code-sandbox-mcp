from unittest.mock import MagicMock
from code_sandbox_mcp.server import mcp, main
import os
import pytest
from fastmcp import Client


@pytest.mark.asyncio
async def test_tools_added():
    # Check if the tools from the tools module are added to the mcp instance
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        assert "run_python_code" in tool_names
        assert "run_javascript_code" in tool_names
