from http import HTTPStatus


class HttpConstants:
    MAX_HTTP_RETRIES = 6
    TIMEOUT_IN_SECONDS = 60
    VERIFY_SSL_CERTIFICATE = False
    HTTP_RETRY_CODES = [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]
    TAKE = 1000
