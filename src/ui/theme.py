"""
MacTech iTool - Theme & Styling Configuration
Cupertino Titanium Forensic Palette for Apple Devices
"""
import sys

def sys_is_windows():
    return sys.platform == "win32"

THEME = {
    "bg_main": "#0B0E14",
    "bg_sidebar": "#0E131F",
    "bg_card": "#131A29",
    "bg_card_alt": "#172235",
    "bg_input": "#0F1626",
    "border": "#1E2B42",
    "border_highlight": "#0071E3",

    # Apple Signature Accents
    "apple_blue": "#0071E3",
    "apple_blue_hover": "#0077ED",
    "apple_cyan": "#00C7BE",
    "apple_cyan_hover": "#05B2AA",
    "apple_indigo": "#5856D6",
    "apple_indigo_hover": "#4B48C8",
    "apple_purple": "#AF52DE",

    # Status & Telemetry
    "success": "#30D158",
    "success_hover": "#28B84D",
    "warning": "#FF9F0A",
    "warning_hover": "#E58F08",
    "danger": "#FF453A",
    "danger_hover": "#E53D32",
    "battery_green": "#34C759",

    # Typography & Grayscale
    "text_main": "#F5F5F7",
    "text_secondary": "#A1A1A6",
    "text_muted": "#6E6E73",
    "text_dark": "#0B0E14",

    "font_family": "Segoe UI" if sys_is_windows() else "SF Pro Display",
    "font_mono": "Consolas" if sys_is_windows() else "SF Mono"
}

