from data_exporter.core.constants import ColumnGroup
from data_exporter.core.constants._product_columns import product_columns
from data_exporter.core.constants._result_columns import result_columns
from data_exporter.core.constants._step_columns import step_columns

import pandas as pd
from pandas import DataFrame
from typing import Any, Dict, List

def __group_columns(df_columns: List[str]) -> Dict[str, List]:
    """Gets the list of columns in the dataframe and group them under various categories"""
    grouped_columns = {
        ColumnGroup.PROPERTIES: [],
        ColumnGroup.STATUS_TYPE_SUMMARY: [],
        ColumnGroup.DATA: [],
        ColumnGroup.INPUTS: [],
        ColumnGroup.OUTPUTS: []
    }

    for column in df_columns:
        if ColumnGroup.DATA in column:
            grouped_columns[ColumnGroup.DATA].append(column)
        elif ColumnGroup.INPUTS in column:
            grouped_columns[ColumnGroup.INPUTS].append(column)
        elif ColumnGroup.OUTPUTS in column:
            grouped_columns[ColumnGroup.OUTPUTS].append(column)
        elif ColumnGroup.PROPERTIES in column:
            grouped_columns[ColumnGroup.PROPERTIES].append(column)
        elif ColumnGroup.STATUS_TYPE_SUMMARY in column:
            grouped_columns[ColumnGroup.STATUS_TYPE_SUMMARY].append(column)
    
    return grouped_columns

def __reorder_columns(prefix: str, df_normalized: DataFrame) -> DataFrame:
    df_columns = df_normalized.columns
    grouped_columns = __group_columns(df_columns)

    final_columns_order = []

    if prefix == 'product':
        final_columns_order = product_columns + grouped_columns[ColumnGroup.PROPERTIES]
    elif prefix == 'result':
        final_columns_order = result_columns + grouped_columns[ColumnGroup.STATUS_TYPE_SUMMARY] + grouped_columns[ColumnGroup.PROPERTIES]
    elif prefix == 'step':
        final_columns_order = step_columns + grouped_columns[ColumnGroup.INPUTS] + grouped_columns[ColumnGroup.OUTPUTS] + grouped_columns[ColumnGroup.DATA] + grouped_columns[ColumnGroup.PROPERTIES]
    
    return df_normalized.reindex(columns=final_columns_order)

def __post_process_normalized_df(normalized_df: DataFrame, prefix: str) -> DataFrame:
    # adding prefix
    normalized_df.columns = [f"{prefix}_{col}" for col in normalized_df.columns]

    # reorders the dataframe based on the given configuration
    normalized_df = __reorder_columns(prefix, normalized_df)

    # Remove columns that are completely empty (if any) after all transformations
    normalized_df.dropna(axis=1, how='all', inplace=True)

    return normalized_df

def __restructure_steps(steps: List) -> List:

    def process_io(io_list: List) -> Dict:
        return {io["name"]: io["value"] for io in io_list}

    for step in steps:
        step["inputs"] = process_io(step.get("inputs", []))
        step["outputs"] = process_io(step.get("outputs", []))

    return steps

def normalize_dataframe(df: List[Dict[str, Any]], prefix: str) -> pd.DataFrame:
    """
    Normalize the dataframe and add a prefix to the columns.

    Args:
        df (List[Dict[str, Any]]): The list of dictionaries to be converted to a dataframe.
        prefix (str): The prefix to be added to the columns.

    Returns:
        pd.DataFrame: The normalized dataframe.
    """
    if prefix == 'step':
        steps = __restructure_steps(df)

        steps_df = DataFrame(pd.json_normalize(steps, sep='.'))
        steps_parameters_df = pd.json_normalize(
            steps,
            record_path=['data', 'parameters'],
            record_prefix="data.parameters.",
            meta=['step_id', 'result_id']
        )

        # merged data frame - merged with the parameters
        steps_merged_df = pd.merge(
            steps_df, steps_parameters_df,
            left_on=['result_id', 'step_id'], right_on=['result_id', 'step_id'],
            how='left'
        )
        steps_merged_df.drop("data.parameters", axis=1, inplace=True)

        return __post_process_normalized_df(steps_merged_df, prefix)
    else:
        # either product or result
        normalized_df = DataFrame(pd.json_normalize(df, sep='.'))

        return __post_process_normalized_df(normalized_df, prefix)

def merge_dataframes(results_df: DataFrame, steps_df: DataFrame, products_df: DataFrame) -> DataFrame:
    """
    Merge the results, steps and products dataframes.

    Args:
        results_df (DataFrame): The results dataframe.
        steps_df (DataFrame): The steps dataframe.
        products_df (DataFrame): The products dataframe.

    Returns:
        DataFrame: The merged dataframe.
    """
    merged_product_result_df = pd.merge(products_df, results_df, left_on='product_part_number', right_on='result_part_number', how='inner')
    merged_product_result_step_df = pd.merge(merged_product_result_df, steps_df, left_on='result_id', right_on='step_result_id', how='inner')

    return merged_product_result_step_df