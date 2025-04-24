from . import mcp
from mcp.server.fastmcp import Context
from typing import Any, Dict, List


@mcp.resource("mealie://meal-plans")
async def list_all_meal_plans(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieve all recipes scheduled on the meal plan.

    Returns:
      - A list of meals planned with
        {
            "page": 1,
            "per_page": 10,
            "total": 0,
            "total_pages": 0,
            "items": [
                {
                    "date": "2019-08-24",
                    "entryType": "breakfast",
                    "title": "",
                    "text": "",
                    "recipeId": "31545f76-b27f-4c7c-9faf-229771396df1",
                    "id": 0,
                    "groupId": "eb54e96e-21b8-4f54-9cd4-80fccbd06f55",
                    "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
                    "householdId": "b5d33c47-da83-44b4-b7bf-7ab3c5485f36",
                    "recipe": { ... }
                }
            ],
            "next": "string",
            "previous": "string"
        }
    """
    resp = await ctx.client.get("/api/meal-plans")
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def create_random_meal(ctx: Context, date: str, meal_type: str) -> Dict[str, Any]:
    """
    Create a random meal according to the household's meal plan settings.

    Parameters:
      - date: year, month, and day to schedule the recipe (e.g. "2025-07-15").
      - meal_type: Meal slot (e.g. "breakfast", "lunch", "dinner").

    Returns:
        - The created MealPlanEntry object, as returned by Mealie.
    """
    payload: Dict[str, Any] = {
        "date": date,
        "entryType": meal_type,
    }
    resp = await ctx.client.post("/api/households/mealplans/random", json=payload)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def add_recipe_to_meal_plan(
    ctx: Context, date: str, meal_type: str, recipe_id: str
) -> Dict[str, Any]:
    """
    Add a recipe entry to the meal plan.

    Parameters:
      - date: year, month, and day to schedule the recipe (e.g. "2025-07-15").
      - meal_type: Meal slot (e.g. "breakfast", "lunch", "dinner").
      - recipe_id: UUID of the recipe to insert.

    Returns:
      - The created MealPlanEntry object, as returned by Mealie.
    """
    payload: Dict[str, Any] = {
        "date": date,
        "entryType": meal_type,
        "recipeId": recipe_id,
    }

    resp = await ctx.client.post(f"/api/households/mealplans", json=payload)
    resp.raise_for_status()
    return resp.json()
