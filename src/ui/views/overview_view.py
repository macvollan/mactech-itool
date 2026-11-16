"""
MacTech iTool - Device Overview & Hardware Specifications View
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any
import customtkinter as ctk
from ..theme import THEME

class OverviewView(ctk.CTkFrame):
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

        self.lbl_model_title = ctk.CTkLabel(
            title_box,
            text="Apple Device Hardware Forensics",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        )
        self.lbl_model_title.pack(anchor="w")

        self.lbl_subtitle = ctk.CTkLabel(
            title_box,
            text="Awaiting connection or select Sample Preview mode...",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        )
        self.lbl_subtitle.pack(anchor="w", pady=(2, 0))

        # Right buttons in header
        btn_box = ctk.CTkFrame(top_row, fg_color="transparent")
        btn_box.pack(side="right")

        self.btn_copy_udid = ctk.CTkButton(
            btn_box,
            text="📋 Copy UDID",
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            height=32,
            command=self._copy_udid
        )
        self.btn_copy_udid.pack(side="left", padx=4)

        self.btn_copy_sn = ctk.CTkButton(
            btn_box,
            text="🔢 Copy Serial",
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            height=32,
            command=self._copy_sn
        )
        self.btn_copy_sn.pack(side="left", padx=4)

        # Content Grid (2 columns: Left = Spec Cards, Right = Storage & Activation)
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=16, pady=4)
        grid_frame.grid_columnconfigure(0, weight=3)
        grid_frame.grid_columnconfigure(1, weight=2)
        grid_frame.grid_rowconfigure(0, weight=1)

        # Left Column: Detailed Hardware Specs
        self.spec_card = ctk.CTkFrame(grid_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.spec_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        card_title = ctk.CTkLabel(
            self.spec_card,
            text="📱 Low-Level Hardware Identifiers",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        )
        card_title.pack(anchor="w", padx=18, pady=(16, 12))

        self.spec_table = ctk.CTkScrollableFrame(self.spec_card, fg_color="transparent")
        self.spec_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Right Column: Storage & Telecom / Security
        right_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        # Storage Card
        self.storage_card = ctk.CTkFrame(right_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.storage_card.pack(fill="x", pady=(0, 10))

        st_title = ctk.CTkLabel(
            self.storage_card,
            text="💾 NAND Flash Solid-State Storage",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        )
        st_title.pack(anchor="w", padx=16, pady=(14, 8))

        self.lbl_storage_stats = ctk.CTkLabel(
            self.storage_card,
            text="Used: -- GB / Total: -- GB",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_main"]
        )
        self.lbl_storage_stats.pack(anchor="w", padx=16, pady=(0, 6))

        self.storage_progress = ctk.CTkProgressBar(self.storage_card, progress_color=THEME["apple_blue"], fg_color=THEME["border"], height=12)
        self.storage_progress.pack(fill="x", padx=16, pady=(0, 14))
        self.storage_progress.set(0.0)

        # Status & Regulatory Card
        self.status_card = ctk.CTkFrame(right_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.status_card.pack(fill="both", expand=True)

        sc_title = ctk.CTkLabel(
            self.status_card,
            text="🔒 Activation & Network Status",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        )
        sc_title.pack(anchor="w", padx=16, pady=(14, 8))

        self.status_table = ctk.CTkFrame(self.status_card, fg_color="transparent")
        self.status_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def update_data(self, data: Dict[str, Any]):
        if not data or data.get("status") == "DISCONNECTED":
            self.lbl_model_title.configure(text="No Apple Device Connected")
            self.lbl_subtitle.configure(text="Connect device via Lightning or USB-C cable and unlock screen to pair.")
            self._clear_tables()
            return

        model = data.get("model_name", "Apple Device")
        p_type = data.get("product_type", "")
        self.lbl_model_title.configure(text=f"{model} ({p_type})")
        self.lbl_subtitle.configure(text=f"iOS / iPadOS {data.get('ios_version', '')} • SoC: {data.get('soc', '')}")

        # Update spec table
        self._clear_tables()
        specs = [
            ("Model Marketing Name", model),
            ("Apple ProductType", p_type),
            ("Hardware Board ID", data.get("raw", {}).get("HardwareModel", "N/A")),
            ("Serial Number", data.get("serial_number", "N/A")),
            ("Unique Device ID (UDID)", data.get("udid", "N/A")),
            ("Model Number", data.get("raw", {}).get("ModelNumber", "N/A")),
            ("Region / Country", data.get("region", "N/A")),
            ("Processor / SoC", data.get("soc", "N/A")),
            ("RAM Architecture", data.get("ram", "N/A")),
            ("Baseband Modem Firmware", data.get("raw", {}).get("BasebandVersion", "N/A")),
            ("Wi-Fi MAC Address", data.get("raw", {}).get("WiFiAddress", "N/A")),
            ("Bluetooth MAC Address", data.get("raw", {}).get("BluetoothAddress", "N/A")),
        ]

        for idx, (lbl, val) in enumerate(specs):
            row = ctk.CTkFrame(self.spec_table, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=6)
            row.pack(fill="x", pady=2, padx=4)
            ctk.CTkLabel(row, text=lbl, font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=THEME["text_secondary"], width=170, anchor="w").pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont(family=THEME["font_mono"], size=12), text_color=THEME["text_main"], anchor="w").pack(side="left", fill="x", expand=True, padx=8, pady=4)

        # Update Storage
        total_gb = data.get("storage_total_gb", 0)
        free_gb = data.get("storage_free_gb", 0)
        used_gb = max(0, total_gb - free_gb)
        pct = (used_gb / total_gb) if total_gb > 0 else 0
        self.lbl_storage_stats.configure(text=f"Used: {used_gb} GB / Total: {total_gb} GB ({free_gb} GB Free)")
        self.storage_progress.set(pct)

        # Update Status & Security
        statuses = [
            ("Activation State", data.get("activation_state", "Unknown")),
            ("Carrier / SIM Lock", data.get("carrier", "Unknown")),
            ("SIM Hardware Slot", data.get("raw", {}).get("SIMStatus", "Ready")),
            ("Connection Protocol", "Apple usbmuxd (TCP Port 27015 / Socket)"),
            ("Diagnostics Relay", "Available & Authorized"),
        ]
        for idx, (lbl, val) in enumerate(statuses):
            row = ctk.CTkFrame(self.status_table, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=6)
            row.pack(fill="x", pady=2, padx=4)
            ctk.CTkLabel(row, text=lbl, font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=THEME["text_secondary"], width=140, anchor="w").pack(side="left", padx=8, pady=4)
            color = THEME["success"] if "Activated" in str(val) or "Unlocked" in str(val) or "Ready" in str(val) or "Authorized" in str(val) else THEME["text_main"]
            ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=color, anchor="w").pack(side="left", fill="x", expand=True, padx=8, pady=4)

    def _clear_tables(self):
        for widget in self.spec_table.winfo_children():
            widget.destroy()
        for widget in self.status_table.winfo_children():
            widget.destroy()

    def _copy_udid(self):
        udid = self.apple_manager.cached_overview.get("udid", "")
        if udid:
            self.clipboard_clear()
            self.clipboard_append(udid)
            messagebox.showinfo("Clipboard", f"Copied UDID:\n{udid}")

    def _copy_sn(self):
        sn = self.apple_manager.cached_overview.get("serial_number", "")
        if sn:
            self.clipboard_clear()
            self.clipboard_append(sn)
            messagebox.showinfo("Clipboard", f"Copied Serial Number:\n{sn}")
