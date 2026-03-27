from fastapi import FastAPI
from alerts_mcp import mcp
from fastapi import FastAPI, Header, HTTPException

mcp_app = mcp.http_app(path="/mcp")

app = FastAPI(title="Shipra MCP")

# Attach MCP lifespan properly
app.router.lifespan_context = mcp_app.lifespan

# Mount MCP under /mcp
app.mount("/", mcp_app)