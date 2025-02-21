from typing import Dict, List

from nisystemlink.utilities.data_exporter._api_clients._api_utilities import (
    post_request,
)
from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import (
    BaseHttpRoutes,
)


class UserClient:
    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        """Initialize an instance.

        Args:
            api_key: API Key for the SystemLink APIs.
            systemlink_uri: SystemLink APIs base url.
        """
        self.__api_key = api_key

        self.__query_users_url = (
            f"{systemlink_uri}{BaseHttpRoutes.USER_APIS_ROUTE}/v1/users/query"
        )

    def __get_headers(self):
        """Gets Headers.

        Returns:
            Returns headers with the api key if __api_key is no null.
        """
        return {"x-ni-api-key": self.__api_key} if self.__api_key else {}

    async def __query_users(self) -> List[Dict]:
        """Query all users.

        Returns:
            The list of all users.
        """
        headers = self.__get_headers()

        users_response = await post_request(
            url=self.__query_users_url,
            headers=headers,
            body={
                "take": 100,
            },
        )
        users_object = users_response["users"]
        continuation_token = users_response["continuationToken"]

        while continuation_token:
            users_response = await post_request(
                url=self.__query_users_url,
                headers=headers,
                body={"take": 100, "continuationToken": continuation_token},
            )

            users_object.extend(users_response["users"])
            continuation_token = users_response["continuationToken"]

        return users_object

    async def get_users(self) -> List[Dict]:
        """Gets all users.

        Returns:
            The list of all users as a dictionary {users_id: first_name = last_name}.
        """
        users = {}

        users_object = await self.__query_users()

        for user in users_object:
            users[user["id"]] = " ".join([user["firstName"], user["lastName"]])

        return users
