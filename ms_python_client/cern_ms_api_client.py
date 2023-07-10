from typing import Optional

from ms_python_client.components.events.cern_events_component import (
    CERNEventsComponents,
)
from ms_python_client.ms_api_client import MSApiClient
from ms_python_client.utils import init_from_env


class CERNMSApiClient(MSApiClient):
    def __init__(
        self,
        account_id: str,
        client_id: str,
        client_secret: str,
        api_endpoint: str = "https://graph.microsoft.com/v1.0",
        use_path: Optional[str] = None,
    ):
        super().__init__(account_id, client_id, client_secret, api_endpoint, use_path)
        self.init_components()

    def init_components(self):
        # Add all the new components here
        self.events = CERNEventsComponents(self)

    @staticmethod
    def init_from_dotenv(
        custom_dotenv=".env", use_path: Optional[str] = None
    ) -> "CERNMSApiClient":
        init_from_env.init_from_dotenv(custom_dotenv)
        ms_client = CERNMSApiClient.init_from_env(use_path=use_path)
        return ms_client

    @staticmethod
    def init_from_env(use_path: Optional[str] = None) -> "CERNMSApiClient":
        values = init_from_env.init_from_env(use_path)
        ms_client = CERNMSApiClient(
            values["account_id"],
            values["client_id"],
            values["client_secret"],
            use_path=values["use_path"],
        )
        return ms_client
