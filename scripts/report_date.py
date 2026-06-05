#!/usr/bin/env python3
"""Resolve daily report dates in Asia/Macau timezone."""

from __future__ import annotations

import argparse
import shlex
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

MACAU_TZ = ZoneInfo("Asia/Macau")


def macau_now() -> datetime:
    return datetime.now(MACAU_TZ)


def macau_datetime(iso_utc: str) -> datetime:
    """Convert an ISO-8601 UTC timestamp to Asia/Macau local time."""
    normalized = iso_utc.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(MACAU_TZ)


def resolve_trigger(triggered_at: str | None = None, report_day: date | None = None) -> datetime:
    if triggered_at:
        return macau_datetime(triggered_at)
    if report_day:
        # Backfill: assume morning automation run at 07:00 Macau
        return datetime(report_day.year, report_day.month, report_day.day, 7, 0, 0, tzinfo=MACAU_TZ)
    return macau_now()


def report_yyyymmdd(dt: datetime) -> str:
    return dt.strftime("%Y%m%d")


def report_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def report_month(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def format_generated_at(dt: datetime) -> str:
    return f"{dt.strftime('%Y-%m-%d %H:%M')}（澳门时间）"


def collection_window_from_trigger(dt: datetime, hours: int = 48) -> tuple[str, str]:
    start = dt - timedelta(hours=hours)
    fmt = "%Y-%m-%d %H:%M"
    return start.strftime(fmt), dt.strftime(fmt)


def format_window(dt: datetime, hours: int = 48) -> str:
    start, end = collection_window_from_trigger(dt, hours)
    return f"{start} ~ {end}（澳门时间 UTC+8）"


def emit_env(triggered_at: str | None = None, report_day: date | None = None) -> None:
    dt = resolve_trigger(triggered_at, report_day)
    values = {
        "REPORT_DATE": report_yyyymmdd(dt),
        "REPORT_ISO": report_iso(dt),
        "REPORT_MONTH": report_month(dt),
        "REPORT_WINDOW": format_window(dt),
        "REPORT_GENERATED_AT": format_generated_at(dt),
        "REPORT_TZ": "Asia/Macau",
    }
    for key, value in values.items():
        print(f"export {key}={shlex.quote(value)}")


def print_details(triggered_at: str) -> None:
    dt = resolve_trigger(triggered_at)
    start, end = collection_window_from_trigger(dt)
    print(f"report_date={report_yyyymmdd(dt)}")
    print(f"report_date_iso={report_iso(dt)}")
    print(f"month_dir={report_month(dt)}")
    print(f"generated_at={format_generated_at(dt)}")
    print(f"window_start={start}")
    print(f"window_end={end}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print Macau report date variables.")
    parser.add_argument(
        "triggered_at",
        nargs="?",
        help="ISO UTC timestamp from automation_trigger_info.triggeredAt",
    )
    parser.add_argument(
        "--date",
        help="Override report day as YYYY-MM-DD (for tests or backfill).",
    )
    args = parser.parse_args()

    report_day = date.fromisoformat(args.date) if args.date else None

    if args.triggered_at:
        emit_env(triggered_at=args.triggered_at)
    else:
        emit_env(report_day=report_day)


if __name__ == "__main__":
    main()
