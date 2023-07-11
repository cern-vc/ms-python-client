import datetime
from typing import TypedDict


class BaseEventParameters(TypedDict):
    """Base parameters for creating an event

    Args:
        zoom_id (str): The zoom event id
    """

    zoom_id: str


class OptionalTimezone(TypedDict, total=False):
    """Optional timezone parameter for creating an event

    Args:
        timezone (str): The timezone of the event
    """

    timezone: str


class EventParameters(BaseEventParameters, OptionalTimezone):
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


class PartialEventParameters(BaseEventParameters, OptionalTimezone, total=False):
    """Parameters for updating an event

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


ZOOM_ID_EXTENDED_PROPERTY_ID = (
    "String {d3123b00-8eb5-4f10-ae88-1269fe4cbaf0} Name ZoomId"
)


def create_event_body(event_parameters: EventParameters) -> dict:
    """Creates an event from the given parameters

    Args:
        event_parameters (EventParameters): The parameters of the event

    Returns:
        Event: The event
    """

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    zoom_id_from_url = event_parameters["zoom_url"].split("/")[-1].split("?")[0]
    if zoom_id_from_url != event_parameters["zoom_id"]:
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
                "value": event_parameters["zoom_id"],
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
    event = {}

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    if "zoom_url" in event_parameters:
        zoom_id_from_url = event_parameters["zoom_url"].split("/")[-1].split("?")[0]
        if zoom_id_from_url != event_parameters["zoom_id"]:
            raise ValueError(
                "The zoom_id from the url does not match the zoom_id from the event parameters"
            )
        event.update(
            {
                "location": {
                    "displayName": event_parameters["zoom_url"],
                    "locationType": "default",
                    "uniqueIdType": "private",
                    "uniqueId": event_parameters["zoom_url"],
                },
                "onlineMeetingUrl": event_parameters["zoom_url"],
            }
        )

    if "subject" in event_parameters:
        event.update(
            {
                "subject": event_parameters["subject"],
            }
        )

    if "start_time" in event_parameters:
        event.update(
            {
                "start": {
                    "dateTime": datetime.datetime.fromisoformat(
                        event_parameters["start_time"]
                    ).isoformat(),
                    "timeZone": timezone,
                }
            }
        )

    if "end_time" in event_parameters:
        event.update(
            {
                "end": {
                    "dateTime": datetime.datetime.fromisoformat(
                        event_parameters["end_time"]
                    ).isoformat(),
                    "timeZone": timezone,
                }
            }
        )

    return event
