import io
from typing import List, Tuple

from nisystemlink.utilities.data_exporter._api_clients._api_clients import ApiClients
from nisystemlink.utilities.data_exporter._api_clients._models import (
    ResultResponse,
    StepResponse,
)
from nisystemlink.utilities.data_exporter.parametric_data_exporter._dataframe_handles import (
    merge_dataframes,
    normalize_dataframe,
)
from nisystemlink.utilities.data_exporter.parametric_data_exporter._models import (
    QueryLinqFilter,
)


class ParametricDataExporter:

    def __init__(self, query_linq_filter: QueryLinqFilter):
        self.__api_clients = ApiClients()
        self.__query_linq_filter = query_linq_filter

    async def export_csv_data(self) -> io.BytesIO:
        results, steps = await self.__get_results_and_steps(self.__query_linq_filter)

        results_df = normalize_dataframe(
            [result.dict() for result in results], "result"
        )
        steps_df = normalize_dataframe([step.dict() for step in steps], "step")

        # getting all part numbers associated with the already queried results. using that to fetch products
        part_numbers = results_df["result_part_number"].unique()

        part_numbers_query = " || ".join(
            [f'partNumber== "{part_number}"' for part_number in part_numbers]
        )
        products = self.__api_clients.product_client.query_products(part_numbers_query)
        products_df = normalize_dataframe(
            [product.dict() for product in products], "product"
        )

        # merging all the data frames and creating a csv file out of it
        merged_product_result_step_df = merge_dataframes(
            results_df, steps_df, products_df
        )

        merged_product_result_step_df.to_csv(index=False)

        # constructing a name with part numbers and creating a csv file out of the merged data frame
        csv_file = io.BytesIO(
            merged_product_result_step_df.to_csv(index=False).encode()
        )

        return csv_file

    async def __get_results_and_steps(
        self, query_linq_filter: QueryLinqFilter
    ) -> Tuple[List[ResultResponse], List[StepResponse]]:
        """Get the results and steps based on the query linq filter.

        Args:
            query_linq_filter (Dict[str, str]): The query linq filter of the dataspace.

        Returns:
            Tuple[List[Dict], List[Dict]]: The results and steps based on the query linq filter.
        """
        steps_filter = query_linq_filter.filter
        results_filter = query_linq_filter.result_filter

        results = await self.__api_clients.results_client.query_results(results_filter)
        steps = await self.__api_clients.steps_client.query_steps(
            steps_filter, results_filter
        )

        return results, steps
