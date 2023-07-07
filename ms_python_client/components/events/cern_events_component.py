import logging
from typing import Mapping, Optional

from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.ms_client_interface import MSClientInterface
from ms_python_client.utils.event_generator import (
    EventParameters,
    PartialEventParameters,
    create_event_body,
    create_partial_event_body,
)

logger = logging.getLogger("ms_python_client")


class NotFoundError(Exception):
    """Execption raised when an event is not found

    Args:
        Exception (Exception): The base exception
    """


class CERNEventsComponents:
    """CERN Events component"""

    def __init__(self, client: MSClientInterface) -> None:
        self.events_component = EventsComponent(client)

    def list_events(
        self, user_id: str, parameters: Optional[Mapping[str, str]] = None
    ) -> dict:
        """List all the events of a user

        Args:
            user_id (str): The user id
            parameters (dict): Optional parameters for the request

        Returns:
            dict: The response of the request
        """
        return self.events_component.list_events(user_id, parameters)

    def get_event_by_indico_id(self, user_id: str, indico_id: str) -> dict:
        """Get an event of a user

        Args:
            indico_id (str): The event id

        Returns:
            dict: The response of the request
        """
        parameters = {"$count": "true", "$filter": f"contains(subject,'{indico_id}')"}
        response = self.events_component.list_events(user_id, parameters)

        count = response.get("@odata.count", 0)
        if count == 0:
            raise NotFoundError(f"Event with indico id {indico_id} not found")

        if count > 1:
            logger.warning(
                "Found %s events with indico id %s. Returning the first one.",
                count,
                indico_id,
            )

        return response.get("value", [])[0]

    def create_event(self, user_id: str, event: EventParameters) -> dict:
        """Create an event for a user

        Args:
            user_id (str): The user id
            event (EventParameters): The event data

        Returns:
            dict: The response of the request
        """
        data = create_event_body(event)
        return self.events_component.create_event(user_id, data)

    def update_event_by_indico_id(
        self, user_id: str, event: PartialEventParameters
    ) -> dict:
        """Update an event for a user

        Args:
            user_id (str): The user id
            event (EventParameters): The event parameters

        Returns:
            dict: The response of the request
        """
        data = create_partial_event_body(event)
        event_id = self.get_event_by_indico_id(user_id, event["indico_event_id"])["id"]
        return self.events_component.update_event(user_id, event_id, data)

    def delete_event_by_indico_id(self, user_id: str, indico_id: str) -> None:
        """Delete an event of a user

        Args:
            user_id (str): The user id
            indico_id (str): The event id

        Returns:
            dict: The response of the request
        """
        event_id = self.get_event_by_indico_id(user_id, indico_id)["id"]
        self.events_component.delete_event(user_id, event_id)
