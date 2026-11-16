"""
MacTech iTool - Apple Firmware & Device Revival Suite
IPSW Catalog Integration, Signed iOS Verification & Restoration Engine
"""

import sys
import os
import subprocess
import threading
from typing import Dict, Any, List, Optional
import requests

IPSW_API_BASE = "https://api.ipsw.me/v4"

class FirmwareManager:
    @staticmethod
    def get_firmwares_for_device(product_type: str) -> List[Dict[str, Any]]:
        """
        Queries Apple's official IPSW signing status for a device identifier
        via IPSW.me API. Returns signed and unsigned versions with Apple CDN URLs.
        """
        try:
            url = f"{IPSW_API_BASE}/device/{product_type}?type=ipsw"
            resp = requests.get(url, timeout=6.0)
            if resp.status_code == 200:
                data = resp.json()
                firmwares = data.get("firmwares", [])
                formatted = []
                for fw in firmwares:
                    size_gb = round(fw.get("filesize", 0) / (1024**3), 2)
                    formatted.append({
                        "version": fw.get("version", "iOS"),
                        "buildid": fw.get("buildid", ""),
                        "signed": fw.get("signed", False),
                        "filesize_gb": size_gb,
                        "release_date": fw.get("releasedate", "")[:10] if fw.get("releasedate") else "Unknown",
                        "url": fw.get("url", ""),
                        "filename": fw.get("filename", "")
                    })
                return formatted
        except Exception:
            pass

        # Offline / Fallback Catalog for common devices
        return [
            {"version": "iOS 18.1.1", "buildid": "22B91", "signed": True, "filesize_gb": 7.42, "release_date": "2024-11-19", "url": "https://updates.cdn-apple.com/...", "filename": f"{product_type}_18.1.1_Restore.ipsw"},
            {"version": "iOS 18.1.0", "buildid": "22B83", "signed": True, "filesize_gb": 7.39, "release_date": "2024-10-28", "url": "https://updates.cdn-apple.com/...", "filename": f"{product_type}_18.1_Restore.ipsw"},
            {"version": "iOS 18.0.1", "buildid": "22A3370", "signed": False, "filesize_gb": 7.15, "release_date": "2024-10-03", "url": "https://updates.cdn-apple.com/...", "filename": f"{product_type}_18.0.1_Restore.ipsw"},
            {"version": "iOS 17.7.2", "buildid": "21H221", "signed": True, "filesize_gb": 6.84, "release_date": "2024-11-19", "url": "https://updates.cdn-apple.com/...", "filename": f"{product_type}_17.7.2_Restore.ipsw"},
            {"version": "iOS 17.6.1", "buildid": "21G93", "signed": False, "filesize_gb": 6.78, "release_date": "2024-08-07", "url": "https://updates.cdn-apple.com/...", "filename": f"{product_type}_17.6.1_Restore.ipsw"},
        ]

    @staticmethod
    def get_dfu_instructions(product_type: str) -> Dict[str, Any]:
        """Provides precise hardware key timing for DFU / Recovery mode entry"""
        if any(k in product_type for k in ["iPhone8", "iPhone9", "iPhone10", "iPhone11", "iPhone12", "iPhone13", "iPhone14", "iPhone15", "iPhone16", "iPhone17"]):
            return {
                "title": "Modern iPhone (iPhone 8 through iPhone 16 Pro Max)",
                "steps": [
                    "1. Connect the iPhone to computer via high-speed USB-C or Lightning cable.",
                    "2. Quickly press and release Volume Up.",
                    "3. Quickly press and release Volume Down.",
                    "4. Press and hold the Side (Power) button until screen goes pitch black (approx. 8-10 seconds).",
                    "5. Keep holding Side button and simultaneously press and hold Volume Down for exactly 5 seconds.",
                    "6. Release Side button while continuing to hold Volume Down for another 10 seconds.",
                    "7. Screen must remain completely black. MacTech iTool will detect 'DFU Mode Connected'."
                ]
            }
        elif "iPhone7" in product_type:
            return {
                "title": "iPhone 7 / 7 Plus DFU Procedure",
                "steps": [
                    "1. Connect iPhone to PC.",
                    "2. Press and hold both Power (Side) button and Volume Down button simultaneously for 8-10 seconds.",
                    "3. Release Power button but keep holding Volume Down for another 8-10 seconds.",
                    "4. Screen remains black when in DFU mode."
                ]
            }
        else:
            return {
                "title": "Home Button Devices (iPhone 6s, SE 1st Gen, iPads)",
                "steps": [
                    "1. Connect device to PC.",
                    "2. Press and hold both Home button and Top/Side Power button for 8-10 seconds.",
                    "3. Release Power button, keep holding Home button for another 10 seconds.",
                    "4. Screen remains black when DFU mode is achieved."
                ]
            }
