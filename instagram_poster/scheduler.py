"""Publishes any due posts from the queue. Intended to be run periodically
(e.g. every 5-15 minutes via cron), not as a long-lived process.
"""
import logging
from datetime import datetime, timezone

from instagram_poster import client, config, queue

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _publish_one(post: dict) -> None:
    media_type = post["media_type"]
    caption = post.get("caption", "")

    if media_type == "IMAGE":
        creation_id = client.create_image_container(post["media_url"], caption)
    elif media_type in ("REELS", "VIDEO"):
        creation_id = client.create_video_container(post["media_url"], caption, media_type=media_type)
        client.wait_for_container_ready(creation_id)
    elif media_type == "CAROUSEL":
        child_ids = [client.create_carousel_item_container(image_url=url) for url in post["carousel_urls"]]
        creation_id = client.create_carousel_container(child_ids, caption)
    else:
        raise ValueError(f"Unsupported media_type: {media_type}")

    media_id = client.publish_container(creation_id)
    queue.update_post(
        post["id"],
        status="posted",
        ig_media_id=media_id,
        posted_at=datetime.now(timezone.utc).isoformat(),
        error=None,
    )
    logger.info("Published post %s as Instagram media %s", post["id"], media_id)


def run_once() -> None:
    config.require_credentials()

    try:
        limit_info = client.get_publishing_limit()
        quota = limit_info.get("data", [{}])[0].get("quota_usage")
        if quota is not None and quota >= config.DAILY_PUBLISH_LIMIT:
            logger.warning("Daily publish limit reached (%s/%s), skipping this run", quota, config.DAILY_PUBLISH_LIMIT)
            return
    except client.InstagramAPIError as exc:
        logger.warning("Could not check publishing limit, proceeding anyway: %s", exc)

    due = queue.due_posts()
    if not due:
        logger.info("No due posts.")
        return

    for post in due:
        logger.info("Publishing post %s (%s)", post["id"], post["media_type"])
        try:
            _publish_one(post)
        except Exception as exc:  # noqa: BLE001 - keep processing the rest of the queue
            logger.exception("Failed to publish post %s", post["id"])
            queue.update_post(post["id"], status="failed", error=str(exc))


if __name__ == "__main__":
    run_once()
