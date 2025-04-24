from . import mcp
from mcp.server.fastmcp import Context
from typing import Any, Dict, List


@mcp.resource("mealie://recipes")
async def list_recipes(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieve all recipes from Mealie.
    Returns a list of recipe summaries.
    """
    r = await ctx.request_context.lifespan_context.client.get("/api/recipes")
    r.raise_for_status()
    return r.json()


@mcp.resource("mealie://recipes/search/{query}")
async def search_recipes(ctx: Context, query: str) -> List[Dict[str, Any]]:
    """
    Search recipes by name or ingredient.

    Parameters:
      - query: text to search for in recipes

    Returns:
      - A list of recipe objects matching the query, as returned by Mealie’s API.
    """
    resp = await ctx.client.get("/api/recipes/search", params={"query": query})
    resp.raise_for_status()
    return resp.json()


@mcp.resource("mealie://recipes/{recipe_id}")
async def get_recipe(ctx: Context, recipe_id: str) -> Dict[str, Any]:
    """
    Fetch the details of a single recipe by its ID.
    """
    r = await ctx.request_context.lifespan_context.client.get(
        f"/api/recipes/{recipe_id}"
    )
    r.raise_for_status()
    return r.json()
