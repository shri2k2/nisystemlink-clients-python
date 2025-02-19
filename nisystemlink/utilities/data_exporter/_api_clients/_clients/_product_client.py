from typing import List

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.product import ProductClient as SystemLinkProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductField,
    QueryProductsRequest,
)
from nisystemlink.utilities.data_exporter._api_clients._constants._http_constants import (
    HttpConstants,
)


class ProductClient:
    __api_key: str | None
    __systemlink_uri: str | None

    __product_client: SystemLinkProductClient

    def __init__(self, api_key: str | None, systemlink_uri: str | None) -> None:
        self.__api_key = api_key
        self.__systemlink_uri = systemlink_uri

        self.__initialize_product_client()

    def __initialize_product_client(self) -> None:
        if self.__api_key and self.__systemlink_uri:
            server_configuration = HttpConfiguration(
                server_uri=self.__systemlink_uri, api_key=self.__api_key
            )
            self.__product_client = SystemLinkProductClient(server_configuration)
        else:
            self.__product_client = SystemLinkProductClient()

    def query_products(self, products_filter: str) -> List[Product]:
        """Queries the products based on the filter provided.

        Args:
            products_filter (str): The filter to be applied to the products.

        Returns:
            List[Product]: The list of products that match the filter.
        """
        products_query = QueryProductsRequest(
            filter=products_filter,
            order_by=ProductField.UPDATED_AT,
            take=HttpConstants.TAKE,
        )
        response = self.__product_client.query_products_paged(products_query)
        all_products = response.products

        while response.continuation_token:
            products_query.continuation_token = response.continuation_token
            response = self.__product_client.query_products_paged(products_query)
            all_products.extend(response.products)

        return all_products
