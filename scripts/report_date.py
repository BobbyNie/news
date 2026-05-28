"""Macau timezone helpers for daily report naming and metadata."""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

MACAU_TZ = ZoneInfo("Asia/Macau")


def macau_datetime(iso_utc: str) -> datetime:
    """Convert an ISO-8601 UTC timestamp to Asia/Macau local time."""
    normalized = iso_utc.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(MACAU_TZ)


def report_date_compact(iso_utc: str) -> str:
    """YYYYMMDD in Macau time — used for filenames and tmp paths."""
    return macau_datetime(iso_utc).strftime("%Y%m%d")


def report_date_iso(iso_utc: str) -> str:
    """YYYY-MM-DD in Macau time — used for titles and commit messages."""
    return macau_datetime(iso_utc).strftime("%Y-%m-%d")


def report_month_dir(iso_utc: str) -> str:
    """YYYY-MM directory segment in Macau time."""
    return macau_datetime(iso_utc).strftime("%Y-%m")


def format_generated_at(iso_utc: str) -> str:
    """Human-readable generation timestamp for HTML metadata."""
    dt = macau_datetime(iso_utc)
    return f"{dt.strftime('%Y-%m-%d %H:%M')}（澳门时间）"


def collection_window(iso_utc: str, hours: int = 48) -> tuple[str, str]:
    """Return (start, end) collection window strings in Macau time."""
    end = macau_datetime(iso_utc)
    start = end - timedelta(hours=hours)
    fmt = "%Y-%m-%d %H:%M"
    return start.strftime(fmt), end.strftime(fmt)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/report_date.py <ISO-UTC-timestamp>")

    ts = sys.argv[1]
    start, end = collection_window(ts)
    print(f"report_date={report_date_compact(ts)}")
    print(f"report_date_iso={report_date_iso(ts)}")
    print(f"month_dir={report_month_dir(ts)}")
    print(f"generated_at={format_generated_at(ts)}")
    print(f"window_start={start}")
    print(f"window_end={end}")
