import asyncio
from mealie_mcp import health


def test_ping_returns_pong():
    async def _run():
        return await health.ping()

    result = asyncio.run(_run())
    assert result == "pong"
