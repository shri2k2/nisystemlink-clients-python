from typing import Awaitable, Callable, Dict

import aiohttp
import backoff
from aiohttp import ClientConnectionError, ClientResponse, ClientResponseError
from nisystemlink.utilities.data_exporter._api_clients._constants import (
    HttpConstants,
    HttpRetryConstants,
    UserExceptionMessages,
)


def __is_not_worth_retry(e: Exception) -> bool:
    return not (
        (
            isinstance(e, aiohttp.ClientResponseError)
            and e.status in HttpRetryConstants.HTTP_RETRY_CODES
        )
        or isinstance(e, aiohttp.ClientConnectionError)
    )


@backoff.on_exception(
    backoff.expo,
    (ClientConnectionError, ClientResponseError),
    max_tries=HttpRetryConstants.MAX_HTTP_RETRIES,
    giveup=__is_not_worth_retry,
)
async def __retry_request(
    callable_function: Callable[[], Awaitable[ClientResponse]]
) -> ClientResponse:
    """Retries an HTTP request in case of client errors, using exponential backoff.

    Args:
        callable_function (Callable): A function that makes an HTTP request (either GET or POST).

    Returns:
        Dict: The parsed response content from the successful HTTP request.

    Raises:
        ClientError: If the request fails and retries are exhausted.
    """
    response = await callable_function()
    response.raise_for_status()

    return response


async def get_request(url: str, headers: Dict[str, str] = {}) -> Dict:
    """Makes an HTTP GET request and retrieves the response content.

    Args:
        url (str): The URL to which the GET request is sent.
        headers (dict, optional): Custom headers to be included in the GET request.

    Returns:
        dict: The parsed JSON response from the GET request.

    Raises:
        ClientError: If the request fails or encounters issues.
    """
    session = aiohttp.ClientSession()

    try:
        response = await __retry_request(
            lambda: session.get(
                url,
                headers=headers,
                ssl=HttpConstants.VERIFY_SSL_CERTIFICATE,
                timeout=HttpConstants.TIMEOUT_IN_SECONDS,
            )
        )

    except aiohttp.ClientResponseError as exception:
        raise Exception(
            UserExceptionMessages.FAILED_TO_CONNECT.format(
                exception.request_info.url.path
            )
        ) from exception

    json_response = await response.json()
    await session.close()

    return json_response


async def post_request(url: str, body: Dict, headers: Dict[str, str] = {}) -> Dict:
    """Makes an HTTP POST request with a JSON body and retrieves the response content.

    Args:
        url (str): The URL to which the POST request is sent.
        body (dict): The JSON body to be included in the POST request.
        headers (dict, optional): Custom headers to be included in the POST request.

    Returns:
        dict: The parsed JSON response from the POST request.

    Raises:
        ClientError: If the request fails or encounters issues.
    """
    default_headers = {"accept": "application/json", "Content-Type": "application/json"}

    headers = {**default_headers, **headers}

    session = aiohttp.ClientSession()

    try:
        response = await __retry_request(
            lambda: session.post(
                url,
                json=body,
                headers=headers,
                ssl=HttpConstants.VERIFY_SSL_CERTIFICATE,
                timeout=HttpConstants.TIMEOUT_IN_SECONDS,
            )
        )

    except aiohttp.ClientResponseError as exception:
        raise Exception(
            UserExceptionMessages.FAILED_TO_CONNECT.format(
                exception.request_info.url.path
            )
        ) from exception

    json_response = await response.json()
    await session.close()

    return json_response
