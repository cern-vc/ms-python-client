import logging
import os
from typing import Any, Optional, TypedDict

from dotenv import load_dotenv

from ms_python_client.utils.file_system import get_project_dir

logger = logging.getLogger("ms_python_client")


class MSClientEnvError(Exception):
    pass


class ReturnType(TypedDict):
    account_id: str
    client_id: str
    client_secret: Any
    use_path: Optional[str]


def init_from_env(use_path: Optional[str] = None) -> ReturnType:
    try:
        account_id = os.environ["MS_ACCOUNT_ID"]
        client_id = os.environ["MS_CLIENT_ID"]
        client_secret = os.environ["MS_CLIENT_SECRET"]
        return ReturnType(
            account_id=account_id,
            client_id=client_id,
            client_secret=client_secret,
            use_path=use_path,
        )
    except KeyError as error:
        raise MSClientEnvError(f"Required key not in environment: {error}") from error


def init_from_dotenv(custom_dotenv=".env"):
    env_dir = os.path.dirname(os.path.realpath(custom_dotenv))
    env_name = os.path.basename(os.path.realpath(custom_dotenv))
    project_dir = get_project_dir() if env_dir == "" else env_dir
    logger.info("Loading env file at %s/%s", project_dir, env_name)
    load_dotenv(os.path.join(project_dir, env_name), verbose=True)
