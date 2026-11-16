"""
MacTech iTool - Main Window
MacTech Solutions Lab
Cupertino-Inspired Dark Forensic & Diagnostic Suite for Apple Devices
"""

import os
import sys
import webbrowser
import threading
import time
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import messagebox

try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
except ImportError:
    ctk = None

from ..core.apple_manager import AppleManager
from .theme import THEME
from .views.overview_view import OverviewView
from .views.authenticity_view import AuthenticityView
from .views.battery_view import BatteryView
from .views.diagnostic_view import DiagnosticView
from .views.firmware_view import FirmwareView
from .views.controller_view import ControllerView
from .views.syslog_view import SyslogView
from .views.driver_view import DriverView

PAYPAL_DONATION_URL = "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=markvollanbarracks@gmail.com&currency_code=USD&item_name=Support+MacTech+iTool+Development"

class MainWindow(ctk.CTk if ctk else object):
    def __init__(self, apple_manager: Optional[AppleManager] = None):
        if not ctk:
            raise RuntimeError("customtkinter is required to launch the GUI.")

        super().__init__()
        self.apple = apple_manager or AppleManager()

        # Window setup
        self.title("MacTech iTool v2.5 (Universal Edition) - Apple Device Diagnostics & Revival Suite")
        self.geometry("1280x840")
        self.minsize(1100, 740)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=THEME["bg_main"])

        # Set Window Icon
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        png_path = os.path.join(base_dir, "assets", "icon.png")
        ico_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(png_path):
            try:
                img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, img)
            except Exception:
                pass
        elif sys.platform == "win32" and os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # Navigation State
        self.current_view_name = "overview"
        self.views: Dict[str, Any] = {}
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self.is_monitoring = True

        # Layout Setup
        self._setup_layout()
        self._setup_sidebar()
        self._setup_topbar()
        self._setup_views()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close_window)

        # Start with default view
        self.show_view("overview")

        # Start device detection thread
        self.monitor_thread = threading.Thread(target=self._device_monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=64)
        self.grid_rowconfigure(1, weight=1)

    def _setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], corner_radius=0, border_width=1, border_color=THEME["border"])
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Lab Brand Header
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(18, 12))

        ctk.CTkLabel(
            brand_frame,
            text="🍎 MacTech iTool",
            font=ctk.CTkFont(family=THEME["font_family"], size=20, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="v2.5 Universal • Apple Forensic Suite",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            text_color=THEME["apple_cyan"]
        ).pack(anchor="w", pady=(1, 0))

        # Connection Pill Card
        self.conn_card = ctk.CTkFrame(self.sidebar, fg_color=THEME["bg_card"], corner_radius=8, border_width=1, border_color=THEME["border"])
        self.conn_card.pack(fill="x", padx=16, pady=(0, 10))

        self.lbl_conn_status = ctk.CTkLabel(
            self.conn_card,
            text="● DISCONNECTED",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            text_color=THEME["text_muted"],
            padx=10,
            pady=6
        )
        self.lbl_conn_status.pack(anchor="w")

        # Sample Preview Mode Toggle Switch
        demo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        demo_frame.pack(fill="x", padx=16, pady=(0, 14))

        self.demo_switch = ctk.CTkSwitch(
            demo_frame,
            text="⚡ Sample Preview Mode",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            text_color=THEME["text_secondary"],
            progress_color=THEME["apple_blue"],
            command=self._on_demo_toggle
        )
        self.demo_switch.pack(anchor="w")

        # Navigation Buttons List
        nav_items = [
            ("overview", "📱 Device Overview"),
            ("authenticity", "🔍 Parts Authenticity"),
            ("battery", "🔋 Battery & Life Extender"),
            ("diagnostic", "🩺 AI Panic Diagnostician"),
            ("firmware", "⚡ Firmware & IPSW Suite"),
            ("controller", "🎮 Device Commands & Apps"),
            ("syslog", "💻 Real-Time Syslog"),
            ("driver", "🛠️ Driver Doctor"),
        ]

        self.nav_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_container.pack(fill="both", expand=True, padx=12, pady=4)

        for view_key, label in nav_items:
            btn = ctk.CTkButton(
                self.nav_container,
                text=label,
                font=ctk.CTkFont(family=THEME["font_family"], size=13, weight="bold"),
                anchor="w",
                fg_color="transparent",
                hover_color=THEME["bg_card_alt"],
                text_color=THEME["text_secondary"],
                height=38,
                corner_radius=8,
                command=lambda k=view_key: self.show_view(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[view_key] = btn

        # Donation & Lab Footer
        footer = ctk.CTkFrame(self.sidebar, fg_color=THEME["bg_card"], corner_radius=8, border_width=1, border_color=THEME["border"])
        footer.pack(fill="x", padx=14, pady=14, side="bottom")

        ctk.CTkLabel(
            footer,
            text="MacTech Solutions Lab",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            text_color=THEME["text_main"]
        ).pack(anchor="w", padx=10, pady=(8, 2))

        ctk.CTkButton(
            footer,
            text="☕ Support Development",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            fg_color=THEME["apple_blue"],
            hover_color=THEME["apple_blue_hover"],
            height=28,
            command=lambda: webbrowser.open(PAYPAL_DONATION_URL)
        ).pack(fill="x", padx=10, pady=(2, 8))

    def _setup_topbar(self):
        self.topbar = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], corner_radius=0, border_width=1, border_color=THEME["border"])
        self.topbar.grid(row=0, column=1, sticky="nsew")

        tb_inner = ctk.CTkFrame(self.topbar, fg_color="transparent")
        tb_inner.pack(fill="both", expand=True, padx=20)

        # Left Info
        left_box = ctk.CTkFrame(tb_inner, fg_color="transparent")
        left_box.pack(side="left", fill="y")

        self.lbl_top_device = ctk.CTkLabel(
            left_box,
            text="No Apple Device Connected",
            font=ctk.CTkFont(family=THEME["font_family"], size=15, weight="bold"),
            text_color=THEME["text_main"]
        )
        self.lbl_top_device.pack(anchor="w", pady=(10, 0))

        self.lbl_top_sub = ctk.CTkLabel(
            left_box,
            text="Lightning / USB-C Port Listening",
            font=ctk.CTkFont(family=THEME["font_family"], size=11),
            text_color=THEME["text_secondary"]
        )
        self.lbl_top_sub.pack(anchor="w")

        # Right Badges & Refresh Button
        right_box = ctk.CTkFrame(tb_inner, fg_color="transparent")
        right_box.pack(side="right", fill="y")

        self.badge_mode = ctk.CTkLabel(
            right_box,
            text="MODE: NORMAL",
            font=ctk.CTkFont(family=THEME["font_family"], size=11, weight="bold"),
            text_color=THEME["apple_cyan"],
            fg_color=THEME["bg_card"],
            corner_radius=6,
            padx=10,
            pady=4
        )
        self.badge_mode.pack(side="left", padx=6, pady=16)

        ctk.CTkButton(
            right_box,
            text="🔄 Refresh",
            font=ctk.CTkFont(family=THEME["font_family"], size=12, weight="bold"),
            fg_color=THEME["border"],
            hover_color=THEME["border_highlight"],
            width=80,
            height=32,
            command=self._manual_refresh
        ).pack(side="left", padx=4, pady=16)

    def _setup_views(self):
        self.content_area = ctk.CTkFrame(self, fg_color=THEME["bg_main"], corner_radius=0)
        self.content_area.grid(row=1, column=1, sticky="nsew")

        self.views["overview"] = OverviewView(self.content_area, self.apple)
        self.views["authenticity"] = AuthenticityView(self.content_area, self.apple)
        self.views["battery"] = BatteryView(self.content_area, self.apple)
        self.views["diagnostic"] = DiagnosticView(self.content_area, self.apple)
        self.views["firmware"] = FirmwareView(self.content_area, self.apple)
        self.views["controller"] = ControllerView(self.content_area, self.apple)
        self.views["syslog"] = SyslogView(self.content_area, self.apple)
        self.views["driver"] = DriverView(self.content_area, self.apple)

        for view in self.views.values():
            view.pack_forget()

    def show_view(self, view_name: str):
        if view_name not in self.views:
            return

        self.current_view_name = view_name

        # Highlight active button
        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.configure(fg_color=THEME["apple_blue"], text_color=THEME["text_main"])
            else:
                btn.configure(fg_color="transparent", text_color=THEME["text_secondary"])

        for v in self.views.values():
            v.pack_forget()

        self.views[view_name].pack(fill="both", expand=True)
        self._refresh_current_view()

    def _on_demo_toggle(self):
        is_on = self.demo_switch.get() == 1
        self.apple.enable_demo_device(is_on)
        self._manual_refresh()

    def _manual_refresh(self):
        data = self.apple.check_connection()
        self._update_ui_state(data)

    def _update_ui_state(self, data: Dict[str, Any]):
        status = data.get("status", "DISCONNECTED")
        mode = data.get("mode", "DISCONNECTED")

        if status == "CONNECTED":
            model = data.get("model_name", "Apple Device")
            sn = data.get("serial_number", "N/A")
            ios = data.get("ios_version", "")
            self.lbl_top_device.configure(text=model)
            self.lbl_top_sub.configure(text=f"S/N: {sn} • iOS {ios}")
            self.lbl_conn_status.configure(text=f"● CONNECTED ({mode})", text_color=THEME["success"])
            self.badge_mode.configure(text=f"MODE: {mode}", text_color=THEME["apple_cyan"])
        else:
            self.lbl_top_device.configure(text="No Apple Device Connected")
            self.lbl_top_sub.configure(text="Connect iPhone / iPad via USB or toggle Sample Preview Mode")
            self.lbl_conn_status.configure(text="● DISCONNECTED", text_color=THEME["text_muted"])
            self.badge_mode.configure(text="MODE: IDLE", text_color=THEME["text_muted"])

        self._refresh_current_view()

    def _refresh_current_view(self):
        v = self.views.get(self.current_view_name)
        if not v:
            return

        if self.current_view_name == "overview":
            v.update_data(self.apple.cached_overview)
        elif self.current_view_name == "authenticity":
            v.update_data(self.apple.cached_authenticity)
        elif self.current_view_name == "battery":
            v.update_data(self.apple.cached_battery)
        elif self.current_view_name == "diagnostic":
            v.update_data(self.apple.cached_panic)
        elif self.current_view_name == "firmware":
            v.update_data(self.apple.cached_firmware, product_type=self.apple.cached_overview.get("product_type", "iPhone16,2"))
        elif self.current_view_name == "controller":
            v.update_data([])
        elif self.current_view_name == "driver":
            v.refresh_status()

    def _device_monitor_loop(self):
        while self.is_monitoring:
            time.sleep(2.5)
            if not self.apple.is_demo_mode:
                data = self.apple.check_connection()
                self.after(0, self._update_ui_state, data)

    def _on_close_window(self):
        self.is_monitoring = False
        try:
            self.views["syslog"].syslog_engine.stop_stream()
        except Exception:
            pass
        self.destroy()
