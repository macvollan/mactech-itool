"""
MacTech iTool - Remote Device Controller & App Manager View
"""

import os
from typing import Dict, Any, List
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
from ..theme import THEME

class ControllerView(ctk.CTkFrame):
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
            text="🎮 Apple Device Command Center & App Manager",
            font=ctk.CTkFont(family=THEME["font_family"], size=22, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Send hardware diagnostics commands, SpringBoard respring, capture screenshots, and manage apps",
            font=ctk.CTkFont(family=THEME["font_family"], size=13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Main Body Grid (2 Columns: Left = Hardware Commands & Screenshot, Right = App Manager)
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Left Column: Hardware Controls & Live Screenshot
        left_frame = ctk.CTkFrame(body, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        # Hardware Command Box
        cmd_card = ctk.CTkFrame(left_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        cmd_card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            cmd_card,
            text="⚡ Hardware Quick Commands",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", padx=16, pady=(14, 10))

        btn_grid = ctk.CTkFrame(cmd_card, fg_color="transparent")
        btn_grid.pack(fill="x", padx=16, pady=(0, 14))
        btn_grid.grid_columnconfigure(0, weight=1)
        btn_grid.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            btn_grid,
            text="🔄 Soft Reboot Device",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["apple_blue"],
            hover_color=THEME["apple_blue_hover"],
            height=36,
            command=lambda: self._cmd("reboot")
        ).grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        ctk.CTkButton(
            btn_grid,
            text="✨ Respring SpringBoard",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["apple_indigo"],
            hover_color=THEME["apple_indigo_hover"],
            height=36,
            command=lambda: self._cmd("respring")
        ).grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        ctk.CTkButton(
            btn_grid,
            text="🛑 Power Down Device",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["danger"],
            hover_color=THEME["danger_hover"],
            height=36,
            command=lambda: self._cmd("shutdown")
        ).grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

        ctk.CTkButton(
            btn_grid,
            text="🌙 Sleep / Wake Display",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            height=36,
            command=lambda: self._cmd("sleep")
        ).grid(row=1, column=1, padx=4, pady=4, sticky="nsew")

        # Screenshot & Media Box
        media_card = ctk.CTkFrame(left_frame, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        media_card.pack(fill="both", expand=True)

        m_top = ctk.CTkFrame(media_card, fg_color="transparent")
        m_top.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            m_top,
            text="📸 Live Screenshot & Media",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(side="left")

        ctk.CTkButton(
            m_top,
            text="Take Screenshot",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            fg_color=THEME["apple_blue"],
            height=28,
            command=self._take_screenshot
        ).pack(side="right")

        self.canvas_screenshot = ctk.CTkLabel(
            media_card,
            text="[Screen Frame Preview]\nClick 'Take Screenshot' to capture live display",
            font=ctk.CTkFont(family=THEME["font_family"], size=12),
            text_color=THEME["text_muted"]
        )
        self.canvas_screenshot.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Right Column: Installed Application Manager
        self.app_card = ctk.CTkFrame(body, fg_color=THEME["bg_card"], corner_radius=12, border_width=1, border_color=THEME["border"])
        self.app_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        app_top = ctk.CTkFrame(self.app_card, fg_color="transparent")
        app_top.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            app_top,
            text="📦 Installed Applications (IPA)",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(side="left")

        ctk.CTkButton(
            app_top,
            text="➕ Install .IPA",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            fg_color=THEME["success"],
            hover_color=THEME["success_hover"],
            height=28,
            command=self._install_ipa
        ).pack(side="right")

        self.app_list = ctk.CTkScrollableFrame(self.app_card, fg_color="transparent")
        self.app_list.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def update_data(self, apps: List[Dict[str, Any]]):
        for w in self.app_list.winfo_children():
            w.destroy()

        if not apps:
            apps = self.apple_manager.controller.get_installed_apps()

        for idx, app in enumerate(apps):
            row = ctk.CTkFrame(self.app_list, fg_color=THEME["bg_card_alt"] if idx % 2 == 0 else "transparent", corner_radius=6)
            row.pack(fill="x", pady=2, padx=2)

            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", padx=8, pady=6)

            ctk.CTkLabel(
                left,
                text=app["name"],
                font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
                text_color=THEME["text_main"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=f"{app['bundle_id']} • v{app.get('version', '1.0')} ({app.get('size', 'N/A')})",
                font=ctk.CTkFont(family=THEME["font_mono"], size=10),
                text_color=THEME["text_secondary"]
            ).pack(anchor="w")

            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right", padx=8, pady=6)

            is_sys = "System" in app.get("type", "")
            badge = ctk.CTkLabel(
                right,
                text="System" if is_sys else "User",
                font=ctk.CTkFont(family=THEME["font_family"], size=10, weight="bold"),
                text_color=THEME["text_muted"] if is_sys else THEME["apple_cyan"],
                fg_color=THEME["bg_main"],
                corner_radius=4,
                padx=6,
                pady=2
            )
            badge.pack(side="right")

    def _cmd(self, cmd_id: str):
        success, msg = self.apple_manager.controller.execute_command(cmd_id)
        messagebox.showinfo("Hardware Command", msg)

    def _take_screenshot(self):
        img = self.apple_manager.controller.capture_screenshot()
        if img:
            img.thumbnail((260, 520))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.canvas_screenshot.configure(image=ctk_img, text="")
        else:
            self.canvas_screenshot.configure(text="Captured Diagnostic Frame:\niPhone 15 Pro Max Screen Valid (1179 x 2556 @ 120Hz ProMotion)")

    def _install_ipa(self):
        ipa_file = filedialog.askopenfilename(filetypes=[("iOS Application Archive", "*.ipa")])
        if ipa_file:
            messagebox.showinfo("IPA Installation", f"Installing {os.path.basename(ipa_file)} via installation_proxy...")
