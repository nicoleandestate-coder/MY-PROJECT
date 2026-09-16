import os

from dotenv import load_dotenv

load_dotenv()

GRAPH_API_VERSION = os.environ.get("GRAPH_API_VERSION", "v21.0")
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")

QUEUE_FILE = os.environ.get(
    "INSTAGRAM_QUEUE_FILE",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "posts_queue.json"),
)

# Instagram's per-account rolling limit on container publishes.
DAILY_PUBLISH_LIMIT = int(os.environ.get("INSTAGRAM_DAILY_PUBLISH_LIMIT", "25"))


def require_credentials() -> None:
    missing = [
        name
        for name, value in (
            ("INSTAGRAM_ACCESS_TOKEN", ACCESS_TOKEN),
            ("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". See SETUP.md for how to obtain them."
        )
