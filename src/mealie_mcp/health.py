from fastmcp import Context
from .server import mcp

@mcp.tool()
async def ping() -> str:
    return "pong"

@mcp.tool()
async def check_connection(ctx: Context) -> dict:
    resp = await ctx.request_context.lifespan_context.client.get("/api/recipes")
    if resp.is_success:
        return {"status": "ok", "http_status": resp.status_code}
    else:
        return {"status": "error", "http_status": resp.status_code}
