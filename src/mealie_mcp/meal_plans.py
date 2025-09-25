from fastmcp import Context
from typing import Any, Dict, List
from .mealie_logger import logger
from .server import mcp


@mcp.tool()
async def list_all_meal_plans(ctx: Context) -> List[Dict[str, Any]]:
    logger.info("Fetching all meal plans")
    resp = await ctx.request_context.lifespan_context.client.get("/api/meal-plans")
    resp.raise_for_status()
    meal_plans = resp.json()
    logger.info(f"Retrieved meal plans: {meal_plans.get('total', 0)} total entries")
    return meal_plans


@mcp.tool()
async def create_random_meal(ctx: Context, date: str, meal_type: str) -> Dict[str, Any]:
    logger.info(f"Creating random meal for {date} ({meal_type})")
    payload: Dict[str, Any] = {"date": date, "entryType": meal_type}
    resp = await ctx.request_context.lifespan_context.client.post(
        "/api/households/mealplans/random", json=payload
    )
    resp.raise_for_status()
    result = resp.json()
    return result


@mcp.tool()
async def add_recipe_to_meal_plan(
    ctx: Context, date: str, meal_type: str, recipe_id: str
) -> Dict[str, Any]:
    logger.info(f"Adding recipe {recipe_id} to meal plan for {date} ({meal_type})")
    payload: Dict[str, Any] = {"date": date, "entryType": meal_type, "recipeId": recipe_id}
    resp = await ctx.request_context.lifespan_context.client.post(
        "/api/households/mealplans", json=payload
    )
    resp.raise_for_status()
    result = resp.json()
    return result
