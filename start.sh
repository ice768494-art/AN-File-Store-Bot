#!/usr/bin/env bash
set -euo pipefail
python -m pip install --no-cache-dir -r requirements.txt
exec python3 main.py
