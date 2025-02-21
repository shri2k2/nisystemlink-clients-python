from typing import Dict, List

from nisystemlink.utilities.data_exporter._api_clients._api_utilities import get_request
from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import (
    BaseHttpRoutes,
)


class AuthClient:
    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        """Initialize an instance.

        Args:
            api_key: API Key for the SystemLink APIs.
            systemlink_uri: SystemLink APIs base url.
        """
        self.__api_key = api_key

        self.__get_auth_content_url = (
            f"{systemlink_uri}{BaseHttpRoutes.AUTH_APIS_ROUTE}/v1/auth"
        )

    def __get_headers(self) -> str:
        """Gets Headers.

        Returns:
            Returns headers with the api key if __api_key is no null.
        """
        return {"x-ni-api-key": self.__api_key} if self.__api_key else {}

    async def get_workspaces(self) -> List[Dict]:
        """Gets all workspaces.

        Returns:
            The list of workspaces to which the user has access to as a dictionary {workspace_id: workspace_name}.
        """
        workspaces = {}

        headers = self.__get_headers()

        auth_response = await get_request(
            url=self.__get_auth_content_url, headers=headers
        )

        for workspace in auth_response["workspaces"]:
            workspaces[workspace["id"]] = workspace["name"]

        return workspaces
