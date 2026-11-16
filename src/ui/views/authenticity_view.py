"""
MacTech iTool - Parts & Authenticity Verification View
Audits factory component serial numbers against current installed modules
"""

from typing import Dict, Any
import customtkinter as ctk
from ..theme import THEME

class AuthenticityView(ctk.CTkFrame):
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
            text="🔍 Apple Parts & Factory Calibration Authenticity Auditor",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Detects replaced screens, non-OEM aftermarket batteries, swapped cameras, and board replacements",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Overall Authenticity Score Badge on the right
        self.score_badge = ctk.CTkFrame(top_row, fg_color=THEME["bg_card_alt"], corner_radius=8, border_width=1, border_color=THEME["success"])
        self.score_badge.pack(side="right")

        self.lbl_score = ctk.CTkLabel(
            self.score_badge,
            text="VERIFYING PARTS...",
            font=ctk.CTkFont(family=THEME["font_family"], size=14, weight="bold"),
            text_color=THEME["success"],
            padx=14,
            pady=8
        )
        self.lbl_score.pack()

        # Component Table Container
        self.table_card = ctk.CTkScrollableFrame(self, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.table_card.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def update_data(self, report: Dict[str, Any]):
        for widget in self.table_card.winfo_children():
            widget.destroy()

        if not report or not report.get("checks"):
            ctk.CTkLabel(
                self.table_card,
                text="Awaiting device pairing to query factory hardware calibration tables...",
                font=ctk.CTkFont(family=THEME["font_family"], size=14),
                text_color=THEME["text_muted"]
            ).pack(pady=40)
            return

        is_all_gen = report.get("is_all_genuine", True)
        score_text = report.get("overall_authenticity", "100% Genuine Apple Parts")
        self.lbl_score.configure(
            text=score_text.upper(),
            text_color=THEME["success"] if is_all_gen else THEME["warning"]
        )
        self.score_badge.configure(
            border_color=THEME["success"] if is_all_gen else THEME["warning"]
        )

        # Build component verification cards
        for idx, check in enumerate(report["checks"]):
            card = ctk.CTkFrame(self.table_card, fg_color=THEME["bg_card_alt"], corner_radius=8, border_width=1, border_color=THEME["border"])
            card.pack(fill="x", padx=12, pady=6)

            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", padx=16, pady=(12, 6))

            ctk.CTkLabel(
                header_row,
                text=check["component"],
                font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
                text_color=THEME["apple_cyan"]
            ).pack(side="left")

            # Status pill
            is_orig = check["is_original"]
            pill_color = THEME["success"] if is_orig else THEME["warning"]
            pill = ctk.CTkLabel(
                header_row,
                text=f"● {check['status']}",
                font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
                text_color=pill_color,
                fg_color=THEME["bg_input"],
                corner_radius=6,
                padx=10,
                pady=4
            )
            pill.pack(side="right")

            # Serial comparison row
            ser_row = ctk.CTkFrame(card, fg_color="transparent")
            ser_row.pack(fill="x", padx=16, pady=(0, 8))

            f_box = ctk.CTkFrame(ser_row, fg_color=THEME["bg_main"], corner_radius=6, border_width=1, border_color=THEME["border"])
            f_box.pack(side="left", fill="x", expand=True, padx=(0, 6), pady=2)
            ctk.CTkLabel(f_box, text="Factory Calibration S/N", font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"), text_color=THEME["text_secondary"]).pack(anchor="w", padx=8, pady=(4, 1))
            ctk.CTkLabel(f_box, text=check["factory_sn"], font=ctk.CTkFont(family=THEME["font_mono"], size=12), text_color=THEME["text_main"]).pack(anchor="w", padx=8, pady=(0, 4))

            c_box = ctk.CTkFrame(ser_row, fg_color=THEME["bg_main"], corner_radius=6, border_width=1, border_color=THEME["border"])
            c_box.pack(side="left", fill="x", expand=True, padx=(6, 0), pady=2)
            ctk.CTkLabel(c_box, text="Current Installed Module S/N", font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"), text_color=THEME["text_secondary"]).pack(anchor="w", padx=8, pady=(4, 1))
            ctk.CTkLabel(c_box, text=check["current_sn"], font=ctk.CTkFont(family=THEME["font_mono"], size=12), text_color=THEME["text_main"]).pack(anchor="w", padx=8, pady=(0, 4))

            # Forensic Detail
            detail_row = ctk.CTkLabel(
                card,
                text=f"ℹ️ {check['detail']}",
                font=ctk.CTkFont(family=THEME["font_family"], size=12),
                text_color=THEME["text_secondary"],
                anchor="w"
            )
            detail_row.pack(fill="x", padx=16, pady=(0, 10))
