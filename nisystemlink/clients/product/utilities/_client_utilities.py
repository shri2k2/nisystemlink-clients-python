from typing import List, Optional

from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductProjection,
    QueryProductsRequest,
)
from nisystemlink.clients.product.utilities._constants import HttpConstants


def __query_products_batched(
    product_client: ProductClient,
    products_query_filter: str,
    column_projection: Optional[List[ProductProjection]] = None,
    take: int = HttpConstants.DEFAULT_QUERY_PRODUCTS_TAKE,
) -> List[Product]:
    """Queries products in batches from the product client.

    Args:
        product_client (ProductClient): The product client instance used to fetch product data.
        products_query_filter (str): The linq filter used to query products.
        column_projection (Optional[List[ProductProjection]]): A list of specific fields to retrieve.
            Defaults to None, which retrieves all fields.
        take (Optional[int]): The maximum number of products to query per batch.

    Returns:
        List[Product]: A list of product responses retrieved from the API.

    Raises:
        ApiException: If unable to communicate with the ``/nitestmonitor`` service
            or provided an invalid argument.
    """
    products_query = QueryProductsRequest(
        filter=products_query_filter,
        projection=column_projection,
        take=take,
    )

    all_products: List[Product] = []

    response = product_client.query_products_paged(products_query)
    all_products.extend(response.products)
    while response.continuation_token:
        products_query.continuation_token = response.continuation_token
        response = product_client.query_products_paged(products_query)
        all_products.extend(response.products)

    return all_products
