import pytest
from fastmcp import FastMCP, Client
from code_sandbox_mcp.server import mcp as code_sandbox_mcp_server
import os


@pytest.fixture(scope="module")
def mcp_stdio_server():
    """
    Fixture to provide the main code_sandbox_mcp server instance for testing.
    """
    # Set transport mode for testing
    os.environ["MCP_TRANSPORT_MODE"] = "stdio"

    yield code_sandbox_mcp_server


@pytest.mark.asyncio
async def test_run_python_code_integration(mcp_stdio_server: FastMCP):
    """
    Tests the run_python_code tool using an in-memory client.
    """
    query = "print('Hello, World!')"
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("run_python_code", {"code": query})
        assert isinstance(result.content[0].text, str)
        assert len(result.content[0].text) > 0


@pytest.mark.asyncio
async def test_run_python_code_integration_with_error(mcp_stdio_server: FastMCP):
    """
    Tests the run_python_code tool using an in-memory client with an error
    """
    query = """from google.genai import genai
    client = genai.Client()
    response = client.generate_content("Hello, world!")
    print(response.text)
    """
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("run_python_code", {"code": query})
        assert isinstance(result.content[0].text, str)
        assert "error" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_run_javascript_code_integration(mcp_stdio_server: FastMCP):
    """
    Tests the run_javascript_code tool using an in-memory client.
    """
    prompt = "console.log('Hello, World!');"
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("run_javascript_code", {"code": prompt})
        assert isinstance(result.content[0].text, str)


@pytest.mark.asyncio
async def test_run_javascript_code_integration_with_error(mcp_stdio_server: FastMCP):
    """
    Tests the run_javascript_code tool using an in-memory client with an error
    """
    prompt = "const x = 1 / 0; console.log(y);"
    async with Client(mcp_stdio_server) as client:
        result = await client.call_tool("run_javascript_code", {"code": prompt})
        assert isinstance(result.content[0].text, str)
        assert "error" in result.content[0].text.lower()
