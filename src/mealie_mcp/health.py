from fastmcp import Context
from .server import mcp

@mcp.tool()
async def ping() -> str:
    return "pong"

@mcp.tool()
async def check_connection(ctx: Context) -> dict:
    resp = await ctx.request_context.lifespan_context.client.get("/api/recipes")
    return {"status": "ok", "http_status": resp.status_code} if resp.is_success else {"status": "error", "http_status": resp.status_code}
