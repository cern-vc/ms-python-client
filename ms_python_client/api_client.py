import logging
from typing import Any, Mapping, Optional

from requests import RequestException, Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger("ms_python_client")

_Headers = Mapping[str, str]
_Data = Mapping[str, Any]


class ApiClient:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.timeout = 10
        self.session = Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def build_headers(self, extra_headers: Optional[_Headers] = None) -> dict:
        """Create the headers for a request appending the ones in the params

        Args:
            extra_headers (dict): Mapping of headers that will be appended to the default ones

        Returns:
            dict: All the headers
        """
        headers: dict[str, str] = {}
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def make_get_request(self, api_path: str, headers: _Headers) -> Response:
        """Makes a GET request using requests

        Args:
            api_path (str): The URL path
            headers (dict): The headers of the request

        Returns:
            Response: The response of the request
        """
        response = None
        full_url = self.api_base_url + api_path
        logger.info("GET %s", api_path)
        try:
            response = self.session.get(full_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except RequestException as e:
            logger.error(e)
            if isinstance(response, Response) and response.text:
                logger.error(response.text)
            raise e
        logger.debug(
            "GET [%s] - %d in %fs",
            api_path,
            response.status_code,
            response.elapsed.total_seconds(),
        )
        return response

    def make_post_request(
        self, api_path: str, headers: _Headers, json: Optional[_Data] = None
    ) -> Response:
        """Makes a POST request using requests

        Args:
            api_path (str): The URL path
            headers (dict): The headers of the request
            json (dict): The body of the request

        Returns:
            Response: The response of the request
        """
        response = None
        full_url = self.api_base_url + api_path
        logger.info("POST %s", api_path)
        try:
            response = self.session.post(
                full_url, headers=headers, json=json, timeout=self.timeout
            )
            response.raise_for_status()
        except RequestException as e:
            logger.error(e)
            if isinstance(response, Response) and response.text:
                logger.error(response.text)
            raise e
        logger.debug(
            "POST [%s] - %d in %fs",
            api_path,
            response.status_code,
            response.elapsed.total_seconds(),
        )
        return response

    def make_patch_request(
        self, api_path: str, headers: _Headers, json: Optional[_Data] = None
    ) -> Response:
        """Makes a PATCH request using requests

        Args:
            api_path (str): The URL path
            headers (dict): The headers of the request
            json (dict): The body of the request

        Returns:
            Response: The response of the request
        """
        response = None
        full_url = self.api_base_url + api_path
        logger.info("PATCH %s", api_path)
        try:
            response = self.session.patch(
                full_url, headers=headers, json=json, timeout=self.timeout
            )
            response.raise_for_status()
        except RequestException as e:
            logger.error(e)
            if isinstance(response, Response) and response.text:
                logger.error(response.text)
            raise e
        logger.debug(
            "PATCH [%s] - %d in %fs",
            api_path,
            response.status_code,
            response.elapsed.total_seconds(),
        )
        return response

    def make_delete_request(
        self, api_path: str, headers: _Headers, json: Optional[_Data] = None
    ) -> Response:
        """Makes a DELETE request using requests

        Args:
            api_path (str): The URL path
            headers (dict): The headers of the request
            json (dict): The body of the request

        Returns:
            Response: The response of the request
        """
        response = None
        full_url = self.api_base_url + api_path
        logger.info("DELETE %s", api_path)
        try:
            response = self.session.delete(
                full_url, headers=headers, json=json, timeout=self.timeout
            )
            response.raise_for_status()
        except RequestException as e:
            logger.error(e)
            if isinstance(response, Response) and response.text:
                logger.error(response.text)
            raise e
        logger.debug(
            "DELETE [%s] - %d in %fs",
            api_path,
            response.status_code,
            response.elapsed.total_seconds(),
        )
        return response
