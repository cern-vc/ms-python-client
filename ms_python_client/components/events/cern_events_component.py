import logging
from typing import Mapping, Optional

from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.ms_client_interface import MSClientInterface
from ms_python_client.utils.event_generator import (
    ZOOM_ID_EXTENDED_PROPERTY_ID,
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
        self,
        user_id: str,
        parameters: Optional[Mapping[str, str]] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """List all the events of a user

        Args:
            user_id (str): The user id
            parameters (dict): Optional parameters for the request

        Returns:
            dict: The response of the request
        """
        return self.events_component.list_events(user_id, parameters, extra_headers)

    def get_event_by_zoom_id(
        self,
        user_id: str,
        zoom_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Get an event of a user

        Args:
            zoom_id (str): The event id

        Returns:
            dict: The response of the request
        """
        parameters = {
            "$count": "true",
            "$filter": f"singleValueExtendedProperties/Any(ep: ep/id eq \
                '{ZOOM_ID_EXTENDED_PROPERTY_ID}' and ep/value eq '{zoom_id}')",
            "$expand": f"singleValueExtendedProperties($filter=id eq \
                '{ZOOM_ID_EXTENDED_PROPERTY_ID}')",
        }
        response = self.events_component.list_events(user_id, parameters, extra_headers)

        count = response.get("@odata.count", 0)
        if count == 0:
            raise NotFoundError(f"Event with zoom id {zoom_id} not found")

        if count > 1:
            logger.warning(
                "Found %s events with zoom id %s. Returning the first one.",
                count,
                zoom_id,
            )

        return response.get("value", [])[0]

    def create_event(
        self,
        user_id: str,
        event: EventParameters,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Create an event for a user

        Args:
            user_id (str): The user id
            event (EventParameters): The event data

        Returns:
            dict: The response of the request
        """
        json = create_event_body(event)
        return self.events_component.create_event(user_id, json, extra_headers)

    def update_event_by_zoom_id(
        self,
        user_id: str,
        event: PartialEventParameters,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Update an event for a user

        Args:
            user_id (str): The user id
            event (EventParameters): The event parameters

        Returns:
            dict: The response of the request
        """
        json = create_partial_event_body(event)
        event_id = self.get_event_by_zoom_id(user_id, event["zoom_id"], extra_headers)[
            "id"
        ]
        return self.events_component.update_event(
            user_id, event_id, json, extra_headers
        )

    def delete_event_by_zoom_id(
        self,
        user_id: str,
        zoom_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Delete an event of a user

        Args:
            user_id (str): The user id
            zoom_id (str): The event id

        Returns:
            dict: The response of the request
        """
        event_id = self.get_event_by_zoom_id(user_id, zoom_id, extra_headers)["id"]
        self.events_component.delete_event(user_id, event_id, extra_headers)
