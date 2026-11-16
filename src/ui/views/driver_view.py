"""
MacTech iTool - Universal Driver & Dependency Doctor View
"""

import sys
import os
import webbrowser
from typing import Dict, Any
import customtkinter as ctk
from ..theme import THEME
from ...core.driver_manager import DriverManager

class DriverView(ctk.CTkFrame):
    def __init__(self, master, apple_manager):
        super().__init__(master, fg_color="transparent")
        self.apple_manager = apple_manager
        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = ctk.CTkFrame(self, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        header.pack(fill="x", padx=16, pady=(16, 12))

        top_row = ctk.CTkFrame(header, fg_color="transparent")
        top_row.pack(fill="x", padx=20, pady=16)

        title_box = ctk.CTkFrame(top_row, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="🛠️ Universal Driver, Daemon & Dependency Doctor",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Audits Apple Mobile Device Support (AMDS), usbmuxd sockets, Apple USB kernel drivers and udev permissions",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Re-check button
        ctk.CTkButton(
            top_row,
            text="🔄 Re-Scan Drivers",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["apple_blue"],
            hover_color=THEME["apple_blue_hover"],
            height=32,
            command=self.refresh_status
        ).pack(side="right")

        # Body Container (2 Columns: Left = Component Table, Right = 1-Click Fix Instructions)
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # Left Column: Driver Component Audit Table
        self.comp_card = ctk.CTkFrame(body, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.comp_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        ctk.CTkLabel(
            self.comp_card,
            text="📋 Host Operating System Driver Status",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.comp_table = ctk.CTkScrollableFrame(self.comp_card, fg_color="transparent")
        self.comp_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Right Column: Setup & Fix Guide
        fix_card = ctk.CTkFrame(body, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        fix_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        ctk.CTkLabel(
            fix_card,
            text="🚀 1-Click Driver Installation & Setup",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["success"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.fix_scroll = ctk.CTkScrollableFrame(fix_card, fg_color="transparent")
        self.fix_scroll.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.refresh_status()

    def refresh_status(self):
        status = DriverManager.inspect_system()

        for w in self.comp_table.winfo_children():
            w.destroy()

        for idx, comp in enumerate(status.get("components", [])):
            row = ctk.CTkFrame(self.comp_table, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=8)
            row.pack(fill="x", pady=4, padx=2)

            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", padx=10, pady=8)

            ctk.CTkLabel(
                left,
                text=comp["name"],
                font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"),
                text_color=THEME["text_main"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=comp["importance"],
                font=ctk.CTkFont(family=THEME["font_family"], size=11),
                text_color=THEME["text_secondary"]
            ).pack(anchor="w")

            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right", padx=10, pady=8)

            is_inst = comp["installed"]
            status_badge = ctk.CTkLabel(
                right,
                text="✓ INSTALLED & READY" if is_inst else "✗ MISSING DRIVER",
                font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
                text_color=THEME["success"] if is_inst else THEME["danger"],
                fg_color=THEME["bg_main"],
                corner_radius=6,
                padx=8,
                pady=4
            )
            status_badge.pack(side="right")

        # Right column: Automated Setup Guidance
        for w in self.fix_scroll.winfo_children():
            w.destroy()

        plat = status["platform"]
        if plat == "win32":
            guide_text = (
                "Windows 10/11 Automated Driver Deployment:\n\n"
                "1. Run 'setup_windows.bat' in the tool root folder.\n"
                "2. It automatically installs the official 64-bit Apple Mobile Device Support (AMDS) and Apple Application Support drivers.\n"
                "3. Connect your iPhone/iPad/Apple Watch and click 'Trust This Computer' on the screen.\n"
                "4. All diagnostic and lockdown services will immediately synchronize."
            )
        elif plat == "darwin":
            guide_text = (
                "macOS Setup (Apple Silicon M1/M2/M3/M4 & Intel):\n\n"
                "1. macOS includes native Apple usbmuxd and lockdown system daemons.\n"
                "2. For extended CLI forensics, run 'brew install libimobiledevice idevicerestore'.\n"
                "3. Double-click 'launch_mac.command' to launch."
            )
        else:
            guide_text = (
                "Linux (Ubuntu / Debian / Arch / Fedora):\n\n"
                "1. Run 'sudo ./setup_linux.sh' to install usbmuxd, libimobiledevice6, and configure 51-apple-device.rules.\n"
                "2. System will enable non-root USB access for Apple devices (VID 0x05ac).\n"
                "3. Run './launch_linux.sh'."
            )

        ctk.CTkLabel(
            self.fix_scroll,
            text=guide_text,
            font=ctk.CTkFont(family=THEME["font_family"], size=12),
            text_color=THEME["text_secondary"],
            justify="left",
            wraplength=380
        ).pack(anchor="w", padx=6, pady=6)

        ctk.CTkButton(
            self.fix_scroll,
            text="🌐 Download Official Apple Drivers CDN",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["apple_blue"],
            hover_color=THEME["apple_blue_hover"],
            height=34,
            command=lambda: webbrowser.open("https://secure-appldnld.apple.com/itunes12/001-44813-20200520-3B1D46CE-9AB2-11EA-9B7C-A8E9A348B47E/iTunes64Setup.exe")
        ).pack(fill="x", padx=6, pady=10)
