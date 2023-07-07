from ms_python_client.utils.event_generator import (
    EventParameters,
    PartialEventParameters,
    create_event_body,
    create_partial_event_body,
)


def test_create_event_body():
    parameters = EventParameters(
        zoom_url="https://zoom.us/j/1234567890",
        indico_event_id="1234567890",
        subject="Test Event",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
    )

    result = create_event_body(parameters)

    assert result == {
        "subject": "[1234567890] Test Event",
        "body": {
            "contentType": "text",
            "content": "Zoom URL: https://zoom.us/j/1234567890",
        },
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
    }


def test_create_partial_event_body_0():
    parameters = PartialEventParameters(
        indico_event_id="1234567890",
    )

    result = create_partial_event_body(parameters)

    assert not result


def test_create_partial_event_body_1():
    parameters = PartialEventParameters(
        indico_event_id="1234567890",
        zoom_url="https://zoom.us/j/1234567890",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "body": {
            "contentType": "text",
            "content": "Zoom URL: https://zoom.us/j/1234567890",
        },
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
        indico_event_id="1234567890",
        subject="Test Event",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "subject": "[1234567890] Test Event",
    }


def test_create_partial_event_body_3():
    parameters = PartialEventParameters(
        indico_event_id="1234567890",
        start_time="2021-01-01T00:00:00",
        end_time="2021-01-01T01:00:00",
        timezone="Europe/Zurich",
    )

    result = create_partial_event_body(parameters)

    assert result == {
        "start": {"dateTime": "2021-01-01T00:00:00", "timeZone": "Europe/Zurich"},
        "end": {"dateTime": "2021-01-01T01:00:00", "timeZone": "Europe/Zurich"},
    }
