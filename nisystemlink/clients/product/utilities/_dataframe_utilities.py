from typing import List, Optional

import pandas as pd
from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.product.models import (
    ProductProjection,
    ProductResponse,
    QueryProductsRequest,
)
from pandas import DataFrame


def __query_products_batched(
    product_client: ProductClient,
    products_query_filter: str,
    column_projection: Optional[List[ProductProjection]] = None,
) -> List[ProductResponse]:
    """Queries products in batches from the product client.

    Args:
        product_client (ProductClient): The product client instance used to fetch product data.
        products_query_filter (str): The linq filter used to query products.
        column_projection (Optional[List[ProductProjection]]): A list of specific fields to retrieve.
            Defaults to None, which retrieves all fields.

    Returns:
        List[ProductResponse]: A list of product responses retrieved from the API.
    """
    products_query = QueryProductsRequest(
        filter=products_query_filter,
        projection=column_projection,
        take=1000,
    )

    all_products: List[ProductResponse] = []

    response = product_client.query_products_paged(products_query)
    all_products.extend(response.products)
    while response.continuation_token:
        products_query.continuation_token = response.continuation_token
        response = product_client.query_products_paged(products_query)
        all_products.extend(response.products)

    return all_products


def __normalize_products(products: List[ProductResponse]) -> DataFrame:
    """Normalizes product data from a list of product responses into a structured DataFrame.

    Args:
        products (List[ProductResponse]): A list of product responses retrieved from the API.

    Returns:
        DataFrame: A Pandas DataFrame containing the normalized product data.
    """
    products_dict_representation = [
        product.dict(exclude_unset=True) for product in products
    ]
    normalized_df = pd.json_normalize(products_dict_representation, sep=".")

    return normalized_df


def get_products_dataframe(
    product_client: ProductClient,
    products_query_filter: str,
    column_projection: Optional[List[ProductProjection]] = None,
) -> DataFrame:
    """Fetches products as Pandas DataFrame.

    Args:
        product_client (ProductClient): The product client instance used to fetch product data.
        products_query_filter (str): The product linq filter used to query products.
        column_projection (Optional[List[ProductProjection]]): A list of specific product fields to retrieve.
                - Mention only the `list of fields` which are to be retrieved.
                - If `left out` or given `None`, it retrieves all the fields.
                - If given with an `empty array`, it excludes all the fields

    Returns:
        DataFrame: A Pandas DataFrame containing the product data.
    """
    products = __query_products_batched(
        product_client, products_query_filter, column_projection
    )

    products_dataframe = __normalize_products(products)

    return products_dataframe
