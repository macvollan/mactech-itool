# 🐧 MacTech iTool - Linux Setup Guide
**MacTech Solutions Lab** • Ubuntu, Debian, Arch, Fedora, openSUSE

### Automatic Setup
Run the automated installer to set up `usbmuxd`, Python dependencies, and non-root udev rules:
```bash
chmod +x setup_linux.sh launch_linux.sh
sudo ./setup_linux.sh
```

### Launching the Tool
```bash
./launch_linux.sh
```

### Udev Rules Note
The installer automatically creates `/etc/udev/rules.d/51-apple-device.rules` with:
```udev
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", MODE="0666", GROUP="plugdev"
```
Ensure your user account is in the `plugdev` group:
```bash
sudo usermod -aG plugdev $USER
```
