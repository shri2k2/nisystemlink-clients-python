from typing import List, Optional

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.product import ProductClient as SystemLinkProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductField,
    QueryProductsRequest,
)
from nisystemlink.utilities.data_exporter._api_clients._api_exception import (
    ApiException,
)
from nisystemlink.utilities.data_exporter._api_clients._constants import (
    ApiExceptionMessages,
    HttpConstants,
)


class ProductClient:

    def __init__(
        self, api_key: Optional[str] = None, systemlink_uri: Optional[str] = None
    ) -> None:
        self.__api_key = api_key
        self.__systemlink_uri = systemlink_uri

        self.__product_client = self.__initialize_product_client()

    def __initialize_product_client(self) -> SystemLinkProductClient:
        if self.__api_key and self.__systemlink_uri:
            server_configuration = HttpConfiguration(
                server_uri=self.__systemlink_uri, api_key=self.__api_key
            )
            return SystemLinkProductClient(server_configuration)

        return SystemLinkProductClient()

    def query_products(self, products_filter: str) -> List[Product]:
        """Queries the products based on the filter provided.

        Args:
            products_filter (str): The filter to be applied to the products.

        Returns:
            List[Product]: The list of products that match the filter.
        """
        try:
            products_query = QueryProductsRequest(
                filter=products_filter,
                order_by=ProductField.UPDATED_AT,
                take=HttpConstants.TAKE,
            )

            all_products = []

            response = self.__product_client.query_products_paged(products_query)

            if not response or response.products is None:
                raise ApiException(
                    message=ApiExceptionMessages.FAILED_TO_RETRIEVE_PROPER_RESPONSE.format(
                        request_context="querying products"
                    ),
                    response=response,
                )

            all_products.extend(response.products)

            while response.continuation_token:
                products_query.continuation_token = response.continuation_token
                response = self.__product_client.query_products_paged(products_query)

                if not response or response.products is None:
                    raise ApiException(
                        message=ApiExceptionMessages.EMPTY_PAGINATION_RESPONSE.format(
                            request_context="querying products"
                        ),
                        response=response,
                    )

                all_products.extend(response.products)

            return all_products

        except ApiException:
            raise  # Re-raise API errors

        except Exception as exception:
            raise ApiException(
                message=ApiExceptionMessages.FAILED_API_REQUEST.format(
                    "query products"
                ),
                response=response,
            ) from exception
