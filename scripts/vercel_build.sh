#!/usr/bin/env bash
# Vercel production build — always use venv Python with Pillow + fpdf2.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"

if [[ ! -x "$PY" ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -q fpdf2 pillow
fi

"$PY" scripts/build_site.py
"$PY" scripts/generate_media_kit_pdf.py

echo "vercel build ok"
