import responses

from ms_python_client.components.events.users_component import UsersComponent
from ms_python_client.ms_api_client import MSApiClient
from tests.ms_python_client.base_test_case import TEST_API_ENDPOINT, BaseTest, mock_msal


class TestUsersComponent(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        ms_client = MSApiClient(
            "account_id", "client_id", "client_secret", api_endpoint=TEST_API_ENDPOINT
        )
        self.events_component = UsersComponent(ms_client)
        return super().setUp()

    @responses.activate
    def test_list_users(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users",
            json={"response": "ok"},
            status=200,
        )
        users_list = self.events_component.list_users()
        assert users_list["response"] == "ok"
