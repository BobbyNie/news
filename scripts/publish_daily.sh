#!/usr/bin/env bash
# Publish daily reports: rebuild index, commit, push main (triggers GitHub Pages).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

eval "$(python3 scripts/report_date.py)"

python3 -m unittest discover -s tests -p 'test_*.py' -q
python3 scripts/validate_report_ui.py --kind AI --date "$REPORT_DATE"
python3 scripts/validate_report_ui.py --kind STOCK --date "$REPORT_DATE"
python3 scripts/build_pages_index.py

git add \
  "tmp/AI/${REPORT_DATE}/" \
  "tmp/STOCK/${REPORT_DATE}/" \
  "${REPORT_MONTH}/AI/${REPORT_DATE}.html" \
  "${REPORT_MONTH}/STOCK/${REPORT_DATE}.html" \
  index.html \
  scripts/report_date.py \
  scripts/validate_report_ui.py \
  tests/test_report_date.py \
  tests/test_validate_report_ui.py \
  prompts/ \
  README.MD 2>/dev/null || true

if git diff --cached --quiet; then
  echo "No staged changes to publish."
  exit 0
fi

git commit -m "daily news reports ${REPORT_ISO}"
git push origin main

echo "Pushed to main. GitHub Pages workflow should deploy ${REPORT_ISO} reports."
