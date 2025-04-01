# Semantic Tool

**Semantic Tool** is a microservice designed for dynamic discovery and invocation of external tools based on semantic similarity. It leverages vector embeddings to allow natural language queries to match and invoke relevant tools from a registry.

## Features

- 🧠 **Semantic Tool Search** – Find tools using vector-based matching of descriptions.
- 🧰 **Tool Invocation API** – Call tools directly via REST interface.
- 🛰️ **Server Management** – Register and list available MCP servers.

## API Overview

### Tool Endpoints

- `GET /api/v1/tools/list`: List all available tools.
- `POST /api/v1/tools/call`: Invoke a tool by name and arguments.
- `POST /api/v1/tools/semantic`: Find relevant tools by semantic similarity to a text query.

### Server Endpoints

- `GET /api/v1/servers/list`: List all active server sessions.

## Configuration

Set config via a URL using `CONFIG_LOCATION` (default: `file:///config.yaml`).

Example `config.yaml`:

```yaml
mcp_servers:
  timeserver:
    command: uvx
    args: ["mcp-timeserver"]
  searxng:
    command: uvx
    args: ["mcp-searxng"]
  wolframalpha:
    command: uvx
    args: ["mcp-wolfram-alpha"]
    env:
      WOLFRAM_API_KEY: "your_api_key"

embedding:
  model_name: "all-MiniLM-L6-v2"
  dim: 384
```

## Installation

### Local (via `uv`)

```bash
uv run semantictool
```

### Docker (recommended)

```bash
docker compose up
```

## Dependencies

- Python 3.13+
- [FastAPI](https://fastapi.tiangolo.com/)
- [sentence-transformers](https://www.sbert.net/)
- [easymcp](https://pypi.org/project/easymcp/)
- [uv](https://astral.sh/uv/)
