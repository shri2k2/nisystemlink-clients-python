from typing import Dict, List
from nisystemlink.utilities.data_exporter._api_clients._api_utilities import get_request
from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import BaseHttpRoutes


class AuthClient:
    __api_key: str | None

    __get_auth_content_url: str

    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        self.__api_key = api_key

        self.__get_auth_content_url = f"{systemlink_uri}{BaseHttpRoutes.USER_APIS_ROUTE}/v1/users/query"

    async def get_workspaces(self) -> List[Dict]:
        workspaces = {}

        auth_response = await get_request(url=self.__get_auth_content_url)

        for workspace in auth_response["workspaces"]:
            workspaces[workspace["id"]] = workspace["name"]

        return workspaces
