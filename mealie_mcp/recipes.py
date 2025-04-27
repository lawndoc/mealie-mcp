from mcp.server.fastmcp import Context
from typing import Any, Dict, List
from .mealie_logger import logger
from .server import mcp


@mcp.tool()
async def list_recipes(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieve all recipes from Mealie.

    Returns:
      - A list of recipe summary objects, as returned by the /api/recipes endpoint.
    """
    logger.info("Fetching all recipes")
    try:
        r = await ctx.request_context.lifespan_context.client.get("/api/recipes")
        r.raise_for_status()
        recipes = r.json()
        logger.info(f"Retrieved {len(recipes)} recipes")
        return recipes
    except Exception as e:
        logger.error(f"Failed to fetch recipes: {str(e)}")
        raise


@mcp.tool()
async def search_recipes(ctx: Context, query: str) -> List[Dict[str, Any]]:
    """
    Search recipes by name or ingredient.

    Parameters:
      - query: text to search for in recipes

    Returns:
      - A list of recipe objects matching the query, as returned by Mealie's API.
    """
    logger.info(f"Searching for recipes with query: {query}")
    try:
        resp = await ctx.request_context.lifespan_context.client.get(
            "/api/recipes/search", params={"query": query}
        )
        resp.raise_for_status()
        recipes = resp.json()
        logger.info(f"Found {len(recipes)} recipes matching query '{query}'")
        return recipes
    except Exception as e:
        logger.error(f"Recipe search failed for query '{query}': {str(e)}")
        raise


@mcp.tool()
async def get_recipe(ctx: Context, recipe_id: str) -> Dict[str, Any]:
    """
    Fetch the details of a single recipe by its ID.
    """
    logger.info(f"Fetching recipe with ID: {recipe_id}")
    try:
        r = await ctx.request_context.lifespan_context.client.get(
            f"/api/recipes/{recipe_id}"
        )
        r.raise_for_status()
        recipe = r.json()
        logger.info(f"Retrieved recipe: {recipe.get('name', 'Unknown')}")
        return recipe
    except Exception as e:
        logger.error(f"Failed to fetch recipe {recipe_id}: {str(e)}")
        raise
