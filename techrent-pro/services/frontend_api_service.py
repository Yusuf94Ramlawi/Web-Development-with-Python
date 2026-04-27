"""Frontend service helpers for calling internal API endpoints."""
from flask import current_app


def request_api(method, path, query=None, json_data=None):
    """
    Perform an internal API request through Flask's test client.

    Args:
        method: HTTP method string.
        path: API path, e.g. '/api/equipment'.
        query: Optional query-string dict.
        json_data: Optional JSON body dict.

    Returns:
        tuple: (status_code, parsed_json_payload)
    """
    with current_app.test_client() as client:
        response = client.open(
            path,
            method=method,
            query_string=query,
            json=json_data,
        )

    payload = response.get_json(silent=True)
    if payload is None:
        payload = {}

    return response.status_code, payload


def get(path, query=None):
    return request_api("GET", path, query=query)


def post(path, json_data=None):
    return request_api("POST", path, json_data=json_data)


def put(path, json_data=None):
    return request_api("PUT", path, json_data=json_data)


def delete(path):
    return request_api("DELETE", path)


def extract_errors(payload):
    """
    Normalize API error payloads into template-friendly field errors.

    Args:
        payload: JSON payload returned by API.

    Returns:
        dict: Field-level errors dictionary.
    """
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, dict):
            return errors
        if payload.get("error"):
            return {"form": payload["error"]}
    return {}
