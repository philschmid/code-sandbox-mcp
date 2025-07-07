import pytest
from fastmcp import FastMCP, Client
from gemini_mcp.server import mcp as gemini_mcp_server
import os


@pytest.fixture(scope="module")
def mcp_stdio_server():
    """
    Fixture to provide the main gemini_mcp server instance for testing.
    """
    # Set transport mode for testing
    os.environ["MCP_TRANSPORT_MODE"] = "stdio"

    yield gemini_mcp_server


@pytest.mark.asyncio
async def test_web_search_integration(mcp_stdio_server: FastMCP):
    """
    Tests the web_search tool using an in-memory client.
    """
    query = "What is the latest news on Gemini AI?"
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("web_search", {"query": query})
        assert isinstance(result[0].text, str)
        assert len(result[0].text) > 0


@pytest.mark.asyncio
async def test_use_gemini_integration(mcp_stdio_server: FastMCP):
    """
    Tests the use_gemini tool using an in-memory client.
    """
    prompt = "What is 1 + 1?"
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("use_gemini", {"prompt": prompt})
        assert isinstance(result[0].text, str)
        assert "2" in result[0].text
