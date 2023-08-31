import json
import logging
import os
import sys

from requests import HTTPError

from ms_python_client import (
    CERNMSApiClient,
    NotFoundError,
    generate_error_log,
    setup_logs,
)

logger = setup_logs(log_level=logging.INFO)

cern_ms_client = CERNMSApiClient.init_from_dotenv()

for env_var in ["USER_ID", "EVENT_ID"]:
    if not os.getenv(env_var):
        logger.error("%s not found in environment variables", env_var)
        sys.exit(1)

USER_ID = os.getenv("USER_ID", "")
EVENT_ID = os.getenv("EVENT_ID", "")

try:
    result = cern_ms_client.events.get_event_zoom_id(USER_ID, EVENT_ID)
    print(f"Zoom ID: {result}")

except HTTPError as e:
    print(json.dumps(generate_error_log(e), indent=4))
    sys.exit(1)

except NotFoundError as e:
    logger.error(e)
    sys.exit(1)
