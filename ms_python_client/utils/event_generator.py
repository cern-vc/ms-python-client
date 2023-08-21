import datetime
from typing import Any, TypedDict


class OptionalTimezone(TypedDict, total=False):
    """Optional timezone parameter for creating an event

    Args:
        timezone (str): The timezone of the event
    """

    timezone: str


class EventParameters(OptionalTimezone, TypedDict):
    """Parameters for creating an event

    Args:
        zoom_url (str): The Zoom URL for the event
        subject (str): The subject of the event
        start_time (str): The start time of the event in **ISO format**
        end_time (str): The end time of the event in **ISO format**
    """

    zoom_url: str
    subject: str
    start_time: str
    end_time: str


class PartialEventParameters(OptionalTimezone, TypedDict, total=False):
    """Parameters for updating an event

    Args:
        subject (str): The subject of the event
        start_time (str): The start time of the event in **ISO format**
        end_time (str): The end time of the event in **ISO format**
    """

    subject: str
    start_time: str
    end_time: str


# This has been set arbitrarily
ZOOM_ID_EXTENDED_PROPERTY_ID = (
    "String {d3123b00-8eb5-4f10-ae88-1269fe4cbaf0} Name ZoomId"
)


def create_event_body(event_parameters: EventParameters, zoom_id: str) -> dict:
    """Creates an event from the given parameters

    Args:
        event_parameters (EventParameters): The parameters of the event

    Returns:
        Event: The event
    """

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    zoom_id_from_url = event_parameters["zoom_url"].split("/")[-1].split("?")[0]
    if zoom_id_from_url != zoom_id:
        raise ValueError(
            "The zoom_id from the url does not match the zoom_id from the event parameters"
        )

    return {
        "subject": event_parameters["subject"],
        "start": {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["start_time"]
            ).isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["end_time"]
            ).isoformat(),
            "timeZone": timezone,
        },
        "location": {
            "displayName": event_parameters["zoom_url"],
            "locationType": "default",
            "uniqueIdType": "private",
            "uniqueId": event_parameters["zoom_url"],
        },
        "attendees": [],
        "allowNewTimeProposals": False,
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "unknown",
        "onlineMeetingUrl": event_parameters["zoom_url"],
        "singleValueExtendedProperties": [
            {
                "id": ZOOM_ID_EXTENDED_PROPERTY_ID,
                "value": zoom_id,
            }
        ],
    }


def create_partial_event_body(event_parameters: PartialEventParameters) -> dict:
    """Updates an event from the given parameters

    Args:
        event_parameters (PartialEventParameters): The parameters of the event

    Returns:
        Event: The event
    """
    event: dict[str, Any] = {}

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    if "subject" in event_parameters:
        event["subject"] = event_parameters["subject"]

    if "start_time" in event_parameters:
        event["start"] = {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["start_time"]
            ).isoformat(),
            "timeZone": timezone,
        }

    if "end_time" in event_parameters:
        event["end"] = {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["end_time"]
            ).isoformat(),
            "timeZone": timezone,
        }

    return event
