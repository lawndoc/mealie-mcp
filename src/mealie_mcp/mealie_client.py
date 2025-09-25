import httpx
import os
from .mealie_logger import logger


class MealieClient:
    async def __aenter__(self):
        self.base_url = os.environ.get("MEALIE_URL", "").rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)
        await self._reauthenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        return False

    async def _reauthenticate(self) -> None:
        base_url = self.base_url
        username = os.environ.get("MEALIE_USERNAME", "")
        password = os.environ.get("MEALIE_PASSWORD", "")
        async with httpx.AsyncClient() as temp_client:
            auth_response = await temp_client.post(
                f"{base_url}/api/auth/token",
                data={
                    "username": username,
                    "password": password,
                    "remember_me": "true",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            auth_response.raise_for_status()
            token = auth_response.json().get("access_token")
        self.headers["Authorization"] = f"Bearer {token}"
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        response = await self.client.request(method, url, **kwargs)
        if response.status_code == 401:
            await self._reauthenticate()
            response = await self.client.request(method, url, **kwargs)
        return response

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("DELETE", url, **kwargs)

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()
