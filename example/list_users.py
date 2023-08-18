import json
import logging
import os
import sys

from requests import HTTPError

from ms_python_client import MSApiClient, generate_error_log, setup_logs

logger = setup_logs(log_level=logging.INFO)

cern_ms_client = MSApiClient.init_from_dotenv()

query = {"$count": "true"}

DISPLAY_NAME = os.getenv("DISPLAY_NAME", "Zoom Room")

if DISPLAY_NAME:
    query.update({"$search": f'"displayName:{DISPLAY_NAME}"'})


try:
    result = cern_ms_client.users.list_users(
        query, extra_headers={"ConsistencyLevel": "eventual"}
    )
    count = result.get("@odata.count", 0)
    print(f"Found {count} users:")

    for event in result.get("value", []):
        print(
            f"\t- {event['displayName']} - {event['id']} - {event['userPrincipalName']}"
        )

except HTTPError as e:
    print(json.dumps(generate_error_log(e), indent=4))
    sys.exit(1)
