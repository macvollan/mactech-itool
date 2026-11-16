#!/usr/bin/env bash
# ==============================================================================
# MacTech iTool - macOS Double-Click Launcher
# MacTech Solutions Lab
# ==============================================================================

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if [ -d "MacTech iTool.app" ]; then
    open "MacTech iTool.app"
    exit 0
fi

python3 main.py "$@"
