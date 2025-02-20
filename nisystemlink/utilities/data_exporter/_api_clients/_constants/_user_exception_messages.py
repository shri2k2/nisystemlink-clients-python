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
