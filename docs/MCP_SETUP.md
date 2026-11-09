# Local MCP setup

SiliconCrew exposes its RTL tools through a local MCP server as well as the web workbench.

## Start the server

From the repository root, activate the project environment and configure at least one model API key in `.env`:

```bash
source .venv/bin/activate
python mcp_server.py
```

The default `stdio` transport is intended to be launched by an MCP client. Keep the server command running under that client rather than starting it in a separate terminal.

## Claude Desktop example

Add a server entry to Claude Desktop's MCP configuration. Use absolute paths for both the virtual-environment Python executable and `mcp_server.py`:

```json
{
  "mcpServers": {
    "siliconcrew": {
      "command": "/absolute/path/to/LLM-RTL-siliconcrew/.venv/bin/python",
      "args": ["/absolute/path/to/LLM-RTL-siliconcrew/mcp_server.py"]
    }
  }
}
```

Restart the MCP client after updating its configuration. On Windows, use the Python executable under `.venv\\Scripts\\python.exe` and Windows-style absolute paths.

## Verify the connection

Ask the client to create a small design, such as a 4-bit counter. SiliconCrew should create a specification, write Verilog and a testbench, then use the local verification tools when they are available.

The server also supports HTTP-based transports for local experimentation. Run `python mcp_server.py --help` to see the available options. Do not expose an unauthenticated development server to an untrusted network.
