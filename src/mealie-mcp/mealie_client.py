import httpx
import os


class MealieClient:
    """
    Wrapper around httpx.AsyncClient that handles token expiration and automatic reauthentication.
    """

    def __init__(self):
        self.base_url = os.environ.get("MEALIE_URL", "").rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)

    async def _reauthenticate(self) -> None:
        """Refresh the authentication token and update headers."""
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
        """
        Send a request to the Mealie API and handle authentication errors.
        """
        try:
            response = await self.client.request(method, url, **kwargs)

            if response.status_code == 401:
                await self._reauthenticate()
                response = await self.client.request(method, url, **kwargs)
            return response

        except httpx.HTTPStatusError as e:
            raise e

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Send a GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Send a POST request."""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> httpx.Response:
        """Send a PUT request."""
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> httpx.Response:
        """Send a PATCH request."""
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """Send a DELETE request."""
        return await self.request("DELETE", url, **kwargs)

    async def close(self) -> None:
        """Close the underlying client."""
        if self.client:
            await self.client.aclose()
