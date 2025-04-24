from . import mcp
from mcp.server.fastmcp import Context
from typing import Any, Dict, List
from .log import logger


@mcp.resource("mealie://shopping-lists")
async def get_all_shopping_lists(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieve every shopping list in the household.
    Returns a list of ShoppingListOut objects as defined by Mealie.
    """
    logger.info("Fetching all shopping lists")
    try:
        resp = await ctx.request_context.lifespan_context.client.get(
            "/api/households/shopping/lists"
        )
        resp.raise_for_status()
        lists = resp.json()
        logger.info(f"Retrieved {len(lists)} shopping lists")
        return lists
    except Exception as e:
        logger.error(f"Failed to fetch shopping lists: {str(e)}")
        raise


@mcp.resource("mealie://shopping-lists/{list_id}")
async def get_shopping_list_contents(ctx: Context, list_id: str) -> Dict[str, Any]:
    """
    Fetch the details (contents) of a single shopping list.

    Parameters:
    - list_id: UUID of the shopping list to retrieve.

    Returns:
    - A dict representing the ShoppingListOut object, e.g.:
      {
        "id": "uuid-of-list",
        "name": "Weekly Groceries",
        "items": [
          {
            "id": "item-uuid",
            "name": "2 carrots",
            "notes": "organic",
            "purchased": false
          },
          ...
        ],
        "created": "2023-04-12T14:23:00Z",
        "updated": "2023-04-13T09:45:00Z"
      }
    """
    logger.info(f"Fetching shopping list with ID: {list_id}")
    try:
        resp = await ctx.request_context.lifespan_context.client.get(
            f"/api/households/shopping/lists/{list_id}"
        )
        resp.raise_for_status()
        shopping_list = resp.json()
        item_count = len(shopping_list.get("items", []))
        logger.info(f"Retrieved shopping list '{shopping_list.get('name', 'Unknown')}' with {item_count} items")
        return shopping_list
    except Exception as e:
        logger.error(f"Failed to fetch shopping list {list_id}: {str(e)}")
        raise


# ----------
# TOOLS
# ----------
@mcp.tool()
async def add_recipe_ingredients_to_list(
    ctx: Context, shopping_list_id: str, recipe_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add the ingredients of a recipe to a given shopping list.

    - shopping_list_id: UUID of the target shopping list
    - recipe_params: payload following Mealie's ShoppingListAddRecipeParamsBulk schema, e.g.:
      {
        "recipeId": "uuid-of-recipe",
        "recipeIncrementQuantity": 1,        # optional, defaults to 1
        "recipeIngredients": [               # optional override
            {
              "name": "2 carrots",
              "notes": "organic",
              "purchased": false
            },
            ...
        ]
      }

    Returns the updated shopping list.
    """
    recipe_id = recipe_params.get("recipeId", "unknown")
    quantity = recipe_params.get("recipeIncrementQuantity", 1)
    logger.info(f"Adding recipe {recipe_id} ingredients (quantity: {quantity}) to shopping list {shopping_list_id}")
    
    try:
        url = f"/api/households/shopping/lists/{shopping_list_id}/recipe"
        resp = await ctx.request_context.lifespan_context.client.post(
            url, json=recipe_params
        )
        resp.raise_for_status()
        result = resp.json()
        item_count = len(result.get("items", []))
        logger.info(f"Successfully added recipe ingredients to shopping list. List now has {item_count} items")
        return result
    except Exception as e:
        logger.error(f"Failed to add recipe {recipe_id} ingredients to shopping list {shopping_list_id}: {str(e)}")
        raise
