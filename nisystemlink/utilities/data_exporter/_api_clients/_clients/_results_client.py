from typing import Dict, List, Optional

from nisystemlink.utilities.data_exporter._api_clients._api_exception import (
    ApiException,
)
from nisystemlink.utilities.data_exporter._api_clients._api_utilities import (
    post_request,
)
from nisystemlink.utilities.data_exporter._api_clients._constants import (
    ApiExceptionMessages,
    BaseHttpRoutes,
    HttpConstants,
    SystemLinkQueryKeys,
)
from nisystemlink.utilities.data_exporter._api_clients._models import (
    ResultResponse,
)
from pydantic import parse_obj_as


class ResultsClient:

    def __init__(
        self, api_key: Optional[str] = None, systemlink_uri: Optional[str] = None
    ) -> None:
        self.__api_key = api_key

        self.__query_results_url = (
            f"{systemlink_uri}{BaseHttpRoutes.TEST_MONITOR_BASE_ROUTE}/query-results"
        )

    def __get_headers(self) -> Dict[str, str]:
        """Helper method to get headers with API key if available."""
        return {"x-ni-api-key": self.__api_key} if self.__api_key else {}

    async def query_results(self, results_filter: str) -> List[ResultResponse]:
        """Makes a POST request to query the test results.

        Args:
            results_filter (str): Linq filter for the test results

        Returns:
            List[Dict]: List of test results
        """
        try:
            body = {
                SystemLinkQueryKeys.FILTER: results_filter,
                SystemLinkQueryKeys.TAKE: HttpConstants.TAKE,
                SystemLinkQueryKeys.ORDER_BY: SystemLinkQueryKeys.UPDATED_AT,
            }
            headers = self.__get_headers()

            all_results = []

            response = await post_request(
                self.__query_results_url, body=body, headers=headers
            )

            if not response or response["results"] is None:
                raise ApiException(
                    message=ApiExceptionMessages.FAILED_TO_RETRIEVE_PROPER_RESPONSE.format(
                        request_context="querying results"
                    ),
                    response=response,
                )

            all_results.extend(response["results"])

            while response["continuationToken"]:
                body["continuationToken"] = response["continuationToken"]
                response = await post_request(
                    self.__query_results_url, body=body, headers=headers
                )

                if not response or response["results"] is None:
                    raise ApiException(
                        message=ApiExceptionMessages.EMPTY_PAGINATION_RESPONSE.format(
                            request_context="querying results"
                        ),
                        response=response,
                    )

                all_results.extend(response["results"])

            return parse_obj_as(List[ResultResponse], all_results)

        except ApiException:
            raise  # Re-raise API errors

        except Exception as exception:
            raise ApiException(
                message=ApiExceptionMessages.FAILED_API_REQUEST.format("query results"),
                response=response,
            ) from exception
