"""
MacTech iTool - Battery Health, Telemetry & Life Extension View
"""

from typing import Dict, Any
import customtkinter as ctk
from ..theme import THEME

class BatteryView(ctk.CTkFrame):
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
            text="🔋 Apple Battery Health, Gas Gauge Telemetry & Life Extender",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Real-time electrochemical analysis, cycle tracking, wear percentage and longevity preservation",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Main Scrollable Body
        self.body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Metric Tiles Container (4 columns)
        self.tiles_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.tiles_frame.pack(fill="x", pady=(0, 12))
        for col in range(4):
            self.tiles_frame.grid_columnconfigure(col, weight=1)

        self.tile_health = self._create_tile(self.tiles_frame, 0, "State of Health", "--%", THEME["success"])
        self.tile_cycles = self._create_tile(self.tiles_frame, 1, "Cycle Count", "--", THEME["apple_cyan"])
        self.tile_capacity = self._create_tile(self.tiles_frame, 2, "Full Charge Capacity", "-- mAh", THEME["text_main"])
        self.tile_temp = self._create_tile(self.tiles_frame, 3, "Battery Temperature", "-- °C", THEME["warning"])

        # Two Columns: Left = Raw Telemetry Table, Right = Battery Extender Advice
        two_col = ctk.CTkFrame(self.body, fg_color="transparent")
        two_col.pack(fill="both", expand=True)
        two_col.grid_columnconfigure(0, weight=1)
        two_col.grid_columnconfigure(1, weight=1)

        # Left Column: In-Depth Telemetry
        self.telem_card = ctk.CTkFrame(two_col, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.telem_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        ctk.CTkLabel(
            self.telem_card,
            text="⚡ Low-Level Gas Gauge Parameters",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.telem_table = ctk.CTkFrame(self.telem_card, fg_color="transparent")
        self.telem_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Right Column: Battery Life Preservation Strategies
        self.tips_card = ctk.CTkFrame(two_col, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.tips_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        ctk.CTkLabel(
            self.tips_card,
            text="🛡️ Battery Longevity & Life Extension Strategies",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["success"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.tips_container = ctk.CTkFrame(self.tips_card, fg_color="transparent")
        self.tips_container.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def _create_tile(self, parent, col, title, initial_val, color):
        frame = ctk.CTkFrame(parent, fg_color=THEME["bg_card"], corner_radius=10, border_width=1, border_color=THEME["border"])
        frame.grid(row=0, column=col, sticky="nsew", padx=4, pady=4)

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=THEME["text_secondary"]).pack(anchor="w", padx=14, pady=(12, 4))
        val_lbl = ctk.CTkLabel(frame, text=initial_val, font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"), text_color=color)
        val_lbl.pack(anchor="w", padx=14, pady=(0, 12))
        return val_lbl

    def update_data(self, data: Dict[str, Any]):
        if not data or not data.get("health_pct"):
            self.tile_health.configure(text="--%")
            self.tile_cycles.configure(text="--")
            self.tile_capacity.configure(text="-- mAh")
            self.tile_temp.configure(text="-- °C")
            return

        # Update Tiles
        pct = data.get("health_pct", 100)
        cond = data.get("condition", "NORMAL")
        self.tile_health.configure(text=f"{pct}% ({cond})", text_color=data.get("condition_color", THEME["success"]))
        self.tile_cycles.configure(text=f"{data.get('cycle_count', 0)} Cycles")
        self.tile_capacity.configure(text=f"{data.get('fcc_mah', 0)} / {data.get('design_capacity_mah', 0)} mAh")
        self.tile_temp.configure(text=f"{data.get('temp_c', 0)} °C / {data.get('temp_f', 0)} °F")

        # Telemetry table
        for w in self.telem_table.winfo_children():
            w.destroy()

        rows = [
            ("State of Health (SoH)", f"{pct}%"),
            ("Design Rating Capacity", f"{data.get('design_capacity_mah', 0)} mAh"),
            ("Full Charge Capacity (FCC)", f"{data.get('fcc_mah', 0)} mAh"),
            ("Cycle Count Rating", f"{data.get('cycle_count', 0)} / 500 OEM Target"),
            ("Cell Instant Voltage", f"{data.get('voltage_mv', 0)} mV ({round(data.get('voltage_mv', 0)/1000, 2)} V)"),
            ("Instant Charge/Discharge Draw", f"{data.get('amperage_ma', 0)} mA"),
            ("Instant Power Draw", f"{data.get('wattage', 0)} W"),
            ("Operating Cell Temperature", f"{data.get('temp_c', 0)} °C ({data.get('temp_f', 0)} °F)"),
            ("Gas Gauge IC State", "Synchronized & Communicating"),
        ]

        for idx, (lbl, val) in enumerate(rows):
            r = ctk.CTkFrame(self.telem_table, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=6)
            r.pack(fill="x", pady=2, padx=2)
            ctk.CTkLabel(r, text=lbl, font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"), text_color=THEME["text_secondary"], width=200, anchor="w").pack(side="left", padx=8, pady=3)
            ctk.CTkLabel(r, text=val, font=ctk.CTkFont(family=THEME["font_mono"], size=12), text_color=THEME["text_main"], anchor="w").pack(side="left", fill="x", expand=True, padx=8, pady=3)

        # Preservation Strategies
        for w in self.tips_container.winfo_children():
            w.destroy()

        tips = data.get("preservation_tips", [])
        for tip in tips:
            t_box = ctk.CTkFrame(self.tips_container, fg_color=THEME["bg_card_alt"], corner_radius=8, border_width=1, border_color=THEME["border"])
            t_box.pack(fill="x", pady=4, padx=2)

            top = ctk.CTkFrame(t_box, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(8, 2))
            ctk.CTkLabel(top, text=tip["title"], font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"), text_color=THEME["apple_cyan"]).pack(side="left")
            ctk.CTkLabel(top, text=tip["impact"], font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"), text_color=THEME["success"]).pack(side="right")

            ctk.CTkLabel(t_box, text=tip["detail"], font=ctk.CTkFont(family=THEME["font_family"], size=11), text_color=THEME["text_secondary"], justify="left", wraplength=480).pack(anchor="w", padx=12, pady=(0, 8))
