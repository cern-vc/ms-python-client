import os
import unittest
from unittest.mock import MagicMock, patch

from ms_python_client.config import Config
from ms_python_client.utils.init_from_env import (
    MSClientEnvError,
    init_from_dotenv,
    init_from_env,
)


class TestInitFromEnv(unittest.TestCase):
    def setUp(self):
        os.environ["AZURE_AUTHORITY"] = "https://login.microsoftonline.com/common"
        os.environ["AZURE_CLIENT_ID"] = "client_id"
        os.environ["AZURE_SCOPE"] = "Scope1,Scope2"

    def tearDown(self):
        os.environ.pop("AZURE_AUTHORITY", None)
        os.environ.pop("AZURE_CLIENT_ID", None)
        os.environ.pop("AZURE_SCOPE", None)

    def test_init_from_env(self):
        config = init_from_env()
        self.assertIsInstance(config, Config)
        self.assertEqual(config.TOKEN_CACHE_FILE, "token_cache.bin")
        self.assertEqual(
            config.AZURE_AUTHORITY, "https://login.microsoftonline.com/common"
        )
        self.assertEqual(config.AZURE_CLIENT_ID, "client_id")
        self.assertEqual(config.AZURE_SCOPE, ["Scope1", "Scope2"])

    def test_init_from_env_missing_key(self):
        os.environ.pop("AZURE_AUTHORITY", None)
        with self.assertRaises(MSClientEnvError):
            init_from_env()


class TestInitFromDotenv(unittest.TestCase):
    @patch("ms_python_client.utils.init_from_env.load_dotenv")
    def test_init_from_dotenv(self, mock_load_dotenv: MagicMock):
        init_from_dotenv("/path/to/project/.env")
        mock_load_dotenv.assert_called_once_with("/path/to/project/.env", verbose=True)
