import unittest

from ms_python_client.config import Config


class TestConfig(unittest.TestCase):
    def test_custom_values(self):
        config = Config(
            token_cache_file="custom_token_cache.bin",
            azure_authority="https://login.microsoftonline.com/common",
            azure_client_id="12345678-1234-5678-abcd-1234567890ab",
            azure_scope=["User.Read"],
        )
        self.assertEqual(config.TOKEN_CACHE_FILE, "custom_token_cache.bin")
        self.assertEqual(
            config.AZURE_AUTHORITY, "https://login.microsoftonline.com/common"
        )
        self.assertEqual(config.AZURE_CLIENT_ID, "12345678-1234-5678-abcd-1234567890ab")
        self.assertEqual(config.AZURE_SCOPE, ["User.Read"])

    def test_missing_authority(self):
        with self.assertRaises(ValueError):
            Config(azure_client_id="12345678-1234-5678-abcd-1234567890ab")

    def test_missing_client_id(self):
        with self.assertRaises(ValueError):
            Config(azure_authority="https://login.microsoftonline.com/common")

    def test_missing_scope(self):
        with self.assertRaises(ValueError):
            Config(
                azure_authority="https://login.microsoftonline.com/common",
                azure_client_id="12345678-1234-5678-abcd-1234567890ab",
            )
