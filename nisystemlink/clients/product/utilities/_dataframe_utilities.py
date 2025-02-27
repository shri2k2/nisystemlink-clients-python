from typing import Any, Dict, List, Optional

import pandas as pd
from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.product.models import (
    ProductOrderBy,
    ProductProjection,
    ProductResponse,
    QueryProductsRequest,
)
from nisystemlink.clients.product.utilities._constants import HttpConstants
from pandas import DataFrame


def __query_products_batched(
    product_client: ProductClient,
    products_query_filter: str,
    column_projection: Optional[List[ProductProjection]] = None,
) -> List[ProductResponse]:
    """Queries products in batches from the product client.

    Args:
        product_client (ProductClient): The product client instance used to fetch product data.
        products_query_filter (str): The filter string used to query products.
        column_projection (Optional[List[ProductProjection]]): A list of specific fields to retrieve.
            Defaults to None, which retrieves all fields.

    Returns:
        List[ProductResponse]: A list of product responses retrieved from the API.
    """
    products_query = QueryProductsRequest(
        filter=products_query_filter,
        order_by=ProductOrderBy.UPDATED_AT,
        projection=column_projection,
        take=HttpConstants.TAKE,
    )

    all_products: List[ProductResponse] = []

    response = product_client.query_products_paged(products_query)

    all_products.extend(response.products)

    while response.continuation_token:
        products_query.continuation_token = response.continuation_token
        response = product_client.query_products_paged(products_query)

        all_products.extend(response.products)

    return all_products


def __reorder_columns(
    df_columns: List[str], column_projection: Optional[List[ProductProjection]] = None
) -> List[str]:
    """Make sure to include only the fields from column projection. Reorders DataFrame columns to ensure
    `properties` fields are grouped together. The properties are placed at the last after all the
    remaining columns.

    When there are multiple products with different properties, in the process of normalization, the new
    properties would be added as the last column of the dataframe. This leads to inconsistency in the arrangement
    of properties. This is the reason to group properties together.

    Args:
        df_columns (List[str]): A list of DataFrame column names.
        column_projection (Optional[List[ProductProjection]]): A list of specific product fields to retrieve.

    Returns:
        List[str]: The reordered list of column names.
    """
    properties_columns: List[str] = []
    remaining_columns: List[str] = []

    for column in df_columns:
        """if there are fields mentioned in the column_projection, then only those columns has to be there
        in the dataframe
        """
        if column_projection and (
            column.upper() not in column_projection
            and not (
                ProductProjection.PROPERTIES.lower() in column
                and ProductProjection.PROPERTIES in column_projection
            )
        ):
            continue

        # grouping the columns either as properties or remaining general columns
        (
            properties_columns
            if ProductProjection.PROPERTIES.lower() in column
            else remaining_columns
        ).append(column)

    return remaining_columns + properties_columns


def __normalize_products(
    products: List[Dict[str, Any]],
    column_projection: Optional[List[ProductProjection]] = None,
) -> DataFrame:
    """Normalizes product data from a list of dictionaries into a structured DataFrame.

    Args:
        products (List[Dict[str, Any]]): A list of dictionaries representing product data.
        column_projection (Optional[List[ProductProjection]]): A list of specific product fields to retrieve.

    Returns:
        DataFrame: A Pandas DataFrame containing the normalized product data.
    """
    normalized_df = pd.json_normalize(products, sep=".")

    reordered_columns = __reorder_columns(normalized_df.columns, column_projection)

    return normalized_df.reindex(columns=reordered_columns)


def get_products_dataframe(
    product_client: ProductClient,
    products_query_filter: str,
    column_projection: Optional[List[ProductProjection]] = None,
) -> DataFrame:
    """Fetches and normalizes products data into a Pandas DataFrame.

    Args:
        product_client (ProductClient): The product client instance used to fetch product data.
        products_query_filter (str): The filter string used to query products.
        column_projection (Optional[List[ProductProjection]]): A list of specific product fields to retrieve.
                - Mention only the `list of fields` which are to be retrieved.
                - If `left out` or given `None` or given an `empty array`, it retrieves all the fields.

    Returns:
        DataFrame: A Pandas DataFrame containing the product data.
    """
    # Converting empty list to None. Considering empty list given from user as they wish to exclude nothing.
    if column_projection == []:
        column_projection = None

    products = __query_products_batched(
        product_client, products_query_filter, column_projection
    )

    products_dataframe = __normalize_products(
        [product.dict() for product in products], column_projection
    )

    return products_dataframe
