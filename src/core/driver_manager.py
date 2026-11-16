"""
MacTech iTool - Universal Apple Driver & Dependency Manager
Automated Driver Inspector & 1-Click Installer for Windows, macOS & Linux
"""

import sys
import os
import subprocess
import shutil
from typing import Dict, Any, List

class DriverManager:
    @staticmethod
    def inspect_system() -> Dict[str, Any]:
        """
        Inspects the host OS to detect Apple communication drivers and daemons
        """
        platform = sys.platform
        status = {
            "platform": platform,
            "ready": False,
            "drivers_installed": False,
            "usbmuxd_running": False,
            "missing_components": [],
            "components": []
        }

        if platform == "win32":
            # 1. Check Apple Mobile Device Service
            amds_running = False
            try:
                res = subprocess.run(["sc", "query", "Apple Mobile Device Service"], capture_output=True, text=True)
                if "RUNNING" in res.stdout:
                    amds_running = True
            except Exception:
                pass

            # 2. Check registry / file paths for Apple drivers
            amds_installed = os.path.exists(r"C:\Program Files\Common Files\Apple\Mobile Device Support\AppleMobileDeviceService.exe") or \
                             os.path.exists(r"C:\Program Files (x86)\Common Files\Apple\Mobile Device Support\AppleMobileDeviceService.exe")

            status["components"].append({
                "name": "Apple Mobile Device Support (AMDS)",
                "installed": amds_installed,
                "running": amds_running,
                "importance": "Mandatory for iOS USB Communication"
            })

            # 3. Check Apple Application Support
            aas_installed = os.path.exists(r"C:\Program Files\Common Files\Apple\Apple Application Support") or \
                            os.path.exists(r"C:\Program Files (x86)\Common Files\Apple\Apple Application Support")
            status["components"].append({
                "name": "Apple Application Support (AAS 64-bit)",
                "installed": aas_installed,
                "running": True if aas_installed else False,
                "importance": "Core CoreFoundation & Plist Runtime"
            })

            # 4. Check Apple USB Driver (usbaapl64.sys)
            usb_driver = os.path.exists(r"C:\Windows\System32\drivers\usbaapl64.sys") or \
                         os.path.exists(r"C:\Windows\System32\DriverStore\FileRepository\usbaapl64.inf_amd64")
            status["components"].append({
                "name": "Apple USB Driver (usbaapl64.sys)",
                "installed": usb_driver,
                "running": True if usb_driver else False,
                "importance": "Low-level Lightning & USB-C DFU/Recovery Controller"
            })

            # 5. Check libimobiledevice CLI binaries in PATH or local bin
            local_bin = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "bin", "win32")
            has_tools = shutil.which("ideviceinfo") is not None or os.path.exists(os.path.join(local_bin, "ideviceinfo.exe"))
            status["components"].append({
                "name": "MacTech Apple Forensic Toolkit (ideviceinfo / idevicerestore)",
                "installed": has_tools,
                "running": True if has_tools else False,
                "importance": "Diagnostic queries & firmware restore operations"
            })

            if not amds_installed:
                status["missing_components"].append("Apple Mobile Device Support 64-bit")
            if not aas_installed:
                status["missing_components"].append("Apple Application Support")

            status["drivers_installed"] = amds_installed and aas_installed
            status["usbmuxd_running"] = amds_running
            status["ready"] = status["drivers_installed"]

        elif platform == "darwin": # macOS
            # macOS has native usbmuxd and lockdown
            has_brew_tools = shutil.which("ideviceinfo") is not None
            status["components"].append({
                "name": "Apple Native Lockdown Framework",
                "installed": True,
                "running": True,
                "importance": "Built-in macOS system service"
            })
            status["components"].append({
                "name": "libimobiledevice & idevicerestore CLI Tools",
                "installed": has_brew_tools,
                "running": has_brew_tools,
                "importance": "Extended diagnostic interrogation via Homebrew"
            })
            status["ready"] = True
            status["drivers_installed"] = True
            status["usbmuxd_running"] = True

        else: # Linux
            has_usbmuxd = shutil.which("usbmuxd") is not None
            has_tools = shutil.which("ideviceinfo") is not None
            has_udev = os.path.exists("/etc/udev/rules.d/51-apple-device.rules")

            status["components"].append({
                "name": "usbmuxd daemon",
                "installed": has_usbmuxd,
                "running": has_usbmuxd,
                "importance": "Linux USB multiplexor for Apple hardware"
            })
            status["components"].append({
                "name": "libimobiledevice-utils",
                "installed": has_tools,
                "running": has_tools,
                "importance": "Diagnostic queries and restore tools"
            })
            status["components"].append({
                "name": "Apple USB udev rules (51-apple-device.rules)",
                "installed": has_udev,
                "running": has_udev,
                "importance": "Allows non-root USB access to Apple devices"
            })

            if not has_usbmuxd:
                status["missing_components"].append("usbmuxd")
            if not has_tools:
                status["missing_components"].append("libimobiledevice-utils")

            status["ready"] = has_usbmuxd
            status["drivers_installed"] = has_usbmuxd
            status["usbmuxd_running"] = has_usbmuxd

        return status

    @staticmethod
    def get_linux_udev_rules() -> str:
        """Returns standard udev rules for Apple devices (VID 0x05ac)"""
        return (
            "# MacTech iTool - Apple Device udev rules\n"
            "# Normal, Recovery, DFU & Apple Watch Mode\n"
            'SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", MODE="0666", GROUP="plugdev"\n'
        )

    @staticmethod
    def get_windows_install_guide() -> str:
        return (
            "MacTech iTool Windows Driver Setup:\n"
            "1. Download iTunes 64-bit or the standalone Apple Mobile Device Support (AMDS) package.\n"
            "2. Extract using 7-Zip or run 'setup_windows.bat' located in the tool directory.\n"
            "3. The script automatically installs AppleMobileDeviceSupport64.msi and starts the service.\n"
        )
