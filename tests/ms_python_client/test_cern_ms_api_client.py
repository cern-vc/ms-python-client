import os

from ms_python_client.cern_ms_api_client import CERNMSApiClient
from tests.ms_python_client.base_test_case import BaseTest, mock_msal


class TestCERNMSApiClientInit(BaseTest):
    @mock_msal()
    def test_init_from_env(self):
        os.environ["MS_ACCOUNT_ID"] = "aaa"
        os.environ["MS_CLIENT_ID"] = "bbb"
        os.environ["MS_CLIENT_SECRET"] = "ccc"

        client = CERNMSApiClient.init_from_env()

        assert client is not None

    @mock_msal()
    def test_init_from_dotenv(self):
        client = CERNMSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        assert client is not None
