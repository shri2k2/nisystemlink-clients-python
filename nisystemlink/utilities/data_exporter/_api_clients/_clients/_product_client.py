from typing import List, Optional

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.product import ProductClient as SystemLinkProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductField,
    QueryProductsRequest,
)
from nisystemlink.utilities.data_exporter._api_clients._constants import (
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
        products_query = QueryProductsRequest(
            filter=products_filter,
            order_by=ProductField.UPDATED_AT,
            take=HttpConstants.TAKE,
        )

        all_products = []

        response = self.__product_client.query_products_paged(products_query)
        all_products.extend(response.products)

        while response.continuation_token:
            products_query.continuation_token = response.continuation_token
            response = self.__product_client.query_products_paged(products_query)
            all_products.extend(response.products)

        return all_products

    def get_product_part_number(self, product_id: str) -> str:
        """Gets product's part number.

        Args:
            product_id: ID of the product.

        Returns:
            Part Number of the product with the specified product ID.
        """
        product_response = self.__product_client.get_product(id=product_id)

        return product_response.part_number
