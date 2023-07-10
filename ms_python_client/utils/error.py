from json import JSONDecodeError

from requests import HTTPError


def generate_error_log(error: HTTPError) -> dict:
    try:
        response = error.response.json()
    except JSONDecodeError:
        response = error.response.text
    output = {
        "error": str(error),
        "status_code": error.response.status_code,
        "response": response,
    }
    return output
