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
        zoom_id="1234567890",
        subject="Test Event",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
    )

    result = create_event_body(parameters)

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
        zoom_id="1234",
        subject="Test Event",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
    )

    with pytest.raises(ValueError):
        create_event_body(parameters)


def test_create_partial_event_body_0():
    parameters = PartialEventParameters(
        zoom_id="1234567890",
    )

    result = create_partial_event_body(parameters)

    assert not result


def test_create_partial_event_body_1():
    parameters = PartialEventParameters(
        zoom_id="1234567890",
        zoom_url="https://zoom.us/j/1234567890",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "location": {
            "displayName": "https://zoom.us/j/1234567890",
            "locationType": "default",
            "uniqueIdType": "private",
            "uniqueId": "https://zoom.us/j/1234567890",
        },
        "onlineMeetingUrl": "https://zoom.us/j/1234567890",
    }


def test_create_partial_event_body_2():
    parameters = PartialEventParameters(
        zoom_id="1234567890",
        subject="Test Event",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "subject": "Test Event",
    }


def test_create_partial_event_body_3():
    parameters = PartialEventParameters(
        zoom_id="1234567890",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
        timezone="Europe/Zurich",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "start": {"dateTime": "2021-01-01T00:00:00", "timeZone": "Europe/Zurich"},
        "end": {"dateTime": "2021-01-01T01:00:00", "timeZone": "Europe/Zurich"},
    }


def test_create_partial_event_body_4():
    parameters = PartialEventParameters(
        zoom_id="1234",
        zoom_url="https://zoom.us/j/1234567890",
    )
    with pytest.raises(ValueError):
        create_partial_event_body(parameters)
