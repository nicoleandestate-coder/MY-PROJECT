import tempfile
from datetime import datetime, timedelta, timezone

import pytest

from instagram_poster import config, queue


@pytest.fixture(autouse=True)
def temp_queue_file(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        f.write(b"[]")
        path = f.name
    monkeypatch.setattr(config, "QUEUE_FILE", path)
    yield path


def test_add_and_list_post():
    scheduled = datetime.now(timezone.utc) + timedelta(days=1)
    post = queue.add_post("IMAGE", "test caption", scheduled, media_url="https://example.com/a.jpg")
    posts = queue.load_all()
    assert len(posts) == 1
    assert posts[0]["id"] == post["id"]
    assert posts[0]["status"] == "pending"


def test_due_posts_only_returns_past_pending():
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    future = datetime.now(timezone.utc) + timedelta(days=1)
    due_post = queue.add_post("IMAGE", "due", past, media_url="https://example.com/a.jpg")
    queue.add_post("IMAGE", "not due", future, media_url="https://example.com/b.jpg")

    due = queue.due_posts()
    assert [p["id"] for p in due] == [due_post["id"]]


def test_add_post_requires_tz_aware_time():
    with pytest.raises(ValueError):
        queue.add_post("IMAGE", "caption", datetime.now(), media_url="https://example.com/a.jpg")


def test_carousel_requires_carousel_urls():
    with pytest.raises(ValueError):
        queue.add_post("CAROUSEL", "caption", datetime.now(timezone.utc) + timedelta(days=1))
