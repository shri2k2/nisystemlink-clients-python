from typing import Dict, List

from nisystemlink.utilities.data_exporter._api_clients._api_utilities import (
    post_request,
)
from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import (
    BaseHttpRoutes,
)
from nisystemlink.utilities.data_exporter._api_clients._constants._http_constants import (
    HttpConstants,
)
from nisystemlink.utilities.data_exporter._api_clients._constants._system_link_http_keys import (
    SystemLinkHttpKeys,
)


class StepsClient:
    __api_key: str | None

    __query_steps_url: str

    def __init__(self, api_key: str | None, systemlink_uri: str | None) -> None:
        self.__api_key = api_key

        self.__query_steps_url = (
            f"{systemlink_uri}{BaseHttpRoutes.TEST_MONITOR_BASE_ROUTE}/query-steps"
        )

    async def query_steps(self, steps_filter: str, results_filter: str) -> List[Dict]:
        """Makes a POST request to query the test steps.

        Args:
            steps_filter (str): Linq filter for the test steps
            results_filter (str): Linq filter for the test results

        Returns:
            List[Dict]: List of test steps
        """
        steps = []
        body = {
            "filter": steps_filter,
            "resultFilter": results_filter,
            "take": HttpConstants.TAKE,
            "orderBy": SystemLinkHttpKeys.UPDATED_AT,
        }
        if self.__api_key:
            headers = {"x-ni-api-key": self.__api_key}
        response = await post_request(
            self.__query_steps_url, body=body, headers=headers
        )

        while response["continuationToken"]:
            steps = steps + response["steps"]
            body["continuationToken"] = response["continuationToken"]
            response = await post_request(
                self.__query_steps_url, body=body, headers=headers
            )

        return steps
