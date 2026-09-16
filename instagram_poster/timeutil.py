from datetime import datetime
from zoneinfo import ZoneInfo

DEFAULT_TZ = ZoneInfo("Africa/Nairobi")


def parse_local_time(value: str) -> datetime:
    """Accepts either a full ISO 8601 timestamp with offset, or a bare
    'YYYY-MM-DD HH:MM' string assumed to be in Africa/Nairobi time.
    """
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Could not parse time {value!r}; use ISO 8601 or 'YYYY-MM-DD HH:MM'") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=DEFAULT_TZ)
    return dt
