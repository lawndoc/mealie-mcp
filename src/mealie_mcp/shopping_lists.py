from fastmcp import Context
from typing import Any, Dict, List
from .mealie_logger import logger
from .server import mcp


@mcp.tool()
async def get_all_shopping_lists(ctx: Context) -> List[Dict[str, Any]]:
    logger.info("Fetching all shopping lists")
    resp = await ctx.request_context.lifespan_context.client.get(
        "/api/households/shopping/lists"
    )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def get_shopping_list_contents(ctx: Context, list_id: str) -> Dict[str, Any]:
    logger.info(f"Fetching shopping list with ID: {list_id}")
    resp = await ctx.request_context.lifespan_context.client.get(
        f"/api/households/shopping/lists/{list_id}"
    )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def add_recipe_ingredients_to_list(
    ctx: Context, shopping_list_id: str, recipe_params: Dict[str, Any]
) -> Dict[str, Any]:
    recipe_id = recipe_params.get("recipeId", "unknown")
    logger.info(
        f"Adding recipe {recipe_id} ingredients to shopping list {shopping_list_id}"
    )
    url = f"/api/households/shopping/lists/{shopping_list_id}/recipe"
    resp = await ctx.request_context.lifespan_context.client.post(url, json=recipe_params)
    resp.raise_for_status()
    return resp.json()
