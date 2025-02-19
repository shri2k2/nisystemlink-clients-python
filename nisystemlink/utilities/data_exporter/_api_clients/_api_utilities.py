from data_exporter._api_clients import _constants

import json
from typing import Callable, Dict

import aiohttp
from aiohttp import ClientError, ClientResponse
import backoff

async def __get_response_content(response: ClientResponse) -> Dict:
    """
    Extracts and parses the response content based on the 'Content-Type' header.

    Args:
        response (ClientResponse): The HTTP response object.

    Returns:
        Dict: The parsed JSON content if the response is JSON, or raises appropriate errors.
    
    Raises:
        ClientError: If there is any issue with parsing or extracting content from the response.
    """
    content_type = response.headers.get('Content-Type', '').lower()

    try:
        # Handle different content types
        if 'application/json' in content_type:
            return await response.json()
        elif 'octet-stream' in content_type:
            binary_content = await response.read()
            if not binary_content:
                raise ClientError(response, _constants.UserExceptionMessages.EMPTY_RESPONSE_BODY)
            return json.loads(binary_content.decode("utf-8"))
        else:
            raise ClientError(response, _constants.UserExceptionMessages.FAILED_TO_PARSE_RESPONSE.format(content_type=content_type))
    except aiohttp.ServerConnectionError:
        raise ClientError(response, _constants.UserExceptionMessages.FAILED_TO_CONNECT)
    except json.JSONDecodeError:
        raise ClientError(response, _constants.UserExceptionMessages.FAILED_TO_PARSE_JSON)
    except aiohttp.ClientResponseError:
        raise ClientError(response, _constants.UserExceptionMessages.FAILED_TO_RETRIEVE_RESPONSE)
    except aiohttp.ClientSSLError:
        raise ClientError(response, _constants.UserExceptionMessages.FAILED_TO_ESTABLISH_SECURE_CONNECTION)

@backoff.on_exception(backoff.expo, ClientError, max_tries=_constants.HttpConstants.MAX_HTTP_RETRIES, giveup=lambda e: e.response.status_code not in _constants.HttpConstants.HTTP_RETRY_CODES)
async def __retry_request(callable_function: Callable[[], ClientResponse]) -> Dict:
    """
    Retries an HTTP request in case of client errors, using exponential backoff.

    Args:
        callable_function (Callable): A function that makes an HTTP request (either GET or POST).

    Returns:
        Dict: The parsed response content from the successful HTTP request.
    
    Raises:
        ClientError: If the request fails and retries are exhausted.
    """
    async with callable_function() as response:
        if not response.ok:
            raise ClientError(response, f"HTTP request failed with status code {response.status}")

        return await __get_response_content(response)

async def get_request(url: str, headers: Dict[str, str] = None) -> Dict:
    """
    Makes an HTTP GET request and retrieves the response content.

    Args:
        url (str): The URL to which the GET request is sent.
        headers (dict, optional): Custom headers to be included in the GET request.

    Returns:
        dict: The parsed JSON response from the GET request.
    
    Raises:
        ClientError: If the request fails or encounters issues.
    """
    if headers is None:
        headers = {}

    async with aiohttp.ClientSession() as session:
        return await __retry_request(lambda: session.get(url, headers=headers, ssl=_constants.HttpConstants.VERIFY_SSL_CERTIFICATE, timeout=_constants.HttpConstants.TIMEOUT_IN_SECONDS))

async def post_request(url: str, body: Dict, headers: Dict[str, str] = None) -> Dict:
    """
    Makes an HTTP POST request with a JSON body and retrieves the response content.

    Args:
        url (str): The URL to which the POST request is sent.
        body (dict): The JSON body to be included in the POST request.
        headers (dict, optional): Custom headers to be included in the POST request.

    Returns:
        dict: The parsed JSON response from the POST request.
    
    Raises:
        ClientError: If the request fails or encounters issues.
    """
    if headers is None:
        headers = {}

    default_headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    headers = {**default_headers, **headers}

    async with aiohttp.ClientSession() as session:
        return await __retry_request(lambda: session.post(url, json=body, headers=headers, ssl=_constants.HttpConstants.VERIFY_SSL_CERTIFICATE, timeout=_constants.HttpConstants.TIMEOUT_IN_SECONDS))