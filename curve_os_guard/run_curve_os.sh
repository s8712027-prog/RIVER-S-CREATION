#!/usr/bin/env bash
# Curve OS Guard: local-only launcher for Linux and macOS.
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" curve_os_cli.py --input data/incoming/DEMO-B20260824-001.csv --coil-id DEMO-B20260824-001
echo "啟動本機儀表板：http://127.0.0.1:8765"
exec "$PYTHON_BIN" app.py
