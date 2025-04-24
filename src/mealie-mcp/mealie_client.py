import httpx
import os
from .log import logger


class MealieClient:
    """
    Wrapper around httpx.AsyncClient that handles token expiration and automatic reauthentication.
    """ 
    async def __aenter__(self):
        self.base_url = os.environ.get("MEALIE_URL", "").rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)
        logger.info(f"Initialized MealieClient with base URL: {self.base_url}")
        await self._reauthenticate()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info("Closing MealieClient")
        await self.client.aclose()
        return False  # re-raise any exceptions

    async def _reauthenticate(self) -> None:
        """Refresh the authentication token and update headers."""
        base_url = self.base_url
        username = os.environ.get("MEALIE_USERNAME", "")
        password = os.environ.get("MEALIE_PASSWORD", "")

        logger.info("Authenticating with Mealie API")
        try:
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
            logger.info("Authentication successful")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Send a request to the Mealie API and handle authentication errors.
        """
        try:
            logger.debug(f"Sending {method} request to {url}")
            response = await self.client.request(method, url, **kwargs)

            if response.status_code == 401:
                logger.warning("Token expired, reauthenticating")
                await self._reauthenticate()
                logger.debug(f"Retrying {method} request to {url}")
                response = await self.client.request(method, url, **kwargs)
            
            if not response.is_success:
                logger.error(f"Request failed with status {response.status_code}: {response.text}")
            else:
                logger.debug(f"Request successful: {response.status_code}")
                
            return response

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during request: {str(e)}")
            raise

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
            logger.info("Closing client connection")
            await self.client.aclose()
