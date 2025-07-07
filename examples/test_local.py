import os
import asyncio
from google import genai
from mcp import ClientSession, StdioServerParameters, stdio_client


# Get the Gemini API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")

# Create Gemini instance LLM class
client = genai.Client(api_key=api_key)

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="gemini-mcp",  # Executable
    args=[
        "--transport",
        "stdio",
    ],
    env={"GEMINI_API_KEY": api_key},
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read,
            write,
        ) as session:
            await session.initialize()
            # Initialize conversation history using simple tuples
            tools = await session.list_tools()
            print(tools)

            r = await session.call_tool(
                "search_web", arguments={"query": "What is the capital of France?"}
            )
            print(r)


if __name__ == "__main__":
    asyncio.run(run())
