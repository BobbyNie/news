"""Tests for Macau report date helpers."""

from scripts.report_date import (
    collection_window,
    format_generated_at,
    macau_datetime,
    report_date_compact,
    report_date_iso,
    report_month_dir,
)


def test_trigger_at_utc_23_maps_to_macau_next_day():
    # Cron 23:02 UTC = 07:02 Macau next calendar day
    triggered = "2026-05-27T23:02:33.581Z"
    assert report_date_compact(triggered) == "20260528"
    assert report_date_iso(triggered) == "2026-05-28"
    assert report_month_dir(triggered) == "2026-05"


def test_generated_at_uses_macau_timezone():
    triggered = "2026-05-27T23:02:33.581Z"
    assert format_generated_at(triggered) == "2026-05-28 07:02（澳门时间）"


def test_collection_window_is_48_hours_ending_at_trigger():
    triggered = "2026-05-27T23:02:33.581Z"
    start, end = collection_window(triggered, hours=48)
    assert start == "2026-05-26 07:02"
    assert end == "2026-05-28 07:02"


def test_macau_datetime_rejects_naive_input():
    dt = macau_datetime("2026-05-27T23:02:33.581Z")
    assert dt.tzinfo is not None
    assert dt.hour == 7
    assert dt.day == 28
