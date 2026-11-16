#!/usr/bin/env bash
# ==============================================================================
# MacTech iTool - Linux One-Click Launcher
# MacTech Solutions Lab
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || realpath "$0" 2>/dev/null || echo "$0")")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "dist/MacTech_iTool" ]; then
    ./dist/MacTech_iTool "$@"
    exit 0
fi

python3 main.py "$@"
