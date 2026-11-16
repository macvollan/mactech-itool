"""
MacTech iTool - Automated Panic Log & Hardware Fault Diagnostician View
"""

from typing import Dict, Any
import customtkinter as ctk
from ..theme import THEME
from ...core.panic_analyzer import PanicAnalyzer

class DiagnosticView(ctk.CTkFrame):
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
            text="🩺 Apple AI Kernel Panic & Hardware Fault Diagnostician",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Parses panic-full logs to diagnose 3-minute reboot loops, NAND fatigue, thermal trips, and audio/baseband crashes",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Quick test pills
        pills_box = ctk.CTkFrame(top_row, fg_color="transparent")
        pills_box.pack(side="right")

        ctk.CTkButton(
            pills_box,
            text="⚡ Test Mic2 Fault",
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            height=30,
            command=lambda: self._test_fault("mic2")
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            pills_box,
            text="💾 Test NAND Panic",
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            height=30,
            command=lambda: self._test_fault("nand")
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            pills_box,
            text="🔋 Test Battery WDT",
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            height=30,
            command=lambda: self._test_fault("battery")
        ).pack(side="left", padx=3)

        # Body container: 2 columns
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_columnconfigure(1, weight=1)
        body_frame.grid_rowconfigure(0, weight=1)

        # Left Column: Identified Fault & Step-by-Step Solutions
        self.sol_card = ctk.CTkFrame(body_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.sol_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        ctk.CTkLabel(
            self.sol_card,
            text="🔧 Root Cause & Technician Repair Protocol",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.sol_content = ctk.CTkScrollableFrame(self.sol_card, fg_color="transparent")
        self.sol_content.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Right Column: Raw Log Inspector
        self.log_card = ctk.CTkFrame(body_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.log_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        ctk.CTkLabel(
            self.log_card,
            text="📜 Panic-Full.ips Telemetry Stream",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.txt_log = ctk.CTkTextbox(
            self.log_card,
            fg_color=THEME["bg_input"],
            text_color=THEME["text_main"],
            font=ctk.CTkFont(family=THEME["font_mono"], size=11),
            corner_radius=8,
            border_width=1,
            border_color=THEME["border"]
        )
        self.txt_log.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def update_data(self, report: Dict[str, Any]):
        if not report or not report.get("has_panic"):
            self._render_empty()
            return
        self._render_report(report)

    def _render_report(self, report: Dict[str, Any]):
        for w in self.sol_content.winfo_children():
            w.destroy()

        fault = report.get("primary_fault", {})
        severity = fault.get("severity", "MEDIUM")
        sev_color = THEME["danger"] if severity == "CRITICAL" else (THEME["warning"] if severity == "HIGH" else THEME["apple_cyan"])

        # Fault Title & Severity Banner
        banner = ctk.CTkFrame(self.sol_content, fg_color=THEME["bg_card_alt"], corner_radius=8, border_width=1, border_color=sev_color)
        banner.pack(fill="x", pady=(0, 10))

        b_top = ctk.CTkFrame(banner, fg_color="transparent")
        b_top.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            b_top,
            text=f"⚠️ {fault.get('fault_name', 'Kernel Panic')}",
            font=ctk.CTkFont(family=THEME["font_family"], size=14, weight="bold"),
            text_color=THEME["text_main"],
            wraplength=400,
            justify="left"
        ).pack(side="left")

        ctk.CTkLabel(
            b_top,
            text=severity,
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            text_color=sev_color,
            fg_color=THEME["bg_main"],
            corner_radius=6,
            padx=8,
            pady=2
        ).pack(side="right")

        ctk.CTkLabel(
            banner,
            text=f"Target Hardware Module: {fault.get('component', 'Unknown')}",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=12, pady=(0, 4))

        ctk.CTkLabel(
            banner,
            text=fault.get("explanation", ""),
            font=ctk.CTkFont(family=THEME["font_family"], size=11),
            text_color=THEME["text_secondary"],
            justify="left",
            wraplength=420
        ).pack(anchor="w", padx=12, pady=(0, 10))

        # Actionable Solutions Steps
        ctk.CTkLabel(
            self.sol_content,
            text="📋 Step-by-Step Hardware Repair Procedure:",
            font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w", pady=(4, 6))

        for step in fault.get("solution", []):
            s_box = ctk.CTkFrame(self.sol_content, fg_color=THEME["bg_card_alt"], corner_radius=6)
            s_box.pack(fill="x", pady=3)
            ctk.CTkLabel(
                s_box,
                text=step,
                font=ctk.CTkFont(family=THEME["font_family"], size=11),
                text_color=THEME["text_main"],
                justify="left",
                wraplength=420
            ).pack(anchor="w", padx=10, pady=6)

    def _render_empty(self):
        for w in self.sol_content.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self.sol_content,
            text="No kernel panics logged or click a quick test button above to simulate.",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_muted"]
        ).pack(pady=40)
        self.txt_log.delete("1.0", "end")
        self.txt_log.insert("1.0", "// No crash log loaded.")

    def _test_fault(self, fault_key: str):
        sample = PanicAnalyzer.get_sample_panic_log(fault_key)
        report = PanicAnalyzer.analyze_panic_log(sample)
        self.txt_log.delete("1.0", "end")
        self.txt_log.insert("1.0", sample)
        self._render_report(report)
