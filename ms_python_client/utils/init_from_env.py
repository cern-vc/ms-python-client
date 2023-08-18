import logging
import os

from dotenv import load_dotenv

from ms_python_client.config import Config
from ms_python_client.utils.file_system import get_project_dir

logger = logging.getLogger("ms_python_client")


class MSClientEnvError(Exception):
    pass


def init_from_env() -> Config:
    try:
        azure_authority = os.environ["AZURE_AUTHORITY"]
        azure_client_id = os.environ["AZURE_CLIENT_ID"]
        azure_scope_str = os.environ["AZURE_SCOPE"]

        token_cache_file = os.environ.get("TOKEN_CACHE_FILE", "token_cache.bin")
        azure_scope = azure_scope_str.split(",")

        return Config(
            token_cache_file=token_cache_file,
            azure_authority=azure_authority,
            azure_client_id=azure_client_id,
            azure_scope=azure_scope,
        )

    except KeyError as error:
        raise MSClientEnvError(f"Required key not in environment: {error}") from error


def init_from_dotenv(custom_dotenv=".env"):
    env_dir = os.path.dirname(os.path.realpath(custom_dotenv))
    env_name = os.path.basename(os.path.realpath(custom_dotenv))
    project_dir = get_project_dir() if env_dir == "" else env_dir
    logger.info("Loading env file at %s/%s", project_dir, env_name)
    load_dotenv(os.path.join(project_dir, env_name), verbose=True)
