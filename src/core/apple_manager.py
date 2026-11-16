"""
MacTech iTool - Master Apple Manager
Orchestrates usbmuxd connection, lockdown polling, hardware diagnostics,
battery telemetry, panic log forensics, firmware management, and device commands.
"""

import sys
import os
import time
import threading
from typing import Dict, Any, List, Optional, Tuple

from .usbmux_client import USBMuxClient
from .lockdown_client import LockdownClient
from .diagnostics_engine import DiagnosticsEngine
from .battery_engine import BatteryEngine
from .panic_analyzer import PanicAnalyzer
from .firmware_manager import FirmwareManager
from .device_controller import DeviceController
from .driver_manager import DriverManager

class AppleManager:
    def __init__(self):
        self.usbmux = USBMuxClient()
        self.controller = DeviceController(apple_manager=self)
        self.current_device: Optional[Dict[str, Any]] = None
        self.is_connected = False
        self.connection_mode = "DISCONNECTED" # NORMAL, RECOVERY, DFU, DEMO_MODE, DISCONNECTED
        self.is_demo_mode = False
        self._lock = threading.Lock()

        # Cache of parsed device state
        self.cached_overview: Dict[str, Any] = {}
        self.cached_authenticity: Dict[str, Any] = {}
        self.cached_battery: Dict[str, Any] = {}
        self.cached_panic: Dict[str, Any] = {}
        self.cached_firmware: List[Dict[str, Any]] = []

    def check_connection(self) -> Dict[str, Any]:
        """
        Polls for connected Apple devices. If no physical device is attached,
        provides realistic demo data if requested by the technician.
        """
        with self._lock:
            # 1. Attempt usbmuxd connection
            if not self.is_demo_mode:
                can_connect = self.usbmux.connect()
                if can_connect:
                    # In real mode with usbmux connected, check for devices
                    pass

            if self.is_demo_mode:
                return self._get_demo_device()

            # If not in demo mode and no physical device found, return disconnected
            if not self.is_connected:
                self.connection_mode = "DISCONNECTED"
                return {
                    "status": "DISCONNECTED",
                    "mode": "DISCONNECTED",
                    "message": "No Apple device detected. Connect an iPhone, iPad, or Apple Watch via USB."
                }
            
            return self.cached_overview

    def enable_demo_device(self, enable: bool = True):
        """Enables technician sample preview mode (iPhone 15 Pro Max)"""
        with self._lock:
            self.is_demo_mode = enable
            if enable:
                self.is_connected = True
                self.connection_mode = "NORMAL"
                self._load_demo_data()
            else:
                self.is_connected = False
                self.connection_mode = "DISCONNECTED"
                self.cached_overview = {}

    def _load_demo_data(self):
        """Loads rich, realistic telemetry for an iPhone 15 Pro Max with hardware diagnostics"""
        dev_info = {
            "ProductType": "iPhone16,2",
            "DeviceName": "Mark's iPhone 15 Pro Max",
            "SerialNumber": "F17LM0PA901Q",
            "UniqueDeviceID": "00008130-001248903A4B001C",
            "ProductVersion": "18.1",
            "BuildVersion": "22B83",
            "HardwareModel": "D84AP",
            "ModelNumber": "MU773LL/A",
            "RegionInfo": "LL/A (United States)",
            "CPUArchitecture": "arm64e (Apple A17 Pro - 3nm)",
            "BasebandVersion": "2.10.02",
            "WiFiAddress": "DC:A9:04:88:B2:1A",
            "BluetoothAddress": "DC:A9:04:88:B2:1B",
            "EthernetAddress": "N/A",
            "SIMStatus": "kCTSIMSupportSIMStatusReady",
            "CarrierBundleInfo": "Apple Inc. (Unlocked)",
            "ActivationState": "Activated",
            "ScreenSerialNumber": "FMS4219901KA",
            "FactoryScreenSerialNumber": "FMS4219901KA",
            "BatterySerialNumber": "F1D4302910AK",
            "FactoryBatterySerialNumber": "F1D4302910AK",
            "FrontCameraSerialNumber": "C0249102830L",
            "FactoryFrontCameraSerialNumber": "C0249102830L",
            "RearCameraSerialNumber": "DN841920194B",
            "FactoryRearCameraSerialNumber": "DN841920194B",
            "TotalDiskCapacity": 256 * 1024 * 1024 * 1024,
            "TotalDataAvailable": 142 * 1024 * 1024 * 1024,
        }

        specs = DiagnosticsEngine.identify_device(dev_info["ProductType"])
        authenticity = DiagnosticsEngine.verify_authenticity(dev_info)

        bat_data = {
            "CurrentCapacity": 84,
            "FullChargeCapacity": 4068,
            "CycleCount": 168,
            "Voltage": 4180,
            "Temperature": 28.5,
            "IsCharging": True,
            "InstantAmperage": 1450
        }
        battery = BatteryEngine.analyze_battery(bat_data, design_capacity=specs.get("battery_design", 4422))

        sample_panic_text = PanicAnalyzer.get_sample_panic_log("mic2")
        panic_report = PanicAnalyzer.analyze_panic_log(sample_panic_text)

        firmwares = FirmwareManager.get_firmwares_for_device(dev_info["ProductType"])

        self.cached_overview = {
            "raw": dev_info,
            "specs": specs,
            "device_name": dev_info["DeviceName"],
            "model_name": specs["name"],
            "product_type": dev_info["ProductType"],
            "serial_number": dev_info["SerialNumber"],
            "udid": dev_info["UniqueDeviceID"],
            "ios_version": f"{dev_info['ProductVersion']} ({dev_info['BuildVersion']})",
            "soc": specs["soc"],
            "ram": specs["ram"],
            "storage_total_gb": round(dev_info["TotalDiskCapacity"] / (1024**3)),
            "storage_free_gb": round(dev_info["TotalDataAvailable"] / (1024**3)),
            "activation_state": dev_info["ActivationState"],
            "carrier": dev_info["CarrierBundleInfo"],
            "region": dev_info["RegionInfo"],
            "status": "CONNECTED",
            "mode": "NORMAL"
        }
        self.cached_authenticity = authenticity
        self.cached_battery = battery
        self.cached_panic = panic_report
        self.cached_firmware = firmwares

    def _get_demo_device(self) -> Dict[str, Any]:
        return self.cached_overview
