---
name: python-mcp-server-generator
description: Best practices for implementing Model Context Protocol (MCP) servers in Python. Integrate Agentic AI capabilities efficiently.
category: Python
license: Private
---

# Python MCP Server Implementation

## When to use this skill

Activate this protocol when you:
- Construct Context and Tool providers for Claude Desktop or similar AI Agent frameworks.
- Implement specialized sub-systems acting as 'eyes and hands' for generic Language Models.
- Rely on standard SSE or stdio bridges over HTTP.

## The Model Context Protocol (MCP)

MCP stands for the ultimate decoupled bridging mechanism letting you write python capabilities mapped strictly into AI Agent inputs.

### Generating a Standard Server

Instead of building boilerplate, leverage the `mcp-server` fast-setup structures. 

```python
from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP instance
mcp = FastMCP("Weather Server")

# 2. Expose a capability as an AI tool using the @mcp.tool decorator
@mcp.tool()
def fetch_weather(city: str) -> str:
    """Fetch the current weather forecasting for a given city."""
    return f"Weather in {city}: 21C, Sunny"

# 3. Start execution
if __name__ == "__main__":
    mcp.run()
```

## Bridging Architecture

Never mingle internal architecture variables directly to the Agent.
Isolate arguments. Validate payloads via `pydantic`. The MCP protocol relies on structured schemas to represent capabilities, and `FastMCP` translates Python hints to JSON Schema.

```python
from pydantic import BaseModel, Field

class AlertRequest(BaseModel):
    message: str = Field(description="The actual broadcast message content")
    urgency: int = Field(description="Urgency level from 1 to 5")

@mcp.tool()
def broadcast_alert(payload: AlertRequest) -> str:
    """Broadcast an urgent alert to the incident room."""
    print(f"[{payload.urgency}] ALERT: {payload.message}")
    return "Alert transmitted."
```

## Running the Server

If integrating via standard input/output (stdio), test your Python server simply by invoking it:

```bash
uv run my_server.py
```

Provide the executable to your Claude setup configuration:
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "my_server.py"]
    }
  }
}
```
