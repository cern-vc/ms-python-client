import json
import logging
import os
import sys

from requests import HTTPError

from ms_python_client import CERNMSApiClient, generate_error_log, setup_logs

logger = setup_logs(log_level=logging.INFO)

cern_ms_client = CERNMSApiClient.init_from_dotenv()

USER_ID = os.getenv("USER_ID")

if not USER_ID:
    logger.error("USER_ID not found in environment variables")
    sys.exit(1)


try:
    query = {"$count": "true"}
    result = cern_ms_client.events.list_events(USER_ID, query)

    count = result.get("@odata.count", 0)
    print(f"Found {count} events:")

    for event in result.get("value", []):
        print(f"\t- {event['subject']} - {event['id']}")

except HTTPError as e:
    print(json.dumps(generate_error_log(e), indent=4))
    sys.exit(1)
