from typing import Any, Mapping, Optional

from ms_python_client.ms_client_interface import MSClientInterface


class EventsComponent:
    def __init__(self, client: MSClientInterface) -> None:
        self.client = client

    def list_events(
        self,
        user_id: str,
        parameters: Optional[Mapping[str, str]] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """List all the events of a user

        Args:
            user_id (str): The user id

        Returns:
            dict: The response of the request
        """
        api_path = f"/users/{user_id}/calendar/events"
        response = self.client.make_get_request(
            api_path, parameters, extra_headers=extra_headers
        )
        return response.json()

    def get_event(
        self,
        user_id: str,
        event_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Get an event of a user

        Args:
            user_id (str): The user id
            event_id (str): The event id

        Returns:
            dict: The response of the request
        """
        api_path = f"/users/{user_id}/calendar/events/{event_id}"
        response = self.client.make_get_request(api_path, extra_headers=extra_headers)
        return response.json()

    def create_event(
        self,
        user_id: str,
        json: Mapping[str, Any],
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Create an event for a user

        Args:
            user_id (str): The user id
            data (Mapping[str, Any]): The event data

        Returns:
            dict: The response of the request
        """
        api_path = f"/users/{user_id}/calendar/events"
        response = self.client.make_post_request(
            api_path, json, extra_headers=extra_headers
        )
        return response.json()

    def update_event(
        self,
        user_id: str,
        event_id: str,
        json: Mapping[str, Any],
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Update an event for a user

        Args:
            user_id (str): The user id
            event_id (str): The event id
            data (Mapping[str, Any]): The event parameters

        Returns:
            dict: The response of the request
        """
        api_path = f"/users/{user_id}/calendar/events/{event_id}"
        response = self.client.make_patch_request(
            api_path, json, extra_headers=extra_headers
        )
        return response.json()

    def delete_event(
        self,
        user_id: str,
        event_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Delete an event of a user

        Args:
            user_id (str): The user id
            event_id (str): The event id

        Returns:
            dict: The response of the request
        """
        api_path = f"/users/{user_id}/calendar/events/{event_id}"
        self.client.make_delete_request(api_path, extra_headers=extra_headers)
