#!/usr/bin/env python3
"""Validate daily report HTML against mobile-first UI requirements."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPORT_FILE_RE = re.compile(r"^(?P<month>\d{4}-\d{2})/(?P<section>AI|STOCK)/(?P<date>\d{8})\.html$")

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

FORBIDDEN = [
    "max-width: 920px",
]


@dataclass(frozen=True)
class ReportRef:
    kind: str
    path: Path
    report_date: str


def validate_report_html(html: str, kind: str) -> list[str]:
    """Return a list of validation error messages (empty if valid)."""
    kind = kind.upper()
    required = AI_REQUIRED if kind == "AI" else STOCK_REQUIRED
    errors: list[str] = []

    for marker in required:
        if marker not in html:
            errors.append(f"missing required marker for {kind}: {marker!r}")

    for marker in FORBIDDEN:
        if marker in html:
            errors.append(f"legacy template marker must not appear: {marker!r}")

    if "<table" in html and "table-wrap" not in html:
        errors.append("tables must be wrapped in .table-wrap")

    top_match = re.search(r'<section id="top">(.*?)</section>', html, flags=re.DOTALL)
    if top_match:
        top_html = top_match.group(1)
        if "top-list" not in top_html:
            errors.append('#top must use <ol class="top-list">')
        card_class = "news-card" if kind == "AI" else "market-card"
        if card_class not in top_html:
            errors.append(f"#top items must use .{card_class}")

    return errors


def discover_reports(root: Path, *, since: str | None = None) -> list[ReportRef]:
    reports: list[ReportRef] = []
    for path in sorted(root.glob("????-??/*/*.html")):
        relative = path.relative_to(root).as_posix()
        match = REPORT_FILE_RE.match(relative)
        if not match:
            continue
        report_date = match.group("date")
        if since and report_date < since:
            continue
        reports.append(ReportRef(kind=match.group("section"), path=path, report_date=report_date))
    return reports


def latest_reports(root: Path) -> list[ReportRef]:
    by_kind: dict[str, ReportRef] = {}
    for report in discover_reports(root):
        current = by_kind.get(report.kind)
        if current is None or report.report_date > current.report_date:
            by_kind[report.kind] = report
    if {"AI", "STOCK"}.issubset(by_kind):
        return [by_kind["AI"], by_kind["STOCK"]]
    return list(by_kind.values())


def validate_paths(reports: list[ReportRef]) -> list[str]:
    failures: list[str] = []
    for report in reports:
        html = report.path.read_text(encoding="utf-8")
        errors = validate_report_html(html, report.kind)
        for error in errors:
            failures.append(f"{report.path}: {error}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mobile-first UI in daily report HTML.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--latest", action="store_true", help="Validate latest AI and STOCK reports.")
    group.add_argument("--all-since", metavar="YYYYMMDD", help="Validate all reports on/after date.")
    parser.add_argument("--kind", choices=["AI", "STOCK"], help="Report kind with --date.")
    parser.add_argument("--date", metavar="YYYYMMDD", help="Report date with --kind.")
    args = parser.parse_args()

    root = args.root.resolve()

    if args.kind and args.date:
        month = f"{args.date[0:4]}-{args.date[4:6]}"
        path = root / month / args.kind / f"{args.date}.html"
        if not path.exists():
            print(f"Report not found: {path}", file=sys.stderr)
            return 1
        reports = [ReportRef(kind=args.kind, path=path, report_date=args.date)]
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
