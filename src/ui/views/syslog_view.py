"""
MacTech iTool - Real-Time Live Apple Syslog Terminal View
"""

import customtkinter as ctk
from ..theme import THEME
from ...core.syslog_engine import SyslogEngine

class SyslogView(ctk.CTkFrame):
    def __init__(self, master, apple_manager):
        super().__init__(master, fg_color="transparent")
        self.apple_manager = apple_manager
        self.syslog_engine = SyslogEngine(on_log_line=self._on_log_line)
        self.current_filter = "ALL"
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
            text="💻 Real-Time Apple Syslog & Kernel Console",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Live low-latency stream of system events, Darwin kernel notifications, and daemon errors",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Controls on Header Right
        btn_box = ctk.CTkFrame(top_row, fg_color="transparent")
        btn_box.pack(side="right")

        self.btn_toggle = ctk.CTkButton(
            btn_box,
            text="▶ Start Stream",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["success"],
            hover_color=THEME["success_hover"],
            height=32,
            command=self._toggle_stream
        )
        self.btn_toggle.pack(side="left", padx=4)

        ctk.CTkButton(
            btn_box,
            text="🧹 Clear",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            height=32,
            command=self._clear_logs
        ).pack(side="left", padx=4)

        # Filter Pills Row
        filter_row = ctk.CTkFrame(self, fg_color=THEME["bg_card"], corner_radius=10, border_width=1, border_color=THEME["border"])
        filter_row.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(filter_row, text="Filter Stream:", font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=THEME["text_secondary"]).pack(side="left", padx=14, pady=8)

        for f_name in ["ALL", "ERRORS", "KERNEL", "THERMAL", "BATTERY"]:
            ctk.CTkButton(
                filter_row,
                text=f_name,
                font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
                fg_color=THEME["apple_blue"] if f_name == "ALL" else THEME["bg_input"],
                hover_color=THEME["border_highlight"],
                height=26,
                width=65,
                command=lambda name=f_name: self._set_filter(name)
            ).pack(side="left", padx=3, pady=6)

        # Terminal Output Box
        self.terminal = ctk.CTkTextbox(
            self,
            fg_color=THEME["bg_main"],
            text_color=THEME["text_main"],
            font=ctk.CTkFont(family=THEME["font_mono"], size=11),
            corner_radius=12,
            border_width=1,
            border_color=THEME["border"]
        )
        self.terminal.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.terminal.insert("1.0", "[MacTech iTool] Syslog Engine Ready. Click 'Start Stream' to capture real-time Darwin kernel telemetry.\n")

    def _toggle_stream(self):
        if not self.syslog_engine.is_running:
            self.syslog_engine.start_stream()
            self.btn_toggle.configure(text="⏸ Pause Stream", fg_color=THEME["warning"])
        else:
            self.syslog_engine.stop_stream()
            self.btn_toggle.configure(text="▶ Resume Stream", fg_color=THEME["success"])

    def _clear_logs(self):
        self.terminal.delete("1.0", "end")

    def _set_filter(self, filter_name: str):
        self.current_filter = filter_name

    def _on_log_line(self, line: str, level: str):
        # Filter check
        if self.current_filter == "ERRORS" and level != "DANGER":
            return
        if self.current_filter == "KERNEL" and "kernel" not in line.lower():
            return
        if self.current_filter == "THERMAL" and "thermal" not in line.lower() and "temp" not in line.lower():
            return
        if self.current_filter == "BATTERY" and "power" not in line.lower() and "battery" not in line.lower():
            return

        self.terminal.insert("end", f"{line}\n")
        self.terminal.see("end")
