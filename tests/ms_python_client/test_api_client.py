import unittest

import responses

from ms_python_client.api_client import ApiClient
from tests.ms_python_client.base_test_case import TEST_API_ENDPOINT


def test_api_client_build_headers_extra():
    api_client = ApiClient(TEST_API_ENDPOINT)
    headers = api_client.build_headers({"Authentication": "Bearer 12345"})
    assert headers == {
        "Authentication": "Bearer 12345",
    }


def test_api_client_build_headers_extra_no_duplicates():
    api_client = ApiClient(TEST_API_ENDPOINT)
    # pylint: disable=duplicate-key
    headers = api_client.build_headers(
        {
            "Authentication": "Bearer 12345",
            "Authentication": "Bearer 12345",
            "Content-type": "application/json",
        }
    )
    assert headers == {
        "Content-type": "application/json",
        "Authentication": "Bearer 12345",
    }


class TestApiClient(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient(TEST_API_ENDPOINT)
        self.headers = self.api_client.build_headers()

    @responses.activate
    def test_api_client_make_get_request(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/test",
            json={"response": "ok"},
            status=200,
        )
        response = self.api_client.make_get_request("/test", headers=self.headers)

        assert response.status_code == 200

    @responses.activate
    def test_api_client_make_get_request_error(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/test",
            status=400,
            json={"response": "not-ok"},
        )
        with self.assertRaises(Exception):
            self.api_client.make_get_request("/test", headers=self.headers)

    @responses.activate
    def test_api_client_make_post_request(self):
        responses.add(
            responses.POST,
            f"{TEST_API_ENDPOINT}/test",
            json={"response": "ok"},
            status=200,
        )
        json = {
            "test": "test",
        }
        response = self.api_client.make_post_request(
            "/test", headers=self.headers, json=json
        )

        assert response.status_code == 200
        assert response.request.body == b'{"test": "test"}'
        assert response.request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_api_client_make_post_request_error(self):
        responses.add(
            responses.POST,
            f"{TEST_API_ENDPOINT}/test",
            status=400,
            json={"response": "not-ok"},
        )
        with self.assertRaises(Exception):
            self.api_client.make_post_request("/test", headers=self.headers)

    @responses.activate
    def test_api_client_make_patch_request(self):
        responses.add(
            responses.PATCH,
            f"{TEST_API_ENDPOINT}/test",
            json={"response": "ok"},
            status=200,
        )
        json = {
            "test": "test",
        }
        response = self.api_client.make_patch_request(
            "/test", headers=self.headers, json=json
        )

        assert response.status_code == 200
        assert response.request.body == b'{"test": "test"}'
        assert response.request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_api_client_make_patch_request_error(self):
        responses.add(
            responses.PATCH,
            f"{TEST_API_ENDPOINT}/test",
            status=400,
            json={"response": "not-ok"},
        )
        with self.assertRaises(Exception):
            self.api_client.make_patch_request("/test", headers=self.headers)

    @responses.activate
    def test_api_client_make_delete_request(self):
        responses.add(
            responses.DELETE,
            f"{TEST_API_ENDPOINT}/test",
            json={"response": "ok"},
            status=200,
        )
        json = {
            "test": "test",
        }
        response = self.api_client.make_delete_request(
            "/test", headers=self.headers, json=json
        )

        assert response.status_code == 200
        assert response.request.body == b'{"test": "test"}'
        assert response.request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_api_client_make_delete_request_error(self):
        responses.add(
            responses.DELETE,
            f"{TEST_API_ENDPOINT}/test",
            status=400,
            json={"response": "not-ok"},
        )
        with self.assertRaises(Exception):
            self.api_client.make_delete_request("/test", headers=self.headers)
