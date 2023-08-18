import logging
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ms_python_client.utils.init_from_env import init_from_dotenv, init_from_env
from ms_python_client.utils.logger import setup_logs

MOCK_TOKEN = "mock_token"
TEST_API_ENDPOINT = "http://localhost"

setup_logs(log_level=logging.DEBUG)


def mock_oauth2_flow(mock_instance):
    # Configure the return value of the methods you want to mock
    # Make the __init__ method return the mock instance
    mock_instance.get_access_token.return_value = (MOCK_TOKEN, "username")
    mock_instance.__class__.get_access_token = mock_instance.get_access_token
    mock_instance.__class__.__init__ = lambda self: None


def mock_msal():
    def decorator(func):
        def wrapper(*args, **kwargs):
            with patch("ms_python_client.ms_api_client.Oauth2Flow") as mock_oauth:
                mock_instance = mock_oauth.return_value
                mock_oauth2_flow(mock_instance)
                return func(*args, **kwargs)

        return wrapper

    return decorator


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        shutil.copy(".env.sample", self.test_dir)
        self.env_file = os.path.join(self.test_dir, ".env.sample")
        init_from_dotenv(custom_dotenv=self.env_file)
        self.config = init_from_env()

        os.environ.pop("AZURE_AUTHORITY", None)
        os.environ.pop("AZURE_CLIENT_ID", None)
        os.environ.pop("AZURE_SCOPE", None)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)
