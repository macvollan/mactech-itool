#!/usr/bin/env bash
# ==============================================================================
# MacTech iTool - macOS Environment & Tool Setup
# MacTech Solutions Lab - https://mactechsolutionslab.vercel.app
# Compatible with Apple Silicon (M1/M2/M3/M4) & Intel
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  MacTech iTool - macOS Environment Installer"
echo "  MacTech Solutions Lab"
echo "============================================================"
echo ""

# 1. Check Homebrew
if command -v brew &>/dev/null; then
    echo "[*] Homebrew detected. Installing Apple diagnostic tools..."
    brew install libimobiledevice idevicerestore ideviceinstaller || true
else
    echo "[!] Homebrew not found. macOS built-in lockdown will be used natively."
fi

# 2. Python Packages
echo ""
echo "[*] Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt || python3 -m pip install --break-system-packages -r requirements.txt

echo ""
echo "============================================================"
echo "  macOS Setup Complete! Launch with ./launch_mac.command"
echo "============================================================"
