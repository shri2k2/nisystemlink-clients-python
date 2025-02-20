from typing import Dict, List
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient as SystemLinkSpecClient
from nisystemlink.clients.spec.models._query_specs import QuerySpecifications, QuerySpecificationsRequest

class SpecClient:
    __api_key: str | None
    __systemlink_uri: str | None

    __spec_client: SystemLinkSpecClient

    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        self.__api_key = api_key
        self.__systemlink_uri = systemlink_uri

        self.__initialize_spec_client()

    def __initialize_spec_client(self) -> None:
        if self.__api_key and self.__systemlink_uri:
            server_configuration = HttpConfiguration(
                server_uri=self.__systemlink_uri, api_key=self.__api_key
            )
            self.__spec_client = SystemLinkSpecClient(server_configuration)
        else:
            self.__spec_client = SystemLinkSpecClient()

    def query_specs(self, product_ids: List[str]) -> QuerySpecifications:
        spec_response = self.__spec_client.query_specs(
            QuerySpecificationsRequest(
                product_ids=product_ids,
                take=1000
            )
        )
        specs = spec_response.specs

        while spec_response.continuation_token:
            continuation_token = spec_response.continuation_token
            spec_response = self.__spec_client.query_specs(
                QuerySpecificationsRequest(
                    product_ids=product_ids,
                    take=1000,
                    continuation_token=continuation_token
                )
            )

            specs.extend(spec_response.specs)

        return specs
