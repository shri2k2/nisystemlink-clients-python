from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import BaseHttpRoutes
from nisystemlink.utilities.data_exporter._api_clients._constants._http_constants import HttpConstants
from nisystemlink.utilities.data_exporter._api_clients._constants._system_link_http_keys import SystemLinkHttpKeys
from nisystemlink.utilities.data_exporter._api_clients._api_utilities import get_request, post_request

from typing import Dict, List

class ResultsClient:
    __api_key: str | None

    __query_result_by_id_url: str
    __query_results_url: str

    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        self.__api_key = api_key

        self.__query_result_by_id_url = f"{systemlink_uri}{BaseHttpRoutes.TEST_MONITOR_BASE_ROUTE}/results/{{result_id}}"
        self.__query_results_url = f"{systemlink_uri}{BaseHttpRoutes.TEST_MONITOR_BASE_ROUTE}/query-results"
    
    async def query_result_by_id(self, result_id: str) -> Dict:
        """
        Makes a GET request to retrieve the result by id.

        Args:
            result_id (str): ID of the test result

        Returns:
            Dict: Test result
        """
        if self.__api_key:
            headers = {'x-ni-api-key': self.__api_key}
        response = await get_request(self.__query_result_by_id_url.format(result_id=result_id), headers)

        return response

    async def query_results(self, results_filter: str) -> List[Dict]:
        """
        Makes a POST request to query the test results.

        Args:
            results_filter (str): Linq filter for the test results

        Returns:
            List[Dict]: List of test results
        """
        results = []
        body = {"filter": results_filter, "take": HttpConstants.TAKE, "orderBy": SystemLinkHttpKeys.UPDATED_AT}
        if self.__api_key:
            headers = {'x-ni-api-key': self.__api_key}
        response = await post_request(self.__query_results_url, body=body, headers=headers)

        while response["continuationToken"]:
            results = results + response["results"]
            body["continuationToken"] = response["continuationToken"]
            response = await post_request(self.__query_results_url, body=body, headers=headers)

        return results