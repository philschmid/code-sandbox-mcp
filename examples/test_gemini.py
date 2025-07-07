from fastmcp import Client
from google import genai
import asyncio


mcp_client = Client(
    {
        "local_server": {
            "transport": "stdio",
            "command": "code-sandbox-mcp",
        }
    }
)
gemini_client = genai.Client()


async def main():
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents="Use Python to ping the google.com website and return the response time.",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
