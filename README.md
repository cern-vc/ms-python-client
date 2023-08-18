# Microsoft Python client

[![Python tests](https://github.com/cern-vc/ms-python-client/actions/workflows/python-tests.yml/badge.svg)](https://github.com/cern-vc/ms-python-client/actions/workflows/python-tests.yml)
[![Pre-commit](https://github.com/cern-vc/ms-python-client/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/cern-vc/ms-python-client/actions/workflows/pre-commit.yaml)
[![CodeQL](https://github.com/cern-vc/ms-python-client/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/cern-vc/ms-python-client/actions/workflows/github-code-scanning/codeql)
[![codecov](https://codecov.io/gh/cern-vc/MS-python-client/branch/main/graph/badge.svg?token=04EY0K0P2S)](https://codecov.io/gh/cern-vc/MS-python-client)

![Build](https://img.shields.io/github/actions/workflow/status/cern-vc/ms-python-client/build.yml?logo=python&label=Publish&color=0E7FC0)
![PyPI - Version](https://img.shields.io/pypi/v/ms-python-client?logo=python)
![PyPI - Download](https://img.shields.io/pypi/dm/ms-python-client?logo=python&color=0E7FC0)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ms-python-client?logo=python&color=0E7FC0)

Microsoft graph API Python client with support for [Device Flow Oauth tokens](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code) with deleguated access.

## Install

This package is [available on Pypi](https://pypi.org/project/ms-python-client/)

```bash
pip install ms-python-client
```

## Requirements

- Python >= 3.9

## How to configure the client variables to make API calls

### Defining your env variables

Define the following variables in your `env` or your `.env` file:

- AZURE_AUTHORITY
- AZURE_CLIENT_ID
- AZURE_SCOPE

#### For testing purposes

For testing purposes, you can use the following value:

- MS_ACCESS_TOKEN

This token could be obtained from the [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) by clicking on the `Sign in with Microsoft` button and then clicking on the `Access Token` tab.

## Usage

### Initialize the MSApiClient from environment variables

```python
from ms_python_client import MSApiClient

ms_client = MSApiClient.init_from_env()
```

### Initialize the MSApiClient from .env

```python
from ms_python_client import MSApiClient

ms_client = MSApiClient.init_from_dotenv()
```

### Initialize the MSApiClient manually

```python
from ms_python_client import MSApiClient,  Config

config = Config(
    azure_authority="<YOUR AZURE AUTHORITY>",
    azure_client_id="<YOUR AZURE CLIENT ID>",
    azure_scope="<YOUR AZURE SCOPE>" # Ex. [User.Read, Calendars.ReadWrite, etc.]
)

ms_client = MSApiClient(
    config=config,
)
```

#### Store of the cache token

By default the token is stored in a file called `token_cache.bin` in the current directory. You can change this behavior by passing the `token_cache_file` parameter to the `Config` constructor.

```python
from ms_python_client import MSApiClient, Config

config = Config(
    azure_authority="<YOUR AZURE AUTHORITY>",
    azure_client_id="<YOUR AZURE CLIENT ID>",
    azure_scope="<YOUR AZURE SCOPE>", # Ex. [User.Read, Calendars.ReadWrite, etc.]
    token_cache_file="/path/to/token_cache.bin"
)

ms_client = MSApiClient(
    config=config,
)
```

This will allow you to reuse the token in the next executions of your script and even in different scripts.

## How to make API calls

```python
USER_ID = "12345"
SUBJECT = "Test meeting"

query = {"$count": "true", "$filter": f"contains(subject,'{SUBJECT}')"}
result = cern_ms_client.events.list_events(USER_ID, query)
```

## Optional: How to configure the logging

```python
from ms_python_client import setup_logs

setup_logs(log_level=logging.DEBUG)
```

## Available endpoints

### **events**:

1. get all events
2. get a single event
3. create an event
4. update an event
5. delete an event

### **users**:

1. get all users

---

## CERN specific usage

Instead of using the `MSApiClient` class, you can use the `CERNMSApiClient` class, which is a subclass of the `MSApiClient` class.
This class will provide you some more utilities but it will only work for CERN users (obviously).

This will be used in the context of synchronizing the events between the CERN Indico system and the calendars of the Zoom Rooms.

### How to initialize the CERNMSApiClient

Follow the [How to configure the client variables to make API calls](#how-to-configure-the-client-variables-to-make-api-calls) section and then:

```python
from ms_python_client import CERNMSApiClient

cern_ms_client = CERNMSApiClient.init_from_dotenv()
```

### Available endpoints

#### **events**:

1. get all events
2. get a single event using zoom id
3. create an event
4. update an event using zoom id
5. delete an event using zoom id
6. get the zoom id of an event

You will find useful the `EventParameters` and `PartialEventParameters` classes, which will help you to create the events.

The `EventParameters` class is used to create an event, while the `PartialEventParameters` class is used to update an event.

- `ZOOM_ID` is the id of the zoom meeting, which can be found inside the url of a meeting link. This is **mandatory** to create an event.
- `USER_ID` is the email of the Zoom Room.

```python
from ms_python_client import CERNMSApiClient, EventParameters, PartialEventParameters

cern_ms_client = CERNMSApiClient.init_from_dotenv()

USER_ID = os.getenv("USER_ID") # Which is the email of the Zoom Room
ZOOM_ID = os.getenv("ZOOM_ID")

event_parameters = EventParameters(
        subject="Test meeting",
        start_time="2021-10-01T12:00:00",
        end_time="2021-10-01T13:00:00",
        timezone="Europe/Zurich",
        zoom_url="https://cern.zoom.us/******",
)

partial_event_parameters = PartialEventParameters(
        end_time="2021-10-01T14:00:00",
) # You can update only the end_time of the event for example

cern_ms_client.events.create_event(USER_ID, ZOOM_ID, event_parameters)
cern_ms_client.events.update_event_by_zoom_id(USER_ID, ZOOM_ID, partial_event_parameters)
cern_ms_client.events.delete_event_by_zoom_id(USER_ID, ZOOM_ID)
```
