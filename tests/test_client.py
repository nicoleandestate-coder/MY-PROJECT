from unittest.mock import patch

from instagram_poster import client


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)

    def json(self):
        return self._json


@patch("instagram_poster.client.requests.request")
def test_create_image_container(mock_request):
    mock_request.return_value = FakeResponse({"id": "container123"})
    creation_id = client.create_image_container("https://example.com/photo.jpg", "hello")
    assert creation_id == "container123"
    _, kwargs = mock_request.call_args
    assert kwargs["params"]["image_url"] == "https://example.com/photo.jpg"
    assert kwargs["params"]["caption"] == "hello"


@patch("instagram_poster.client.requests.request")
def test_publish_container(mock_request):
    mock_request.return_value = FakeResponse({"id": "media456"})
    media_id = client.publish_container("container123")
    assert media_id == "media456"


@patch("instagram_poster.client.requests.request")
def test_error_response_raises(mock_request):
    mock_request.return_value = FakeResponse({"error": {"message": "bad token"}}, status_code=400)
    try:
        client.create_image_container("https://example.com/photo.jpg", "hello")
        assert False, "expected InstagramAPIError"
    except client.InstagramAPIError as exc:
        assert "bad token" in str(exc)
