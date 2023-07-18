import responses

from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.ms_api_client import MSApiClient
from tests.ms_python_client.base_test_case import TEST_API_ENDPOINT, BaseTest, mock_msal


class TestEventsComponent(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        ms_client = MSApiClient(
            "account_id", "client_id", "client_secret", api_endpoint=TEST_API_ENDPOINT
        )
        self.events_component = EventsComponent(ms_client)
        return super().setUp()

    @responses.activate
    def test_list_events(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        parameters = {
            "key": "value",
        }
        headers = {
            "test": "test",
        }
        events_list = self.events_component.list_events("user_id", parameters, headers)
        assert events_list["response"] == "ok"
        assert (
            responses.calls[0].request.url
            == f"{TEST_API_ENDPOINT}/users/user_id/calendar/events?key=value"
        )
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_get_event(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            json={"response": "ok"},
            status=200,
        )
        headers = {
            "test": "test",
        }
        event = self.events_component.get_event(
            "user_id", "event_id", extra_headers=headers
        )
        assert event["response"] == "ok"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_create_event(self):
        responses.add(
            responses.POST,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        data = {
            "key": "value",
        }
        headers = {
            "test": "test",
        }
        event = self.events_component.create_event("user_id", data, headers)
        assert event["response"] == "ok"
        assert responses.calls[0].request.body == b'{"key": "value"}'
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_update_event(self):
        responses.add(
            responses.PATCH,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            json={"response": "ok"},
            status=200,
        )
        data = {
            "key": "value",
        }
        headers = {
            "test": "test",
        }
        event = self.events_component.update_event("user_id", "event_id", data, headers)
        assert event["response"] == "ok"
        assert responses.calls[0].request.body == b'{"key": "value"}'
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_delete_event(self):
        responses.add(
            responses.DELETE,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            status=204,
        )
        headers = {
            "test": "test",
        }
        self.events_component.delete_event("user_id", "event_id", headers)
        assert responses.calls[0].request.headers["test"] == "test"
