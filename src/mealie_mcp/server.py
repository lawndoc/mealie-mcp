import click
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
from .mealie_client import MealieClient
from .mealie_logger import logger


@dataclass
class AppContext:
    client: MealieClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    logger.info("Starting Mealie MCP server")
    try:
        async with MealieClient() as client:
            logger.info("MealieClient initialized successfully")
            yield AppContext(client=client)
    except Exception as e:
        logger.error(f"Error during server setup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down Mealie MCP server")
        

mcp = FastMCP("Mealie", lifespan=app_lifespan)
from . import meal_plans
from . import recipes
from . import shopping_lists


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="sse",
    help="Transport type",
)
def main(transport: str = "sse") -> None:
    logger.info("Initializing FastMCP server for Mealie")
    try:
        mcp.run(transport=transport)
    except Exception as e:
        logger.critical(f"Fatal error in MCP server: {str(e)}")
        raise
