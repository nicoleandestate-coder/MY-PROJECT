"""A simple JSON-file backed queue of posts waiting to go out.

Kept deliberately simple (no database) since this is a low-volume,
single-account posting system. Safe for one process at a time.
"""
import json
import os
import uuid
from datetime import datetime, timezone

from instagram_poster import config

VALID_STATUSES = {"pending", "posted", "failed", "cancelled"}
VALID_MEDIA_TYPES = {"IMAGE", "REELS", "VIDEO", "CAROUSEL"}


def _ensure_queue_file() -> None:
    os.makedirs(os.path.dirname(config.QUEUE_FILE), exist_ok=True)
    if not os.path.exists(config.QUEUE_FILE):
        with open(config.QUEUE_FILE, "w") as f:
            json.dump([], f)


def load_all() -> list:
    _ensure_queue_file()
    with open(config.QUEUE_FILE) as f:
        return json.load(f)


def save_all(posts: list) -> None:
    _ensure_queue_file()
    with open(config.QUEUE_FILE, "w") as f:
        json.dump(posts, f, indent=2, default=str)


def add_post(
    media_type: str,
    caption: str,
    scheduled_time: datetime,
    media_url: str = None,
    carousel_urls: list = None,
) -> dict:
    media_type = media_type.upper()
    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError(f"media_type must be one of {sorted(VALID_MEDIA_TYPES)}")
    if media_type == "CAROUSEL" and not carousel_urls:
        raise ValueError("CAROUSEL posts require carousel_urls")
    if media_type != "CAROUSEL" and not media_url:
        raise ValueError(f"{media_type} posts require media_url")
    if scheduled_time.tzinfo is None:
        raise ValueError("scheduled_time must be timezone-aware")

    post = {
        "id": str(uuid.uuid4()),
        "media_type": media_type,
        "media_url": media_url,
        "carousel_urls": carousel_urls,
        "caption": caption,
        "scheduled_time": scheduled_time.astimezone(timezone.utc).isoformat(),
        "status": "pending",
        "ig_media_id": None,
        "error": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "posted_at": None,
    }
    posts = load_all()
    posts.append(post)
    save_all(posts)
    return post


def due_posts(now: datetime = None) -> list:
    now = now or datetime.now(timezone.utc)
    return [
        p
        for p in load_all()
        if p["status"] == "pending" and datetime.fromisoformat(p["scheduled_time"]) <= now
    ]


def update_post(post_id: str, **fields) -> dict:
    posts = load_all()
    for post in posts:
        if post["id"] == post_id:
            post.update(fields)
            save_all(posts)
            return post
    raise KeyError(f"No queued post with id {post_id}")


def cancel_post(post_id: str) -> dict:
    return update_post(post_id, status="cancelled")
