import datetime
import json
import logging
import os
import sys

from requests import HTTPError

from ms_python_client import (
    CERNMSApiClient,
    PartialEventParameters,
    generate_error_log,
    setup_logs,
)

logger = setup_logs(log_level=logging.INFO)

cern_ms_client = CERNMSApiClient.init_from_dotenv()

for env_var in ["USER_ID", "ZOOM_ID"]:
    if not os.getenv(env_var):
        logger.error("%s not found in environment variables", env_var)
        sys.exit(1)

USER_ID = os.getenv("USER_ID", "")
ZOOM_ID = os.getenv("ZOOM_ID", "")

start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
end_time = start_time + datetime.timedelta(hours=1)

data = PartialEventParameters(
    start_time=start_time.isoformat(timespec="seconds"),
    end_time=end_time.isoformat(timespec="seconds"),
    # timezone= Set by default to Europe/Zurich
    # subject= Could be updated as well
)

try:
    result = cern_ms_client.events.update_event_by_zoom_id(USER_ID, ZOOM_ID, data)
    print(json.dumps(result, indent=4))

except HTTPError as e:
    print(json.dumps(generate_error_log(e), indent=4))
    sys.exit(1)
