"""Process Oauth2 authentication flow."""

import atexit
import json
import logging
import os
import sys

import msal

from ms_python_client.config import Config

logger = logging.getLogger("ms_python_client")


class Oauth2Flow:
    """Process Oauth2 authentication flow."""

    def __init__(self, conf: Config) -> None:
        """Initialize the Oauth2 Flow."""
        self.conf = conf
        self.cache = msal.SerializableTokenCache()

        if os.path.exists(self.conf.TOKEN_CACHE_FILE):
            with open(self.conf.TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
                self.cache.deserialize(f.read())
                logger.debug("Token cache loaded")

        atexit.register(
            lambda: self._save_cache() if self.cache.has_state_changed else None
        )

        self.app = msal.PublicClientApplication(
            self.conf.AZURE_CLIENT_ID,
            authority=self.conf.AZURE_AUTHORITY,
            token_cache=self.cache,
        )

    def _save_cache(self):
        with open(self.conf.TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(self.cache.serialize())
            logger.debug("Token cache saved")

    def get_access_token(self) -> "tuple[str, str]":
        """Get access token.

        Raises:
            ValueError: Error on doing the Device Flow
            ValueError: Error on getting the access token

        Returns:
            tuple[str, str]: Access token and username
        """
        result = None
        # Try to reload token from the cache
        accounts = self.app.get_accounts()

        if accounts:
            result = self.app.acquire_token_silent(
                scopes=self.conf.AZURE_SCOPE,
                account=accounts[0],
                authority=None,
                force_refresh=False,
                claims_challenge=None,
            )

        if not result:
            logger.info(
                "No suitable token exists in cache. Let's get a new one from AAD."
            )

            flow = self.app.initiate_device_flow(scopes=self.conf.AZURE_SCOPE)

            if "user_code" not in flow:
                raise ValueError(
                    f"Fail to create device flow. Err: {json.dumps(flow, indent=4)}"
                )

            logger.info(flow["message"])
            sys.stdout.flush()  # Some terminal needs this to ensure the message is shown

            # Ideally you should wait here, in order to save some unnecessary polling
            # input("Press Enter after signing in from another device to proceed, CTRL+C to abort.")

            result = self.app.acquire_token_by_device_flow(
                flow
            )  # By default it will block
            # You can follow this instruction to shorten the block time
            # https://msal-python.readthedocs.io/en/latest/#msal.PublicClientApplication.acquire_token_by_device_flow
            # or you may even turn off the blocking behavior,
            # and then keep calling acquire_token_by_device_flow(flow) in your own customized loop.

        if "access_token" in result:
            # return the access token AND the username
            if not accounts:
                accounts = self.app.get_accounts()
            logger.info(f"Token aquired for: {accounts[0]['username']}")

            if "scope" in result:
                logger.debug(f"Scopes: {result['scope']}")

            return result["access_token"], accounts[0]["username"]

        raise ValueError(
            "Error getting access_token",
            result.get("error"),
            result.get("error_description"),
            result.get("correlation_id"),
        )
