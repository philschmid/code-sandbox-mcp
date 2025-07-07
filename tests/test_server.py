from unittest.mock import MagicMock
from gemini_mcp.server import mcp, main
import os
import pytest
from fastmcp import Client


@pytest.mark.asyncio
async def test_tools_added():
    # Check if the tools from the tools module are added to the mcp instance
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        assert "web_search" in tool_names
        assert "use_gemini" in tool_names


def test_main_stdio(mocker):
    # Mock argparse to return stdio transport
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_parser = MagicMock()
    mock_parser.parse_args.return_value = mock_args
    mocker.patch("gemini_mcp.server.argparse.ArgumentParser", return_value=mock_parser)
    mock_run = mocker.patch("gemini_mcp.server.mcp.run")

    # Call main
    main()

    # Assertions
    mock_run.assert_called_once_with(transport="stdio")
    assert os.environ.get("MCP_TRANSPORT_MODE") == "stdio"


def test_main_streamable_http(mocker):
    # Mock argparse to return streamable-http transport
    mock_args = MagicMock()
    mock_args.transport = "streamable-http"
    mock_parser = MagicMock()
    mock_parser.parse_args.return_value = mock_args
    mocker.patch("gemini_mcp.server.argparse.ArgumentParser", return_value=mock_parser)
    mock_run = mocker.patch("gemini_mcp.server.mcp.run")

    # Call main
    main()

    # Assertions
    assert os.environ.get("MCP_TRANSPORT_MODE") == "streamable-http"
    mock_run.assert_called_once()
    run_kwargs = mock_run.call_args.kwargs
    assert run_kwargs["transport"] == "streamable-http"
    assert run_kwargs["host"] == "0.0.0.0"
    assert run_kwargs["port"] == 8000
    assert run_kwargs["path"] == "/mcp"
    assert "middleware" in run_kwargs
