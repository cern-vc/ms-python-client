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
        os.environ["MS_ACCOUNT_ID"] = "aaa"
        os.environ["MS_CLIENT_ID"] = "bbb"
        os.environ["MS_CLIENT_SECRET"] = "ccc"

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
    def test_init_with_use_path(self):
        client = MSApiClient.init_from_dotenv(
            custom_dotenv=self.env_file, use_path=self.test_dir
        )
        assert client is not None

    @mock_msal()
    def test_build_headers(self):
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers()
        assert headers is not None
        assert headers["Authorization"] == f"Bearer {MOCK_TOKEN}"
        assert headers["Content-type"] == "application/json"

    @mock_msal(cache_enabled=False)
    def test_build_header_without_cache(self):
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers()
        assert headers is not None
        assert headers["Authorization"] == f"Bearer {MOCK_TOKEN}"
        assert headers["Content-type"] == "application/json"

    def test_with_token(self):
        os.environ["MS_ACCESS_TOKEN"] = "test_token"
        client = MSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        headers = client.build_headers()
        assert headers is not None
        assert headers["Authorization"] == "Bearer test_token"
        assert headers["Content-type"] == "application/json"

        os.environ.pop("MS_ACCESS_TOKEN", None)


class TestMSApiClient(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        self.client = MSApiClient("AAA", "BBB", "CCC", api_endpoint=TEST_API_ENDPOINT)
        return super().setUp()

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


class TestMSApiClientFromPath(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        super().setUp()
        self.client = MSApiClient(
            "AAA", "BBB", "CCC", api_endpoint=TEST_API_ENDPOINT, use_path=self.test_dir
        )

    @responses.activate
    def test_get_request(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/ms",
            json={"response": "ok"},
            status=200,
        )
        response = self.client.make_get_request("/ms", {})
        assert response.status_code == 200

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
