from typing import List, Optional

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient as SystemLinkSpecClient
from nisystemlink.clients.spec.models._query_specs import QuerySpecificationsRequest
from nisystemlink.clients.spec.models._specification import SpecificationWithHistory


class SpecClient:
    def __init__(
        self, api_key: Optional[str] = None, systemlink_uri: Optional[str] = None
    ) -> None:
        """Initialize an instance.

        Args:
            api_key: API Key for the SystemLink APIs.
            systemlink_uri: SystemLink APIs base url.
        """
        self.__api_key = api_key
        self.__systemlink_uri = systemlink_uri

        self.__initialize_spec_client()

    def __initialize_spec_client(self) -> None:
        """Initialize SystemLink Spec Client Instance."""
        if self.__api_key and self.__systemlink_uri:
            server_configuration = HttpConfiguration(
                server_uri=self.__systemlink_uri, api_key=self.__api_key
            )
            self.__spec_client = SystemLinkSpecClient(server_configuration)
        else:
            self.__spec_client = SystemLinkSpecClient()

    def query_specs(self, product_ids: List[str]) -> List[SpecificationWithHistory]:
        """Query specs of a specific product.

        Args:
            product_ids: ID od the product to query specs.

        Returns:
            The list of specs of the specified product.
        """
        spec_response = self.__spec_client.query_specs(
            QuerySpecificationsRequest(
                product_ids=product_ids,
                take=1000,
            )
        )
        specs = spec_response.specs if spec_response.specs else []

        while spec_response.continuation_token:
            continuation_token = spec_response.continuation_token
            spec_response = self.__spec_client.query_specs(
                QuerySpecificationsRequest(
                    product_ids=product_ids,
                    take=1000,
                    continuation_token=continuation_token,
                )
            )

            specs.extend(spec_response.specs if spec_response.specs else [])

        return specs
