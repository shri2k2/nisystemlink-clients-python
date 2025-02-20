import io
from typing import Dict, List
from nisystemlink.utilities.data_exporter._api_clients._api_clients import ApiClients
from nisystemlink.utilities.data_exporter.specs_exporter._dataframe_handles import serialize_specs


class SpecsExporter:
    __api_clients: ApiClients
    __workspaces: List[Dict]
    __users : List[Dict]

    def __init__(self) -> None:
        self.__api_clients = ApiClients()
        self.__workspaces = self.__api_clients.auth_client.get_workspaces()
        self.__users = self.__api_clients.user_client.get_users()

    def export_csv_data(self, product_id: str) -> None:
        product_part_number = self.__api_clients.product_client.get_product_part_number(product_id=product_id)

        specs = self.__api_clients.spec_client.query_specs(product_ids=[product_id])

        specs_df = serialize_specs(specs=specs, product_part_number=product_part_number, workspaces=self.__workspaces, users=self.__users)

        csv_file = io.BytesIO(specs_df.to_csv(index=False).encode())
