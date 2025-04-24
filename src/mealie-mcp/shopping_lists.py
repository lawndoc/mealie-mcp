from . import mcp
from mcp.server.fastmcp import Context
from typing import Any, Dict, List


@mcp.resource("mealie://shopping-lists")
async def get_all_shopping_lists(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieve every shopping list in the household.
    Returns a list of ShoppingListOut objects as defined by Mealie.
    """
    resp = await ctx.request_context.lifespan_context.client.get(
        "/api/households/shopping/lists"
    )
    resp.raise_for_status()
    return resp.json()


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
    resp = await ctx.request_context.lifespan_context.client.get(
        f"/api/households/shopping/lists/{list_id}"
    )
    resp.raise_for_status()
    return resp.json()


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
    - recipe_params: payload following Mealie’s ShoppingListAddRecipeParamsBulk schema, e.g.:
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
    url = f"/api/households/shopping/lists/{shopping_list_id}/recipe"
    resp = await ctx.request_context.lifespan_context.client.post(
        url, json=recipe_params
    )
    resp.raise_for_status()
    return resp.json()
