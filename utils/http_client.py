import httpx

from settings import settings


async def make_get_request(
    url: str,
    credentials: tuple = (),
) -> dict:
    """
    Make a GET request to the Azure DevOps API

    Args:
        url: The URL to make the request to
        params: The parameters to send with the request
        credentials: The credentials to use for the request

    Returns:
        The response from the request
    """

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url, auth=credentials)
        response.raise_for_status()

        return response.json()


async def make_post_request(
    url: str,
    method: str,
    data: dict = {},
    credentials: tuple = (),
) -> dict:
    """
    Make a request to the Azure DevOps API

    Args:
        url: The URL to make the request to
        method: The HTTP method to use
        data: The data to send with the request
        params: The parameters to send with the request
        credentials: The credentials to use for the request

    Returns:
        The response from the request
    """

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=data, auth=credentials)
        response.raise_for_status()

        return response.json()


async def make_patch_request(
    url: str,
    data: dict | list[dict],
    credentials: tuple = (),
) -> dict:
    """
    Make a PATCH request to the Azure DevOps API
    """

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Content-Type": "application/json-patch+json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.patch(url, json=data, auth=credentials)
        response.raise_for_status()

        return response.json()
