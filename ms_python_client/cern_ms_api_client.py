from ms_python_client.components.events.cern_events_component import (
    CERNEventsComponents,
)
from ms_python_client.config import Config
from ms_python_client.ms_api_client import MSApiClient
from ms_python_client.utils import init_from_env


class CERNMSApiClient(MSApiClient):
    def __init__(
        self,
        config: Config,
        api_endpoint: str = "https://graph.microsoft.com/v1.0",
    ):
        super().__init__(config, api_endpoint)
        self.init_components()

    def init_components(self):
        # Add all the new components here
        self.events = CERNEventsComponents(self)

    @staticmethod
    def init_from_dotenv(custom_dotenv=".env") -> "CERNMSApiClient":
        init_from_env.init_from_dotenv(custom_dotenv)
        ms_client = CERNMSApiClient.init_from_env()
        return ms_client

    @staticmethod
    def init_from_env() -> "CERNMSApiClient":
        config = init_from_env.init_from_env()
        ms_client = CERNMSApiClient(config)
        return ms_client
