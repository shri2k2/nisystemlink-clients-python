from typing import List, Optional

import pandas as pd
from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductProjection,
)
from nisystemlink.clients.product.utilities._client_utilities import (
    __batch_query_products,
)
from nisystemlink.clients.product.utilities._constants import HttpConstants
from pandas import DataFrame


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

    Raises:
        ApiException: If unable to communicate with the ``/nitestmonitor`` service
            or provided an invalid argument.
    """
    products = __batch_query_products(
        product_client,
        products_query_filter,
        column_projection,
        take=HttpConstants.DEFAULT_QUERY_PRODUCTS_TAKE,
    )

    products_dataframe = __normalize_products(products)

    return products_dataframe


def __normalize_products(products: List[Product]) -> DataFrame:
    """Normalizes product data from a list of product responses into a structured DataFrame.

    Args:
        products (List[Product]): A list of product responses retrieved from the API.

    Returns:
        DataFrame: A Pandas DataFrame containing the normalized product data.
    """
    products_dict_representation = [
        product.dict(exclude_unset=True) for product in products
    ]
    normalized_dataframe = pd.json_normalize(products_dict_representation, sep=".")
    normalized_dataframe.dropna(axis="columns", how="all", inplace=True)

    return normalized_dataframe
