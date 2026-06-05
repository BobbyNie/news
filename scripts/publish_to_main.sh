#!/usr/bin/env bash
# Publish daily reports to main (triggers GitHub Pages).
# Safe for Cursor Automation on cursor/* feature branches: merges into main then pushes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TRIGGERED_AT="${1:-${TRIGGERED_AT:-}}"
if [[ -n "$TRIGGERED_AT" ]]; then
  eval "$(python3 scripts/report_date.py "$TRIGGERED_AT")"
else
  eval "$(python3 scripts/report_date.py)"
fi

run_gates() {
  python3 -m unittest discover -s tests -p 'test_*.py' -q
  python3 scripts/validate_report_ui.py --kind AI --date "$REPORT_DATE"
  python3 scripts/validate_report_ui.py --kind STOCK --date "$REPORT_DATE"
  python3 scripts/build_pages_index.py
}

stage_reports() {
  git add \
    "tmp/AI/${REPORT_DATE}/" \
    "tmp/STOCK/${REPORT_DATE}/" \
    "${REPORT_MONTH}/AI/${REPORT_DATE}.html" \
    "${REPORT_MONTH}/STOCK/${REPORT_DATE}.html" \
    index.html 2>/dev/null || true
}

ensure_reports_exist() {
  local missing=0
  for f in \
    "${REPORT_MONTH}/AI/${REPORT_DATE}.html" \
    "${REPORT_MONTH}/STOCK/${REPORT_DATE}.html"; do
    if [[ ! -f "$f" ]]; then
      echo "Missing report: $f" >&2
      missing=1
    fi
  done
  if [[ "$missing" -ne 0 ]]; then
    exit 1
  fi
}

commit_pending_on_branch() {
  stage_reports
  if ! git diff --cached --quiet; then
    git commit -m "daily news reports ${REPORT_ISO}"
  fi
}

merge_branch_into_main() {
  local source_ref="$1"
  local source_label="$2"

  git fetch origin main
  git checkout main
  git pull origin main

  if git merge "$source_ref" -m "merge: daily reports ${REPORT_ISO} from ${source_label}"; then
    return 0
  fi

  echo "Merge conflict; cherry-picking commits from ${source_label}..." >&2
  git merge --abort 2>/dev/null || true

  local sha
  for sha in $(git rev-list --reverse origin/main.."$source_ref"); do
    git cherry-pick "$sha" || {
      git cherry-pick --abort
      echo "Cherry-pick failed at ${sha}. Resolve manually." >&2
      exit 1
    }
  done
}

rebuild_index_if_needed() {
  python3 scripts/build_pages_index.py
  git add index.html
  if ! git diff --cached --quiet; then
    git commit -m "chore: rebuild index after merge ${REPORT_ISO}"
  fi
}

run_gates
ensure_reports_exist

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
SOURCE_REF="$(git rev-parse HEAD)"

commit_pending_on_branch
SOURCE_REF="$(git rev-parse HEAD)"

if [[ "$CURRENT_BRANCH" == "main" ]]; then
  git push origin main
  echo "Pushed main (${REPORT_ISO}). GitHub Pages deploy triggered."
  exit 0
fi

merge_branch_into_main "$SOURCE_REF" "$CURRENT_BRANCH"
run_gates
rebuild_index_if_needed
git push origin main
echo "Merged ${CURRENT_BRANCH} -> main (${REPORT_ISO}). GitHub Pages deploy triggered."

git checkout "$CURRENT_BRANCH" 2>/dev/null || true
