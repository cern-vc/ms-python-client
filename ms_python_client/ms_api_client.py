import atexit
import logging
import os
from typing import Any, Mapping, Optional

import requests
from msal import ConfidentialClientApplication, SerializableTokenCache

from ms_python_client.api_client import ApiClient
from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.components.users.users_component import UsersComponent
from ms_python_client.ms_client_interface import MSClientInterface
from ms_python_client.utils import init_from_env

logging.getLogger("ms_python_client").addHandler(logging.NullHandler())
logger = logging.getLogger("ms_python_client")

_Data = Mapping[str, Any]
_Headers = Mapping[str, str]


class MSApiClient(MSClientInterface):
    @staticmethod
    def init_from_env(use_path: Optional[str] = None) -> "MSApiClient":
        values = init_from_env.init_from_env(use_path)
        ms_client = MSApiClient(
            values["account_id"],
            values["client_id"],
            values["client_secret"],
            use_path=values["use_path"],
        )
        return ms_client

    @staticmethod
    def init_from_dotenv(
        custom_dotenv=".env",
        use_path: Optional[str] = None,
    ) -> "MSApiClient":
        init_from_env.init_from_dotenv(custom_dotenv)
        ms_client = MSApiClient.init_from_env(use_path=use_path)
        return ms_client

    def setup_cache(self, cache_path: str) -> SerializableTokenCache:
        cache = SerializableTokenCache()
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                cache.deserialize(f.read())
        atexit.register(
            lambda: self._write_cache(cache_path, cache)
            if cache.has_state_changed
            else None
        )
        return cache

    def _write_cache(self, cache_path: str, cache: SerializableTokenCache) -> None:
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(cache.serialize())

    def init_components(self):
        # Add all the new components here
        self.events = EventsComponent(self)
        self.users = UsersComponent(self)

    def __init__(
        self,
        account_id: str,
        client_id: str,
        client_secret: str,
        api_endpoint: str = "https://graph.microsoft.com/v1.0",
        use_path: Optional[str] = None,
    ):
        self.api_client = ApiClient(api_base_url=api_endpoint)
        if "MS_ACCESS_TOKEN" not in os.environ:
            self.app = ConfidentialClientApplication(
                client_id=client_id,
                authority=f"https://login.microsoftonline.com/{account_id}",
                client_credential=client_secret,
                token_cache=(
                    self.setup_cache(use_path + "/token_cache.bin")
                    if use_path
                    else None
                ),
            )
        self.init_components()

    def build_headers(self, extra_headers: Optional[_Headers] = None) -> _Headers:
        if "MS_ACCESS_TOKEN" in os.environ:
            token = {
                "access_token": os.environ["MS_ACCESS_TOKEN"],
            }
        else:
            result = self.app.acquire_token_silent(
                scopes=["https://graph.microsoft.com/.default"], account=None
            )
            if (not result) or "access_token" not in result:
                logger.debug(
                    "No suitable token exists in cache. Let's get a new one from AAD."
                )
                token = self.app.acquire_token_for_client(
                    scopes=["https://graph.microsoft.com/.default"]
                )
            else:
                token = result
        headers = self.api_client.build_headers(
            extra_headers={"Authorization": f"Bearer {token['access_token']}"}
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
