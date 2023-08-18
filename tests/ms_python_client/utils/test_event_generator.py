import pytest

from ms_python_client.utils.event_generator import (
    EventParameters,
    PartialEventParameters,
    create_event_body,
    create_partial_event_body,
)


def test_create_event_body():
    parameters = EventParameters(
        zoom_url="https://zoom.us/j/1234567890",
        subject="Test Event",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
    )

    result = create_event_body(parameters, "1234567890")

    assert result == {
        "subject": "Test Event",
        "start": {"dateTime": "2021-01-01T00:00:00", "timeZone": "Europe/Zurich"},
        "end": {"dateTime": "2021-01-01T01:00:00", "timeZone": "Europe/Zurich"},
        "location": {
            "displayName": "https://zoom.us/j/1234567890",
            "locationType": "default",
            "uniqueIdType": "private",
            "uniqueId": "https://zoom.us/j/1234567890",
        },
        "attendees": [],
        "allowNewTimeProposals": False,
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "unknown",
        "onlineMeetingUrl": "https://zoom.us/j/1234567890",
        "singleValueExtendedProperties": [
            {
                "id": "String {d3123b00-8eb5-4f10-ae88-1269fe4cbaf0} Name ZoomId",
                "value": "1234567890",
            }
        ],
    }


def test_create_event_body_with_error():
    parameters = EventParameters(
        zoom_url="https://zoom.us/j/1234567890",
        subject="Test Event",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
    )

    with pytest.raises(ValueError):
        create_event_body(parameters, "1234")


def test_create_partial_event_body_1():
    parameters = PartialEventParameters(
        subject="Test Event",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "subject": "Test Event",
    }


def test_create_partial_event_body_2():
    parameters = PartialEventParameters(
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
        timezone="Europe/Zurich",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "start": {"dateTime": "2021-01-01T00:00:00", "timeZone": "Europe/Zurich"},
        "end": {"dateTime": "2021-01-01T01:00:00", "timeZone": "Europe/Zurich"},
    }
