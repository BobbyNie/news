#!/usr/bin/env python3
"""Build the GitHub Pages site index for generated news reports."""

from __future__ import annotations

import argparse
import html
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DAILY_REPORT_PATH_RE = re.compile(r"^(?P<month>\d{4}-\d{2})/(?P<section>AI|STOCK)/(?P<date>\d{8})\.html$")
WEEKLY_REPORT_PATH_RE = re.compile(r"^(?P<month>\d{4}-\d{2})/(?P<year>\d{4})-W(?P<week>\d{2})\.html$")
SECTION_LABELS = {
    "AI": "AI 日报",
    "STOCK": "股市日报",
    "WEEKLY": "AI + 股市周报",
}
SECTION_ORDER = {
    "AI": 0,
    "STOCK": 1,
    "WEEKLY": 2,
}


@dataclass(frozen=True)
class Report:
    report_date: date
    section: str
    relative_path: str
    title: str

    @property
    def section_label(self) -> str:
        return SECTION_LABELS[self.section]

    @property
    def display_date(self) -> str:
        return self.report_date.isoformat()


def parse_report_date(value: str) -> date:
    return date(int(value[0:4]), int(value[4:6]), int(value[6:8]))


def parse_weekly_report_date(year: str, week: str) -> date:
    return date.fromisocalendar(int(year), int(week), 7)


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return path.stem
    return re.sub(r"\s+", " ", match.group(1)).strip()


def discover_reports(root: Path) -> list[Report]:
    reports: list[Report] = []
    paths = [*root.glob("????-??/*/*.html"), *root.glob("????-??/*.html")]
    for path in sorted(paths):
        relative_path = path.relative_to(root).as_posix()
        daily_match = DAILY_REPORT_PATH_RE.match(relative_path)
        if daily_match:
            reports.append(
                Report(
                    report_date=parse_report_date(daily_match.group("date")),
                    section=daily_match.group("section"),
                    relative_path=relative_path,
                    title=extract_title(path),
                )
            )
            continue

        weekly_match = WEEKLY_REPORT_PATH_RE.match(relative_path)
        if not weekly_match:
            continue
        reports.append(
            Report(
                report_date=parse_weekly_report_date(weekly_match.group("year"), weekly_match.group("week")),
                section="WEEKLY",
                relative_path=relative_path,
                title=extract_title(path),
            )
        )
    return sorted(reports, key=lambda report: (-report.report_date.toordinal(), SECTION_ORDER[report.section]))


def render_index(reports: list[Report]) -> str:
    latest = reports[:1]
    items = "\n".join(render_report_item(report) for report in reports)
    latest_summary = (
        f'<p class="summary">最新报告：<a href="{html.escape(latest[0].relative_path)}">'
        f"{html.escape(latest[0].title)}</a></p>"
        if latest
        else '<p class="summary">还没有生成日报。</p>'
    )
    report_list = f'<ul class="reports">\n{items}\n  </ul>' if reports else '<p class="empty">暂无报告。</p>'
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 和股市 News 索引</title>
  <style>
    :root {{ --fg: #182026; --muted: #5a6670; --border: #d8dee4; --bg: #f6f8fa; --link: #0969da; }}
    body {{ color: var(--fg); font-family: system-ui, "PingFang TC", "Noto Sans TC", sans-serif; line-height: 1.6; margin: 0 auto; max-width: 920px; padding: 28px 20px 48px; }}
    h1 {{ border-bottom: 2px solid var(--border); font-size: 1.8rem; margin: 0 0 12px; padding-bottom: 10px; }}
    h2 {{ font-size: 1.2rem; margin-top: 28px; }}
    a {{ color: var(--link); }}
    .summary {{ color: var(--muted); margin: 0 0 24px; }}
    .reports {{ list-style: none; margin: 0; padding: 0; }}
    .report {{ border: 1px solid var(--border); border-radius: 6px; margin: 10px 0; padding: 12px 14px; }}
    .report a {{ font-weight: 650; }}
    .meta {{ color: var(--muted); display: block; font-size: 0.9rem; margin-top: 4px; }}
    .empty {{ background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 14px; }}
  </style>
</head>
<body>
  <h1>AI 和股市 News 索引</h1>
  {latest_summary}
  <h2>全部报告</h2>
  {report_list}
</body>
</html>
"""


def render_report_item(report: Report) -> str:
    return (
        '    <li class="report">'
        f'<a href="{html.escape(report.relative_path)}">{html.escape(report.title)}</a>'
        f'<span class="meta">{html.escape(report.display_date)} · {html.escape(report.section_label)}</span>'
        "</li>"
    )


def copy_reports(root: Path, site_dir: Path, reports: list[Report]) -> None:
    for report in reports:
        source = root / report.relative_path
        destination = site_dir / report.relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_site(root: Path, site_dir: Path) -> None:
    reports = discover_reports(root)
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    copy_reports(root, site_dir, reports)
    (site_dir / "index.html").write_text(render_index(reports), encoding="utf-8")


def write_index(root: Path, output: Path) -> None:
    output.write_text(render_index(discover_reports(root)), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GitHub Pages index for news reports.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--index", type=Path, help="Write index.html to this path.")
    parser.add_argument("--site-dir", type=Path, help="Build a publishable site directory.")
    args = parser.parse_args()

    root = args.root.resolve()
    if args.site_dir:
        build_site(root, args.site_dir.resolve())
    else:
        write_index(root, (args.index or root / "index.html").resolve())


if __name__ == "__main__":
    main()
