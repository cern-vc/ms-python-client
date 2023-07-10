from typing import Mapping, Optional

from ms_python_client.ms_client_interface import MSClientInterface


class UsersComponent:
    def __init__(self, client: MSClientInterface) -> None:
        self.client = client

    def list_users(self, parameters: Optional[Mapping[str, str]] = None) -> dict:
        """List all users

        Args:
            parameters (Optional[Mapping[str, str]], optional): Parameters for the request. Defaults to None.

        Returns:
            dict: The response of the request
        """
        api_path = "/users"
        response = self.client.make_get_request(api_path, parameters)
        return response.json()
