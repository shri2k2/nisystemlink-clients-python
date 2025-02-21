from http import HTTPStatus


class BaseHttpRoutes:
    AUTH_APIS_ROUTE = "/niauth"
    USER_APIS_ROUTE = "/niuser"
    WEBAPPS_BASE_ROUTE = "/niapp/v1/webapps"
    TEST_MONITOR_BASE_ROUTE = "/nitestmonitor/v2"


class HttpConstants:
    TIMEOUT_IN_SECONDS = 60
    VERIFY_SSL_CERTIFICATE = True
    TAKE = 1000


class HttpRetryConstants:
    HTTP_RETRY_CODES = [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]
    MAX_HTTP_RETRIES = 6


class SystemLinkQueryKeys:
    FILTER = "filter"
    RESULT_FILTER = "resultFilter"
    UPDATED_AT = "UPDATED_AT"
    TAKE = "take"
    ORDER_BY = "orderBy"


class UserExceptionMessages:
    """Messages displayed to the user."""

    DATASPACE_NOT_FOUND = "The dataspace {dataspace_name} does not exist."
    EMPTY_RESPONSE_BODY = "The response body is empty."
    FAILED_TO_PARSE_RESPONSE = (
        "Failed to parse the response content for type {content_type}"
    )
    FAILED_TO_CONNECT = "Failed to connect to the server"
    FAILED_TO_PARSE_JSON = "Failed to parse JSON response"
    FAILED_TO_RETRIEVE_RESPONSE = "Failed to retrieve response content"
    FAILED_TO_ESTABLISH_SECURE_CONNECTION = "Failed to establish a secure connection"
    UNKNOWN_ERROR = "Error while making the request to {api_url}"
