from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from .mealie_client import MealieClient
from .log import logger


@dataclass
class AppContext:
    client: MealieClient


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    logger.info("Starting Mealie MCP server")
    try:
        async with MealieClient() as client:
            logger.info("MealieClient initialized successfully")
            ctx = AppContext(client=client)
            yield ctx
    except Exception as e:
        logger.error(f"Error during server lifespan: {str(e)}")
        raise
    finally:
        logger.info("Shutting down Mealie MCP server")


if __name__ == "__main__":
    logger.info("Initializing FastMCP server for Mealie")
    mcp = FastMCP("Mealie", lifespan=lifespan)
    try:
        mcp.run()
    except Exception as e:
        logger.critical(f"Fatal error in MCP server: {str(e)}")
        raise
