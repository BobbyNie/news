#!/usr/bin/env bash
# Publish daily reports to main (local/manual wrapper).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/publish_to_main.sh" "$@"
