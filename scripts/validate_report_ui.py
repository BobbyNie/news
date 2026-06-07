#!/usr/bin/env python3
"""Validate daily report HTML against mobile-first UI requirements."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DAILY_REPORT_FILE_RE = re.compile(r"^(?P<month>\d{4}-\d{2})/(?P<section>AI|STOCK)/(?P<date>\d{8})\.html$")
WEEKLY_REPORT_FILE_RE = re.compile(r"^(?P<month>\d{4}-\d{2})/(?P<year>\d{4})-W(?P<week>\d{2})\.html$")
WEEKLY_DATE_RE = re.compile(r"^(?P<year>\d{4})-W(?P<week>\d{2})$")

AI_REQUIRED = [
    "AI DAILY BRIEF",
    "hero hero-ai",
    "top-list",
    "news-card",
    "table-wrap",
    "-webkit-text-size-adjust",
    "max-width: 760px",
    'class="report report-ai"',
]

STOCK_REQUIRED = [
    "MARKET DAILY BRIEF",
    "hero hero-stock",
    "top-list",
    "market-card",
    "change-up",
    "table-wrap",
    "-webkit-text-size-adjust",
    "max-width: 780px",
    'class="report report-stock"',
]

WEEKLY_REQUIRED = [
    "AI + MARKET WEEKLY BRIEF",
    "hero hero-weekly",
    "top-list",
    "weekly-card",
    "table-wrap",
    "-webkit-text-size-adjust",
    "max-width: 800px",
    'class="report report-weekly"',
]

REQUIRED_BY_KIND = {
    "AI": AI_REQUIRED,
    "STOCK": STOCK_REQUIRED,
    "WEEKLY": WEEKLY_REQUIRED,
}

TOP_CARD_CLASS_BY_KIND = {
    "AI": "news-card",
    "STOCK": "market-card",
    "WEEKLY": "weekly-card",
}

FORBIDDEN = [
    "max-width: 920px",
]

AI_FINANCE_APPLICATION_MARKERS = [
    'section id="finance-ai-applications"',
    # Backward compatibility for already-published reports before the application-focused section name.
    'section id="finance-ai"',
]

READ_ALOUD_REQUIRED_SINCE = "20260608"
READ_ALOUD_REQUIRED = [
    "reader-controls",
    "data-reader-controls",
    "speechSynthesis",
    "SpeechSynthesisUtterance",
]


@dataclass(frozen=True)
class ReportRef:
    kind: str
    path: Path
    report_date: str


def parse_weekly_report_end_date(year: str, week: str) -> date:
    return date.fromisocalendar(int(year), int(week), 7)


def parse_weekly_report_date(year: str, week: str) -> str:
    return parse_weekly_report_end_date(year, week).strftime("%Y%m%d")


def validate_report_html(html: str, kind: str, *, report_date: str | None = None) -> list[str]:
    """Return a list of validation error messages (empty if valid)."""
    kind = kind.upper()
    required = REQUIRED_BY_KIND[kind]
    errors: list[str] = []

    for marker in required:
        if marker not in html:
            errors.append(f"missing required marker for {kind}: {marker!r}")

    for marker in FORBIDDEN:
        if marker in html:
            errors.append(f"legacy template marker must not appear: {marker!r}")

    if kind == "AI" and not any(marker in html for marker in AI_FINANCE_APPLICATION_MARKERS):
        errors.append('missing required marker for AI: \'section id="finance-ai-applications"\'')

    if report_date and report_date >= READ_ALOUD_REQUIRED_SINCE:
        for marker in READ_ALOUD_REQUIRED:
            if marker not in html:
                errors.append(f"missing required read-aloud marker for {kind}: {marker!r}")

    if "<table" in html and "table-wrap" not in html:
        errors.append("tables must be wrapped in .table-wrap")

    top_match = re.search(r'<section id="top">(.*?)</section>', html, flags=re.DOTALL)
    if top_match:
        top_html = top_match.group(1)
        if "top-list" not in top_html:
            errors.append('#top must use <ol class="top-list">')
        card_class = TOP_CARD_CLASS_BY_KIND[kind]
        if card_class not in top_html:
            errors.append(f"#top items must use .{card_class}")

    return errors


def discover_reports(root: Path, *, since: str | None = None) -> list[ReportRef]:
    reports: list[ReportRef] = []
    paths = [*root.glob("????-??/*/*.html"), *root.glob("????-??/*.html")]
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        daily_match = DAILY_REPORT_FILE_RE.match(relative)
        if daily_match:
            report_date = daily_match.group("date")
            if since and report_date < since:
                continue
            reports.append(ReportRef(kind=daily_match.group("section"), path=path, report_date=report_date))
            continue

        weekly_match = WEEKLY_REPORT_FILE_RE.match(relative)
        if not weekly_match:
            continue
        report_date = parse_weekly_report_date(weekly_match.group("year"), weekly_match.group("week"))
        if since and report_date < since:
            continue
        reports.append(ReportRef(kind="WEEKLY", path=path, report_date=report_date))
    return reports


def latest_reports(root: Path) -> list[ReportRef]:
    by_kind: dict[str, ReportRef] = {}
    for report in discover_reports(root):
        current = by_kind.get(report.kind)
        if current is None or report.report_date > current.report_date:
            by_kind[report.kind] = report
    ordered_kinds = ["AI", "STOCK", "WEEKLY"]
    return [by_kind[kind] for kind in ordered_kinds if kind in by_kind]


def validate_paths(reports: list[ReportRef]) -> list[str]:
    failures: list[str] = []
    for report in reports:
        html = report.path.read_text(encoding="utf-8")
        errors = validate_report_html(html, report.kind, report_date=report.report_date)
        for error in errors:
            failures.append(f"{report.path}: {error}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mobile-first UI in daily report HTML.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--latest", action="store_true", help="Validate latest AI, STOCK, and WEEKLY reports.")
    group.add_argument("--all-since", metavar="YYYYMMDD", help="Validate all reports on/after date.")
    parser.add_argument("--kind", choices=["AI", "STOCK", "WEEKLY"], help="Report kind with --date.")
    parser.add_argument("--date", metavar="YYYYMMDD|YYYY-Www", help="Report date with --kind.")
    args = parser.parse_args()

    root = args.root.resolve()

    if args.kind and args.date:
        if args.kind == "WEEKLY":
            match = WEEKLY_DATE_RE.match(args.date)
            if not match:
                print(f"Weekly report date must use YYYY-Www: {args.date}", file=sys.stderr)
                return 1
            week_end = parse_weekly_report_end_date(match.group("year"), match.group("week"))
            report_date = week_end.strftime("%Y%m%d")
            path = root / week_end.strftime("%Y-%m") / f"{args.date}.html"
        else:
            report_date = args.date
            month = f"{args.date[0:4]}-{args.date[4:6]}"
            path = root / month / args.kind / f"{args.date}.html"
        if not path.exists():
            print(f"Report not found: {path}", file=sys.stderr)
            return 1
        reports = [ReportRef(kind=args.kind, path=path, report_date=report_date)]
    elif args.all_since:
        reports = discover_reports(root, since=args.all_since)
    else:
        reports = latest_reports(root)

    if not reports:
        print("No reports found to validate.", file=sys.stderr)
        return 1

    failures = validate_paths(reports)
    if failures:
        print("Report UI validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    names = ", ".join(report.path.relative_to(root).as_posix() for report in reports)
    print(f"OK: {names}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
