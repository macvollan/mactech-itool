"""
MacTech iTool - Main Entry Point
MacTech Solutions Lab
Automated Apple Hardware Forensics, Authenticity Auditor & Device Revival Suite
"""

import sys
import os

# Ensure package root is placed in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core.apple_manager import AppleManager
from src.ui.main_window import MainWindow

def main():
    try:
        apple_mgr = AppleManager()
        # Enable demo mode by default on initial technician launch so UI displays rich telemetry immediately
        apple_mgr.enable_demo_device(True)
        app = MainWindow(apple_manager=apple_mgr)
        app.demo_switch.select()
        app.mainloop()
    except Exception as e:
        print(f"Error launching MacTech iTool: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
