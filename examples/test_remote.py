# pip install easymcp google-genai mcp mcp_simple_arxiv markitdown-mcp
# requires Python 3.13+
import os
import asyncio
import subprocess
from google import genai
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


# Get the Gemini API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")

# Create Gemini instance LLM class
client = genai.Client(api_key=api_key)

# remote_url = "http://localhost:8000/mcp"
remote_url = "https://gemini-mcp-server-231532712093.europe-west1.run.app/mcp/"


async def run():
    async with streamablehttp_client(
        remote_url, headers={"Authorization": f"Bearer {api_key}"}
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Initialize conversation history using simple tuples
            config = genai.types.GenerateContentConfig(
                temperature=0,
                tools=[session],
            )
            print("Agent is ready. Type 'exit' to quit.")
            chat = client.aio.chats.create(
                model="gemini-2.5-flash-preview-05-20", config=config
            )
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Exiting chat.")
                    break

                # Append user message to history
                response = await chat.send_message(user_input)
                if len(response.automatic_function_calling_history) > 0:
                    if (
                        response.automatic_function_calling_history[0].parts[0].text
                        == user_input
                    ):
                        response.automatic_function_calling_history.pop(0)
                    for call in response.automatic_function_calling_history:
                        if call.parts[0].function_call:
                            print(f"Function call: {call.parts[0].function_call}")
                        elif call.parts[0].function_response:
                            print(
                                f"Function response: {call.parts[0].function_response.response['result'].content[0].text}"
                            )
                print(f"Assistant: {response.text}")


if __name__ == "__main__":
    asyncio.run(run())
