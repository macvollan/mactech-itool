#!/usr/bin/env bash
# ==============================================================================
# MacTech iTool - Linux One-Step Environment & Apple Udev Setup
# MacTech Solutions Lab - https://mactechsolutionslab.vercel.app
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || realpath "$0" 2>/dev/null || echo "$0")")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  MacTech iTool - Linux Environment & Driver Installer"
echo "  MacTech Solutions Lab"
echo "============================================================"
echo ""

# 1. Package Manager Detection & System Dependencies
if command -v apt-get &>/dev/null; then
    echo "[*] Detected Debian / Ubuntu / Mint / Pop!_OS"
    echo "[*] Installing required packages (Python3, Tk, usbmuxd, libimobiledevice)..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-tk usbmuxd libimobiledevice6 libimobiledevice-utils ideviceinstaller
elif command -v dnf &>/dev/null; then
    echo "[*] Detected Fedora / RHEL / CentOS"
    echo "[*] Installing required packages..."
    sudo dnf install -y python3 python3-pip python3-tkinter usbmuxd libimobiledevice libimobiledevice-utils
elif command -v pacman &>/dev/null; then
    echo "[*] Detected Arch Linux / Manjaro / EndeavourOS"
    echo "[*] Installing required packages..."
    sudo pacman -Sy --noconfirm python python-pip tk usbmuxd libimobiledevice
elif command -v zypper &>/dev/null; then
    echo "[*] Detected openSUSE"
    sudo zypper install -y python3 python3-pip python3-tk usbmuxd libimobiledevice-tools
else
    echo "[!] Unrecognized package manager. Please ensure python3, tk, and usbmuxd are installed manually."
fi

# 2. Python Dependencies
echo ""
echo "[*] Installing Python dependencies (CustomTkinter, Pillow, Requests)..."
python3 -m pip install --user -r requirements.txt || python3 -m pip install --user --break-system-packages -r requirements.txt

# 3. Apple Device USB Udev Rules (VID 0x05ac)
echo ""
echo "[*] Configuring Apple USB udev rules for non-root hardware access..."
UDEV_RULE_FILE="/etc/udev/rules.d/51-apple-device.rules"
if [ ! -f "$UDEV_RULE_FILE" ]; then
    echo '[*] Creating /etc/udev/rules.d/51-apple-device.rules...'
    sudo tee "$UDEV_RULE_FILE" > /dev/null << 'EOF'
# MacTech iTool - Apple Device udev rules
# Normal, Recovery, DFU & Apple Watch Mode
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", MODE="0666", GROUP="plugdev"
EOF
    sudo udevadm control --reload-rules || true
    sudo udevadm trigger || true
    echo "[OK] Udev rules configured successfully."
else
    echo "[OK] Apple udev rules already present at $UDEV_RULE_FILE."
fi

# 4. Start & Enable usbmuxd Service
echo ""
echo "[*] Starting and enabling usbmuxd daemon..."
if command -v systemctl &>/dev/null; then
    sudo systemctl restart usbmuxd || true
    sudo systemctl enable usbmuxd || true
fi

echo ""
echo "============================================================"
echo "  Linux Setup Complete! Launch with ./launch_linux.sh"
echo "============================================================"
