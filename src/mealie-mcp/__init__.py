from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from mealie_client import MealieClient


@dataclass
class AppContext:
    client: MealieClient


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    async with MealieClient() as client:
        ctx = AppContext(client=client)
        yield ctx


mcp = FastMCP("Mealie", lifespan=lifespan)
