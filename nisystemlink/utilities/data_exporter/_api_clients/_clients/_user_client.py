from typing import Dict, List
from nisystemlink.utilities.data_exporter._api_clients._api_utilities import post_request
from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import (
    BaseHttpRoutes,
)


class UserClient:
    __api_key: str | None

    __query_users_url: str

    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        self.__api_key = api_key

        self.__query_users_url = f"{systemlink_uri}{BaseHttpRoutes.USER_APIS_ROUTE}/v1/users/query"

    async def __query_users(self) -> List[Dict]:
        users_response = await post_request(
                url=self.__query_users_url,
                body={
                    "take": 100,
                },
            )
        users_object = users_response["users"]
        continuation_token = users_response["continuationToken"]

        while continuation_token:
            users_response = await post_request(
                url=self.__query_users_url,
                body={"take": 100, "continuationToken": continuation_token},
            )

            users_object.extend(users_response["users"])
            continuation_token = users_response["continuationToken"]

        return users_object

    async def get_users(self) -> List[Dict]:
        users = {}

        users_object = await self.__query_users()

        for user in users_object:
            users[user["id"]] = " ".join([user["firstName"], user["lastName"]])

        return users
