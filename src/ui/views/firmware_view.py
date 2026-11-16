"""
MacTech iTool - Apple Firmware Revival & IPSW Suite View
"""

import webbrowser
from typing import Dict, Any, List
import customtkinter as ctk
from ..theme import THEME
from ...core.firmware_manager import FirmwareManager

class FirmwareView(ctk.CTkFrame):
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
            text="⚡ Apple Official Firmware (IPSW) & Device Revival Suite",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Restore, flash or update iOS/iPadOS with signing verification, Clean Restore or Retain User Data",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Recovery Controls on Header Right
        rec_box = ctk.CTkFrame(top_row, fg_color="transparent")
        rec_box.pack(side="right")

        ctk.CTkButton(
            rec_box,
            text="⬇️ Enter Recovery",
            fg_color=THEME["warning"],
            hover_color=THEME["warning_hover"],
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            height=32,
            command=self._enter_recovery
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            rec_box,
            text="⬆️ Exit Recovery",
            fg_color=THEME["success"],
            hover_color=THEME["success_hover"],
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            height=32,
            command=self._exit_recovery
        ).pack(side="left", padx=4)

        # Body Frame (2 Columns: Left = IPSW Catalog, Right = Restore Modes & DFU Guide)
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # Left Column: IPSW Catalog Table
        self.ipsw_card = ctk.CTkFrame(body, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.ipsw_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        ctk.CTkLabel(
            self.ipsw_card,
            text="🌐 Official Apple Signed Firmwares (Direct Apple CDN)",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.ipsw_table = ctk.CTkScrollableFrame(self.ipsw_card, fg_color="transparent")
        self.ipsw_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Right Column: Flashing Modes & DFU Instructions
        right_frame = ctk.CTkFrame(body, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        # Flashing Modes Card
        mode_card = ctk.CTkFrame(right_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        mode_card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            mode_card,
            text="🛠️ Firmware Restore Strategy",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.restore_mode_var = ctk.StringVar(value="retain")

        r1 = ctk.CTkRadioButton(
            mode_card,
            text="Retain User Data Flash (Preserve Photos, Apps & Data)",
            variable=self.restore_mode_var,
            value="retain",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["apple_blue"]
        )
        r1.pack(anchor="w", padx=16, pady=(6, 4))

        r2 = ctk.CTkRadioButton(
            mode_card,
            text="Clean Restore / Full Erase (Wipe NAND & Revive Corrupted Boot)",
            variable=self.restore_mode_var,
            value="erase",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["danger"]
        )
        r2.pack(anchor="w", padx=16, pady=(4, 14))

        # DFU Guide Card
        self.dfu_card = ctk.CTkFrame(right_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.dfu_card.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.dfu_card,
            text="📟 Hardware DFU & Recovery Sequence Guide",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.dfu_steps_box = ctk.CTkScrollableFrame(self.dfu_card, fg_color="transparent")
        self.dfu_steps_box.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def update_data(self, firmwares: List[Dict[str, Any]], product_type: str = "iPhone16,2"):
        for w in self.ipsw_table.winfo_children():
            w.destroy()

        if not firmwares:
            ctk.CTkLabel(
                self.ipsw_table,
                text="Awaiting device to query official Apple IPSW signing catalog...",
                font=ctk.CTkFont(family=THEME["font_family"], size=13),
                text_color=THEME["text_muted"]
            ).pack(pady=40)
            return

        for idx, fw in enumerate(firmwares):
            row = ctk.CTkFrame(self.ipsw_table, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=8)
            row.pack(fill="x", pady=4, padx=2)

            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", padx=10, pady=8)

            ctk.CTkLabel(
                left,
                text=f"{fw['version']} ({fw['buildid']})",
                font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"),
                text_color=THEME["text_main"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=f"Size: {fw['filesize_gb']} GB • Released: {fw['release_date']}",
                font=ctk.CTkFont(family=THEME["font_family"], size=11),
                text_color=THEME["text_secondary"]
            ).pack(anchor="w")

            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right", padx=10, pady=8)

            is_signed = fw["signed"]
            s_badge = ctk.CTkLabel(
                right,
                text="✓ SIGNED" if is_signed else "✗ UNSIGNED",
                font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
                text_color=THEME["success"] if is_signed else THEME["danger"],
                fg_color=THEME["bg_main"],
                corner_radius=6,
                padx=8,
                pady=2
            )
            s_badge.pack(side="left", padx=6)

            if is_signed and fw.get("url"):
                ctk.CTkButton(
                    right,
                    text="Download",
                    font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
                    fg_color=THEME["apple_blue"],
                    hover_color=THEME["apple_blue_hover"],
                    width=75,
                    height=28,
                    command=lambda u=fw["url"]: webbrowser.open(u)
                ).pack(side="left")

        # Update DFU steps
        for w in self.dfu_steps_box.winfo_children():
            w.destroy()
        dfu_info = FirmwareManager.get_dfu_instructions(product_type)
        ctk.CTkLabel(
            self.dfu_steps_box,
            text=dfu_info["title"],
            font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w", pady=(2, 6))

        for step in dfu_info["steps"]:
            ctk.CTkLabel(
                self.dfu_steps_box,
                text=step,
                font=ctk.CTkFont(family=THEME["font_family"], size=11),
                text_color=THEME["text_secondary"],
                justify="left",
                wraplength=380
            ).pack(anchor="w", pady=2)

    def _enter_recovery(self):
        self.apple_manager.controller.execute_command("enter_recovery")

    def _exit_recovery(self):
        self.apple_manager.controller.execute_command("exit_recovery")
