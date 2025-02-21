from typing import Dict, List, Optional

from nisystemlink.utilities.data_exporter._api_clients._api_utilities import (
    post_request,
)
from nisystemlink.utilities.data_exporter._api_clients._constants import (
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
        all_results.extend(response["results"])

        while response["continuationToken"]:
            body["continuationToken"] = response["continuationToken"]
            response = await post_request(
                self.__query_results_url, body=body, headers=headers
            )
            all_results.extend(response["results"])

        return parse_obj_as(List[ResultResponse], all_results)
