import os

from nisystemlink.utilities.data_exporter._api_clients._clients._product_client import (
    ProductClient,
)
from nisystemlink.utilities.data_exporter._api_clients._clients._results_client import (
    ResultsClient,
)
from nisystemlink.utilities.data_exporter._api_clients._clients._steps_client import (
    StepsClient,
)
from nisystemlink.utilities.data_exporter._api_clients._clients._webapps_client import (
    WebAppsClient,
)


class ApiClients:
    __api_key: str | None
    __systemlink_uri: str | None

    # clients from ni-systemlink (configuration done in the ProductClient in clients)
    product_client: ProductClient

    # clients that we have developed
    results_client: ResultsClient
    steps_client: StepsClient
    webapps_client: WebAppsClient

    def __init__(self) -> None:
        self.__api_key = os.getenv("SYSTEMLINK_API_KEY")
        self.__systemlink_uri = os.getenv("SYSTEMLINK_HTTP_URI")

        self.__initialize_clients()

    def __initialize_clients(self) -> None:
        self.product_client = ProductClient(self.__api_key, self.__systemlink_uri or "")
        self.results_client = ResultsClient(self.__api_key, self.__systemlink_uri or "")
        self.steps_client = StepsClient(self.__api_key, self.__systemlink_uri or "")
        self.webapps_client = WebAppsClient(self.__api_key, self.__systemlink_uri or "")
