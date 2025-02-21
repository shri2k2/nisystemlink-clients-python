import io

from nisystemlink.utilities.data_exporter._api_clients._api_clients import ApiClients
from nisystemlink.utilities.data_exporter.specs_exporter._dataframe_handles import (
    serialize_specs,
)


class SpecsExporter:
    def __init__(self) -> None:
        """Initialize an instance."""
        self.__api_clients = ApiClients()

    async def export_csv_data(self, product_id: str) -> io.BytesIO:
        """Export Specs Detials into a csv file.

        Args:
            product_id: ID of the product to export specs.

        Returns:
            CSV file with specs details of the specified product.
        """
        product_part_number = self.__api_clients.product_client.get_product_part_number(
            product_id=product_id
        )

        specs = self.__api_clients.spec_client.query_specs(product_ids=[product_id])

        workspaces = await self.__api_clients.auth_client.get_workspaces()
        users = await self.__api_clients.user_client.get_users()

        specs_df = serialize_specs(
            specs=specs,
            product_part_number=product_part_number,
            workspaces=workspaces,
            users=users,
        )

        csv_file = io.BytesIO(specs_df.to_csv(index=False).encode())

        return csv_file
