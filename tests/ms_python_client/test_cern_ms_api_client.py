import os

from ms_python_client.cern_ms_api_client import CERNMSApiClient
from tests.ms_python_client.base_test_case import BaseTest, mock_msal


class TestCERNMSApiClientInit(BaseTest):
    @mock_msal()
    def test_init_from_env(self):
        os.environ[
            "AZURE_AUTHORITY"
        ] = "https://login.microsoftonline.com/organizations"
        os.environ["AZURE_CLIENT_ID"] = "test"
        os.environ["AZURE_SCOPE"] = "Scope1,Scope2"

        client = CERNMSApiClient.init_from_env()

        assert client is not None

    @mock_msal()
    def test_init_from_dotenv(self):
        client = CERNMSApiClient.init_from_dotenv(custom_dotenv=self.env_file)
        assert client is not None
