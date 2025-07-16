import os
import asyncio
import time
from mcp import ClientSession, StdioServerParameters, stdio_client

server_params = StdioServerParameters(
    command="code-sandbox-mcp",  # Executable
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
            print([tool.name for tool in tools.tools])

            start_time = time.time()
            r = await session.call_tool(
                "run_javascript_code",
                arguments={"code": "console.log('Hello, World!');"},
            )
            print(r.content[0].text)
            print(f"Time taken: {time.time() - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(run())
