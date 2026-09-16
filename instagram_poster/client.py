"""Thin wrapper around the Instagram Graph API's content publishing endpoints.

Reference: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing
"""
import time

import requests

from instagram_poster import config


class InstagramAPIError(RuntimeError):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


def _request(method, path, **kwargs):
    url = f"{config.GRAPH_API_BASE_URL}/{path}"
    params = kwargs.pop("params", {})
    params.setdefault("access_token", config.ACCESS_TOKEN)
    response = requests.request(method, url, params=params, timeout=30, **kwargs)
    if response.status_code >= 400:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise InstagramAPIError(f"{method} {path} failed: {detail}", response=response)
    return response.json()


def create_image_container(image_url: str, caption: str = "") -> str:
    data = _request(
        "POST",
        f"{config.IG_USER_ID}/media",
        params={"image_url": image_url, "caption": caption},
    )
    return data["id"]


def create_video_container(video_url: str, caption: str = "", media_type: str = "REELS") -> str:
    data = _request(
        "POST",
        f"{config.IG_USER_ID}/media",
        params={"video_url": video_url, "caption": caption, "media_type": media_type},
    )
    return data["id"]


def create_carousel_item_container(image_url: str = None, video_url: str = None) -> str:
    if not image_url and not video_url:
        raise ValueError("Carousel item needs either image_url or video_url")
    params = {"is_carousel_item": "true"}
    if image_url:
        params["image_url"] = image_url
    else:
        params["video_url"] = video_url
        params["media_type"] = "VIDEO"
    data = _request("POST", f"{config.IG_USER_ID}/media", params=params)
    return data["id"]


def create_carousel_container(children_ids: list, caption: str = "") -> str:
    data = _request(
        "POST",
        f"{config.IG_USER_ID}/media",
        params={
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "caption": caption,
        },
    )
    return data["id"]


def get_container_status(creation_id: str) -> str:
    data = _request("GET", creation_id, params={"fields": "status_code"})
    return data["status_code"]


def wait_for_container_ready(creation_id: str, timeout_seconds: int = 300, poll_interval: int = 5) -> None:
    """Videos/reels are processed asynchronously; poll until FINISHED before publishing."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        status = get_container_status(creation_id)
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise InstagramAPIError(f"Container {creation_id} failed processing")
        time.sleep(poll_interval)
    raise InstagramAPIError(f"Container {creation_id} did not finish processing within {timeout_seconds}s")


def publish_container(creation_id: str) -> str:
    data = _request(
        "POST",
        f"{config.IG_USER_ID}/media_publish",
        params={"creation_id": creation_id},
    )
    return data["id"]


def get_publishing_limit() -> dict:
    """Remaining quota out of the rolling 24h publish limit for this account."""
    return _request(
        "GET",
        f"{config.IG_USER_ID}/content_publishing_limit",
        params={"fields": "config,quota_usage"},
    )
