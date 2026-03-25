from unittest.mock import Mock, patch

import requests

from src.ingest.greenhouse_connector import GreenhouseConnector


def test_fetch_payload_retries_then_succeeds():
    connector = GreenhouseConnector(board_token="acme", max_attempts=3)

    responses = [
        requests.RequestException("temporary failure"),
        Mock(json=lambda: {"jobs": []}, raise_for_status=lambda: None),
    ]

    def fake_get(*args, **kwargs):
        result = responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    with patch("src.ingest.greenhouse_connector.requests.get", side_effect=fake_get):
        payload = connector._fetch_payload("https://example.com")

    assert payload == {"jobs": []}
