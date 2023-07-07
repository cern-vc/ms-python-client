# Microsoft Python client

[![Python tests](https://github.com/cern-vc/MS-python-client/actions/workflows/python-tests.yml/badge.svg)](https://github.com/cern-vc/MS-python-client/actions/workflows/python-tests.yml)
[![pre-commit](https://github.com/cern-vc/MS-python-client/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/cern-vc/MS-python-client/actions/workflows/pre-commit.yaml)
[![CodeQL](https://github.com/cern-vc/MS-python-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cern-vc/MS-python-client/actions/workflows/codeql-analysis.yml)
[![codecov](https://codecov.io/gh/cern-vc/MS-python-client/branch/main/graph/badge.svg?token=04EY0K0P2S)](https://codecov.io/gh/cern-vc/MS-python-client)

Microsoft graph API Python client with support for [Server to Server Oauth tokens](https://learn.microsoft.com/en-us/graph/auth/auth-concepts?view=graph-rest-1.0) with App Only access.

## Install

This package is [available on Pypi](https://pypi.org/project/MS-python-client/)

```bash
pip install MS-python-client
```

## Requirements

- Python >= 3.10

## Usage

### Defining your env variables

Define the following variables in your `env` or your `.env` file:

- ms_ACCOUNT_ID
- ms_CLIENT_ID
- ms_CLIENT_SECRET

#### For testing purposes

For testing purposes, you can use the following values:

- ms_ACCESS_TOKEN

This token could be obtained from the [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) by clicking on the `Sign in with Microsoft` button and then clicking on the `Access Token` tab.

### Initialize the MSApiClient from environment variables

```python
from ms_python_client.ms_api_client import MSApiClient

ms_client = MSApiClient.init_from_env()
```

### Initialize the MSApiClient from .env

```python
from ms_python_client.ms_api_client import MSApiClient

ms_client = MSApiClient.init_from_dotenv()
```

### Initialize the MSApiClient manually

```python
from ms_python_client.ms_api_client import MSApiClient

ms_client = MSApiClient(
        account_id="<YOUR ACCOUNT ID>",
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>")
```

### Use the file system to store the access token instead of environment

There are some cases where you might want to store the access token in the file system in order to share its value with other elements of the application (Ex. different pods on a Kubernetes/Openshift application).

You can define the path where the token will be stored, passing the `use_path` variable to the constructor:

```python
from ms_python_client.ms_api_client import MSApiClient

ms_client = MSApiClient(
        account_id="<YOUR ACCOUNT ID>",
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>",
        use_path="/path/to/token/folder")
```

## How to make API calls

```python
USER_ID = "12345"
SUBJECT = "Test meeting"

query = {"$count": "true", "$filter": f"contains(subject,'{SUBJECT}')"}
result = cern_ms_client.events.list_events(USER_ID, query)
```

## Optional: How to configure the logging

```python
from ms_python_client.utils.logger import setup_logs

setup_logs(log_level=logging.DEBUG)
```

## Available endpoints

### **events**:

1. get all events
2. get a single event
3. create an event
4. update an event
5. delete an event

## CERN specific endpoints

Instead of using the `MSApiClient` class, you can use the `CERNMSApiClient` class, which is a subclass of the `MSApiClient` class.
This class will provide you some more utilities but it will only work for CERN users (obviously).

This will be used in the context of synchronizing the events between the CERN Indico system and the calendars of the Zoom Rooms.

### How to initialize the CERNMSApiClient

```python
from ms_python_client.cern_ms_api_client import CERNMSApiClient

cern_ms_client = CERNMSApiClient.init_from_env()
```

### Available endpoints

#### **events**:

1. get all events
2. get a single event using indico id
3. create an event
4. update an event using indico id
5. delete an event using indico id

You will find useful the `EventParameters` and `PartialEventParameters` classes, which will help you to create the events.

**indico_event_id** is the id of the event in the indico system which is mandatory to create an event.

**USER_ID** is the email of the Zoom Room.

```python
from ms_python_client.cern_ms_api_client import (
        CERNMSApiClient,
        EventParameters,
        PartialEventParameters,
        )

cern_ms_client = CERNMSApiClient.init_from_env()

USER_ID = os.getenv("USER_ID") # Which is the email of the Zoom Room
INDICO_EVENT_ID = os.getenv("INDICO_EVENT_ID")

event_parameters = EventParameters(
        subject="Test meeting",
        start_time="2021-10-01T12:00:00",
        end_time="2021-10-01T13:00:00",
        timezone="Europe/Zurich",
        indico_event_id=INDICO_EVENT_ID,
        zoom_url="https://cern.zoom.us/******",
)

partial_event_parameters = PartialEventParameters(
        indico_event_id=INDICO_EVENT_ID,
        end_time="2021-10-01T14:00:00",
) # You can update only the end_time of the event for example

cern_ms_client.events.create_event(USER_ID, event_parameters)
cern_ms_client.events.update_event_by_indico_id(USER_ID, partial_event_parameters)
cern_ms_client.events.delete_event_by_indico_id(USER_ID, INDICO_EVENT_ID)
```