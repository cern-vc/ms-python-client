import os

import pytest
import responses

from ms_python_client.ms_api_client import MSApiClient
from ms_python_client.utils.init_from_env import MSClientEnvError
from tests.ms_python_client.base_test_case import (
    MOCK_TOKEN,
    TEST_API_ENDPOINT,
    BaseTest,
    mock_msal,
)


class TestMSApiClientInit(BaseTest):
    @mock_msal()
    def test_init_from_env(self):
        os.environ[
            "AZURE_AUTHORITY"
        ] = "https://login.microsoftonline.com/organizations"
        os.environ["AZURE_CLIENT_ID"] = "test"
        os.environ["AZURE_SCOPE"] = "Scope1,Scope2"

        client = MSApiClient.init_from_env()

        assert client is not None

    @mock_msal()
    def test_init_from_env_exception(self):
        with pytest.raises(MSClientEnvError):
            MSApiClient.init_from_env()

    @mock_msal()
    def test_init_from_dotenv(self):
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        assert client is not None

    @mock_msal()
    def test_build_headers(self):
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers()
        assert headers is not None
        assert headers["Authorization"] == f"Bearer {MOCK_TOKEN}"

    @mock_msal()
    def test_build_headers_with_extra_headers(self):
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers({"test": "test"})
        assert headers is not None
        assert headers["Authorization"] == f"Bearer {MOCK_TOKEN}"
        assert headers["test"] == "test"

    @mock_msal()
    def test_with_token(self):
        os.environ["MS_ACCESS_TOKEN"] = "test_token"
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers()
        assert headers is not None
        assert headers["Authorization"] == "Bearer test_token"


class TestMSApiClient(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        super().setUp()
        self.client = MSApiClient(self.config, api_endpoint=TEST_API_ENDPOINT)

    @responses.activate
    def test_get_request(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/ms",
            json={"response": "ok"},
            status=200,
        )
        response = self.client.make_get_request("/ms", {"test": "test"})
        assert response.status_code == 200
        assert response.request.url == f"{TEST_API_ENDPOINT}/ms?test=test"

    @responses.activate
    def test_patch_request(self):
        responses.add(
            responses.PATCH,
            f"{TEST_API_ENDPOINT}/ms",
            json={"response": "ok"},
            status=200,
        )
        response = self.client.make_patch_request("/ms", {})
        assert response.status_code == 200

    @responses.activate
    def test_post_request(self):
        responses.add(
            responses.POST,
            f"{TEST_API_ENDPOINT}/ms",
            json={"response": "ok"},
            status=200,
        )
        response = self.client.make_post_request("/ms", {})
        assert response.status_code == 200

    @responses.activate
    def test_delete_request(self):
        responses.add(
            responses.DELETE,
            f"{TEST_API_ENDPOINT}/ms",
            json={"response": "ok"},
            status=200,
        )
        response = self.client.make_delete_request("/ms")
        assert response.status_code == 200
