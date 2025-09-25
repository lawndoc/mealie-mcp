from fastmcp import Context
from typing import Any, Dict, List
from .mealie_logger import logger
from .server import mcp


@mcp.tool()
async def list_recipes(ctx: Context) -> List[Dict[str, Any]]:
    """Retrieve all recipes from Mealie."""
    logger.info("Fetching all recipes")
    r = await ctx.request_context.lifespan_context.client.get("/api/recipes")
    r.raise_for_status()
    recipes = r.json()
    logger.info(f"Retrieved {len(recipes)} recipes")
    return recipes


@mcp.tool()
async def search_recipes(ctx: Context, query: str) -> List[Dict[str, Any]]:
    """Search recipes by name or ingredient."""
    logger.info(f"Searching for recipes with query: {query}")
    resp = await ctx.request_context.lifespan_context.client.get(
        "/api/recipes/search", params={"query": query}
    )
    resp.raise_for_status()
    recipes = resp.json()
    logger.info(f"Found {len(recipes)} recipes matching query '{query}'")
    return recipes


@mcp.tool()
async def get_recipe(ctx: Context, recipe_id: str) -> Dict[str, Any]:
    """Fetch details of a single recipe by ID."""
    logger.info(f"Fetching recipe with ID: {recipe_id}")
    r = await ctx.request_context.lifespan_context.client.get(
        f"/api/recipes/{recipe_id}"
    )
    r.raise_for_status()
    recipe = r.json()
    logger.info(f"Retrieved recipe: {recipe.get('name', 'Unknown')}")
    return recipe
