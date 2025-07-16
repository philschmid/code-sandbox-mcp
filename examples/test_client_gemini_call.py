import os
import asyncio
import time
from mcp import ClientSession, StdioServerParameters, stdio_client

server_params = StdioServerParameters(
    command="code-sandbox-mcp",
    args=["--pass-through-env", "GEMINI_API_KEY"],
    env={"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")},
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
                "run_python_code",
                arguments={
                    "code": f"""
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
"""
                },
            )
            print(r.content[0].text)
            print(f"Time taken: {time.time() - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(run())
