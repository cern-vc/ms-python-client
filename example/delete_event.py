import json
import logging
import os
import sys

from requests import HTTPError

from ms_python_client.cern_ms_api_client import CERNMSApiClient
from ms_python_client.utils.error import generate_error_log
from ms_python_client.utils.logger import setup_logs

logger = setup_logs(log_level=logging.INFO)

cern_ms_client = CERNMSApiClient.init_from_dotenv()

for env_var in ["USER_ID", "ZOOM_ID"]:
    if not os.getenv(env_var):
        logger.error("%s not found in environment variables", env_var)
        sys.exit(1)

USER_ID = os.getenv("USER_ID", "")
ZOOM_ID = os.getenv("ZOOM_ID", "")

try:
    cern_ms_client.events.delete_event_by_zoom_id(USER_ID, ZOOM_ID)
    print(f"Event {ZOOM_ID} deleted")

except HTTPError as e:
    print(json.dumps(generate_error_log(e), indent=4))
    sys.exit(1)
