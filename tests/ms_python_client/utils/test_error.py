from requests import HTTPError, Response

from ms_python_client.utils.error import generate_error_log


def test_generate_error_log():
    response = Response()
    response.status_code = 400
    error = HTTPError("Error decoding the response", response=response)

    error_output = {
        "error": "Error decoding the response",
        "status_code": 400,
        "response": "",
    }

    assert generate_error_log(error) == error_output
