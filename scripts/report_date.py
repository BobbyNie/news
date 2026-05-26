#!/usr/bin/env python3
"""Resolve daily report dates in Asia/Macau timezone."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

MACAU_TZ = ZoneInfo("Asia/Macau")


def macau_now() -> datetime:
    return datetime.now(MACAU_TZ)


def macau_today() -> date:
    return macau_now().date()


def report_yyyymmdd(report_day: date | None = None) -> str:
    day = report_day or macau_today()
    return day.strftime("%Y%m%d")


def report_iso(report_day: date | None = None) -> str:
    day = report_day or macau_today()
    return day.isoformat()


def report_month(report_day: date | None = None) -> str:
    day = report_day or macau_today()
    return day.strftime("%Y-%m")


def collection_window(report_day: date | None = None) -> tuple[datetime, datetime]:
    """Previous calendar day 22:00 through report day 22:00, Macau time."""
    day = report_day or macau_today()
    end = datetime(day.year, day.month, day.day, 22, 0, 0, tzinfo=MACAU_TZ)
    start = end - timedelta(days=2)
    return start, end


def format_window(report_day: date | None = None) -> str:
    start, end = collection_window(report_day)
    fmt = "%Y-%m-%d %H:%M"
    return f"{start.strftime(fmt)} ~ {end.strftime(fmt)}（澳门时间 UTC+8）"


def emit_env(report_day: date | None = None) -> None:
    day = report_day or macau_today()
    values = {
        "REPORT_DATE": report_yyyymmdd(day),
        "REPORT_ISO": report_iso(day),
        "REPORT_MONTH": report_month(day),
        "REPORT_WINDOW": format_window(day),
        "REPORT_TZ": "Asia/Macau",
    }
    for key, value in values.items():
        print(f"{key}={value}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print Macau report date variables.")
    parser.add_argument(
        "--date",
        help="Override report day as YYYY-MM-DD (for tests or backfill).",
    )
    args = parser.parse_args()

    report_day = None
    if args.date:
        report_day = date.fromisoformat(args.date)

    emit_env(report_day)


if __name__ == "__main__":
    main()
