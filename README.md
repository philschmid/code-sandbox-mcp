# Code Sandbox MCP Server

The Code Sandbox MCP Server is a secure, STDIO-based Model Context Protocol (MCP) Server, allowing AI assistants and LLM applications to safely execute code snippets using containerized environments. It is uses the [llm-sandbox](https://github.com/vndee/llm-sandbox) package to execute the code snippets. 

**How It Works:**
1. Starts a container session (podman, docker, etc.) and ensures the session is open.
2. Writes the `code` to a temporary file on the host.
3. Copies this temporary file into the container at the configured `workdir`.
4. Executes the language-specific commands to run the code, e.g. python `python3 -u code.py` or javascript `node -u code.js`
5. Captures the output and error streams from the container.
6. Returns the output and error streams to the client.

**Available Tools:**
- **run_python_code** - Executes a snippet of Python code in a secure, isolated sandbox.
  - `code` (string, required): The Python code to execute.
- **run_js_code** - Executes a snippet of JavaScript (Node.js) code in a secure, isolated sandbox.
  - `code` (string, required): The JavaScript code to execute.

## Installation

```bash
pip install git+https://github.com/philschmid/code-sandbox-mcp.git
```

## Getting Started: Usage with an MCP Client

Examples:
- [Local Client Python](./examples/test_local_client_python.py) example for running python code
- [Gemini SDK](./examples/test_gemini.py) example for running python code with the Gemini SDK
- [Calling Gemini from a client](./examples/test_client_gemini_call.py) example for running python code that uses the Gemini SDK and passes through the Gemini API key
- [Local Client Javascript](./examples/test_local_client_js.py) example for running javascript code

To use the Code Sandbox MCP server, you need to add it to your MCP client's configuration file (e.g., in your AI assistant's settings). The server is designed to be launched on-demand by the client.

Add the following to your `mcpServers` configuration:

```json
{
  "mcpServers": {
    "code-sandbox": {
      "command": "code-sandbox-mcp",
    }
  }
}
```

### Provide Secrets and pass through environment variables

You can pass through environment variables to the sandbox by setting the `--pass-through-env` flag when starting the MCP server and providing the env when starting the server

```json
{
  "mcpServers": {
    "code-sandbox": {
      "command": "code-sandbox-mcp",
      "args": ["--pass-through-env", "API_KEY,SECRET_TOKEN"]
      "env": {
        "API_KEY": "1234567890",
        "SECRET_TOKEN": "1234567890"
      }
    }
  }
}
```

### Provide a custom container image

You can provide a custom container image by setting the `CONTAINER_IMAGE` and `CONTAINER_LANGUAGE` environment variables when starting the MCP server. Both variables are required as the `CONTAINER_LANGUAGE` is used to determine the commands to run in the container and the `CONTAINER_IMAGE` is used to determine the image to use.

Note: When providing a custom container image both tools will use the same container image.

```json
{
  "mcpServers": {
    "code-sandbox": {
      "command": "code-sandbox-mcp",
      "env": {
        "CONTAINER_IMAGE": "your-own-image",
        "CONTAINER_LANGUAGE": "python" # or "javascript"
      }
    }
  }
}
```

## Customize/Build new Container Images

The repository comes with 2 container images, which are published on Docker Hub:

- `philschmi/code-sandbox-python:latest`
- `philschmi/code-sandbox-js:latest`

```bash
docker build -t philschmi/code-sandbox-python:latest -f containers/Dockerfile.python .
docker build -t philschmi/code-sandbox-js:latest -f containers/Dockerfile.nodejs .
```

The script will build the image using the current user's account. To update the images you want to use you can either pass the --python-image or --js-image flags when starting the MCP server or update the [const.py](./src//code_sandbox_mcp/const.py) file. 

To push the images to Docker Hub you need to retag the images to your own account and push them.

```bash
docker tag philschmi/code-sandbox-python:latest <your-account>/code-sandbox-python:latest
docker push <your-account>/code-sandbox-python:latest
```

To customize or install additional dependencies you can add them to the [Dockerfile](./Dockerfile) and build the image again. 


## Testing

### With MCP Inspector
Start the server with streamable-http and test your server using the MCP inspector. Alternatively start inspector and run the server with stdio.

```bash
npx @modelcontextprotocol/inspector
```

To run the test suite for `code-sandbox-mcp` and its components, clone the repository and run:

```bash
# You may need to install development dependencies first
pip install -e ".[dev]"

# Run the tests
pytest tests/
```

## License

Code Sandbox MCP Server is open source software licensed under the [MIT License](https://github.com/vndee/llm-sandbox/blob/main/LICENSE).