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


def test_main_stdio(mocker):
    # Mock argparse to return stdio transport
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_parser = MagicMock()
    mock_parser.parse_args.return_value = mock_args
    mocker.patch(
        "code_sandbox_mcp.server.argparse.ArgumentParser", return_value=mock_parser
    )
    mock_run = mocker.patch("code_sandbox_mcp.server.mcp.run")

    # Call main
    main()

    # Assertions
    mock_run.assert_called_once_with(transport="stdio")
    assert os.environ.get("MCP_TRANSPORT_MODE") == "stdio"
