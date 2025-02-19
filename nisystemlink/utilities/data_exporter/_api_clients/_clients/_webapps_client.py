from nisystemlink.utilities.data_exporter._api_clients._constants._base_http_routes import BaseHttpRoutes
from nisystemlink.utilities.data_exporter._api_clients._constants._user_exception_messages import UserExceptionMessages
from nisystemlink.utilities.data_exporter._api_clients._models._webapp_content import WebappContent
from nisystemlink.utilities.data_exporter._api_clients._models._webapp_meta_data import WebappMetaData
from nisystemlink.utilities.data_exporter._api_clients._api_utilities import get_request, post_request

class WebAppsClient:
    __api_key: str | None

    __query_webapps_url: str
    __get_webapp_content_url: str

    def __init__(self, api_key: str, systemlink_uri: str) -> None:
        self.__api_key = api_key

        self.__query_webapps_url = f"{systemlink_uri}{BaseHttpRoutes.WEBAPPS_BASE_ROUTE}/query"
        self.__get_webapp_content_url = f"{systemlink_uri}{BaseHttpRoutes.WEBAPPS_BASE_ROUTE}/{{webapp_id}}/content"

    async def get_webapp_metadata(self, dataspace_name: str, workspace_id: str) -> WebappMetaData:
        """
        Makes a POST request to query for the metadata of a webapp.

        Args:
            dataspace_name (str): Name of the dataspace
            workspace_id (str): Workspace ID of the product

        Raises:
            Exception: Dataspace not found

        Returns:
            WebappMetaData: Metadata of the webapp
        """

        body = {"filter": f"name == \"{dataspace_name}\" && type == \"DataSpace\" && workspace == \"{workspace_id}\""}
        if self.__api_key:
            headers = {'x-ni-api-key': self.__api_key}
        webapps = await post_request(self.__query_webapps_url, body=body, headers=headers)

        if not webapps["webapps"]:
            raise Exception(UserExceptionMessages.DATASPACE_NOT_FOUND.format(dataspace_name=dataspace_name))
        webapp_metadata = WebappMetaData.parse_obj(webapps["webapps"][0])

        return webapp_metadata

    async def get_webapp_content(self, webapp_id: str) -> WebappContent:
        """
        Makes a GET request to retrieve the content of a webapp.

        Args:
            webapp_id (str): Id of the webapp

        Returns:
            WebappContent: Content of the webapp
        """

        if self.__api_key:
            headers = {'x-ni-api-key': self.__api_key}
        webapp_content = await get_request(
            f"{self.__get_webapp_content_url.format(webapp_id=webapp_id)}",
            headers
        )

        return WebappContent.parse_obj(webapp_content)