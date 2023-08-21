import logging
import os
from typing import Any, Mapping, Optional

import requests

from ms_python_client.api_client import ApiClient
from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.components.users.users_component import UsersComponent
from ms_python_client.config import Config
from ms_python_client.interfaces.ms_client_interface import MSClientInterface
from ms_python_client.services.oauth2_flow import Oauth2Flow
from ms_python_client.utils import init_from_env

logging.getLogger("ms_python_client").addHandler(logging.NullHandler())
logger = logging.getLogger("ms_python_client")

_Data = Mapping[str, Any]
_Headers = Mapping[str, str]


class MSApiClient(MSClientInterface):
    @staticmethod
    def init_from_env() -> "MSApiClient":
        config = init_from_env.init_from_env()
        ms_client = MSApiClient(config)
        return ms_client

    @staticmethod
    def init_from_dotenv(
        custom_dotenv=".env",
    ) -> "MSApiClient":
        init_from_env.init_from_dotenv(custom_dotenv)
        ms_client = MSApiClient.init_from_env()
        return ms_client

    def init_components(self):
        # Add all the new components here
        self.events = EventsComponent(self)
        self.users = UsersComponent(self)

    def __init__(
        self,
        config: Config,
        api_endpoint: str = "https://graph.microsoft.com/v1.0",
    ):
        if "MS_ACCESS_TOKEN" in os.environ and os.getenv("MS_ACCESS_TOKEN") != "":
            self.dev_token = os.environ["MS_ACCESS_TOKEN"]
        else:
            self.dev_token = None
            self.oauth = Oauth2Flow(config)

        self.api_client = ApiClient(api_base_url=api_endpoint)
        self.init_components()

    def build_headers(self, extra_headers: Optional[_Headers] = None) -> _Headers:
        if self.dev_token:
            token = self.dev_token
        else:
            token = self.oauth.get_access_token()[0]

        headers = self.api_client.build_headers(
            extra_headers={"Authorization": f"Bearer {token}"}
        )
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def build_query_string_from_dict(
        self, parameters: Optional[Mapping[str, str]]
    ) -> str:
        query_string = "?"
        for key, value in parameters.items() if parameters else []:
            if value:
                query_string += f"{key}={value}&"
        return query_string[:-1]

    def make_get_request(
        self,
        api_path: str,
        parameters: Optional[Mapping[str, str]] = None,
        extra_headers: Optional[_Headers] = None,
    ) -> requests.Response:
        headers = self.build_headers(extra_headers)
        query_string = self.build_query_string_from_dict(parameters)

        response = self.api_client.make_get_request(
            api_path=f"{api_path}{query_string}",
            headers=headers,
        )

        return response

    def make_post_request(
        self, api_path: str, json: _Data, extra_headers: Optional[_Headers] = None
    ) -> requests.Response:
        headers = self.build_headers(extra_headers)

        response = self.api_client.make_post_request(
            api_path=api_path, headers=headers, json=json
        )

        return response

    def make_patch_request(
        self, api_path: str, json: _Data, extra_headers: Optional[_Headers] = None
    ) -> requests.Response:
        headers = self.build_headers(extra_headers)

        response = self.api_client.make_patch_request(
            api_path=api_path, headers=headers, json=json
        )

        return response

    def make_delete_request(
        self, api_path: str, extra_headers: Optional[_Headers] = None
    ) -> requests.Response:
        headers = self.build_headers(extra_headers)

        response = self.api_client.make_delete_request(
            api_path=api_path, headers=headers
        )

        return response
