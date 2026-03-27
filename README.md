# shipra-alerts-mcp-py

Shipra Alerts MCP server built with `FastMCP`, with a FastAPI host app for HTTP deployment.

## Requirements

- Python `3.12`
- `uv`
- Node.js and `npx` if you want to use MCP Inspector

## Install dependencies

From the project root:

```bash
uv sync
```

## Run locally

### Option 1: Run the FastAPI server

This starts the HTTP server and exposes the MCP app through FastAPI.

```bash
uv run python server.py
```

By default, the app will be available on:

- `http://127.0.0.1:8000`
- MCP endpoint: `http://127.0.0.1:8000/mcp`

You can also run it directly with uvicorn:

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000
```

### Option 2: Run the MCP server with MCP Inspector

Run this MCP server with the MCP Inspector from the project root:

```bash
npx @modelcontextprotocol/inspector \
  uv \
  --directory . \
  run \
  python \
  main.py
```

If you want to use an absolute path instead of running from the repo root:

```bash
npx @modelcontextprotocol/inspector \
  uv \
  --directory F:/Work/2026/mcp-tools/shipra-alerts-mcp-py \
  run \
  python \
  main.py
```

Short form:

```bash
npx @modelcontextprotocol/inspector uv --directory F:/Work/2026/mcp-tools/shipra-alerts-mcp-py run python main.py
```

## Deploy on a server

The simplest production deployment is to run the FastAPI app with `uvicorn` behind a reverse proxy such as Nginx or Caddy.

### Start the app

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000
```

### Linux example with `systemd`

Create a service file like:

```ini
[Unit]
Description=Shipra Alerts MCP FastAPI server
After=network.target

[Service]
WorkingDirectory=/opt/shipra-alerts-mcp-py
ExecStart=/usr/local/bin/uv run uvicorn server:app --host 0.0.0.0 --port 8000
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable shipra-alerts
sudo systemctl start shipra-alerts
```

### Reverse proxy

Point your reverse proxy to:

- App base URL: `http://127.0.0.1:8000`
- MCP endpoint: `http://127.0.0.1:8000/mcp`

If you expose it publicly, add TLS and any required auth headers at the proxy layer or in the app.

## Claude Desktop config

Example `claude_desktop_config.json` entry for connecting to a deployed remote MCP server:

```json
{
  "mcpServers": {
    "shipra-alerts": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "<MCP URL>",
        "--allow-http",
        "--header",
        "Authorization:${AUTH_TOKEN}"
      ],
      "env": {
        "AUTH_TOKEN": "Bearer <YOUR TOKEN>"
      }
    }
  }
}
```
