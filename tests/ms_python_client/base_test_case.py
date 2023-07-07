import logging
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ms_python_client.utils.logger import setup_logs

MOCK_TOKEN = "mock_token"
TEST_API_ENDPOINT = "http://localhost"

setup_logs(log_level=logging.DEBUG)


def mock_confidential_client_application(mock_instance, cache_disabled: bool):
    # Configure the return value of the methods you want to mock
    mock_instance.acquire_token_silent.return_value = (
        {"access_token": MOCK_TOKEN} if not cache_disabled else None
    )
    mock_instance.acquire_token_for_client.return_value = {"access_token": MOCK_TOKEN}


def mock_msal(cache_enabled=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with patch(
                "ms_python_client.ms_api_client.ConfidentialClientApplication"
            ) as mock_cca:
                mock_instance = mock_cca.return_value
                mock_confidential_client_application(mock_instance, not cache_enabled)
                return func(*args, **kwargs)

        return wrapper

    return decorator


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        shutil.copy(".env.sample", self.test_dir)
        self.env_file = os.path.join(self.test_dir, ".env.sample")

        os.environ.pop("MS_ACCOUNT_ID", None)
        os.environ.pop("MS_CLIENT_ID", None)
        os.environ.pop("MS_CLIENT_SECRET", None)
        os.environ.pop("MS_ACCESS_TOKEN", None)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)
