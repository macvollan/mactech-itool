"""
MacTech iTool - USBMuxd Protocol Client
Pure-Python communication with Apple USB Multiplexor daemon (usbmuxd)
Works across Windows (TCP 127.0.0.1:27015), macOS (/var/run/usbmuxd), and Linux (/var/run/usbmuxd)
"""

import sys
import os
import socket
import struct
import plistlib
import threading
import time
from typing import Optional, Dict, List, Callable, Any

USBMUX_VERSION = 1
USBMUX_TYPE_PLIST = 8
DEFAULT_WINDOWS_PORT = 27015
DEFAULT_UNIX_SOCKET = "/var/run/usbmuxd"

class USBMuxPacket:
    @staticmethod
    def pack(payload_dict: dict, tag: int = 1) -> bytes:
        data = plistlib.dumps(payload_dict)
        length = len(data) + 16
        header = struct.pack("<IIII", length, USBMUX_VERSION, USBMUX_TYPE_PLIST, tag)
        return header + data

    @staticmethod
    def unpack(sock: socket.socket) -> Optional[dict]:
        try:
            header_raw = sock.recv(16)
            if len(header_raw) < 16:
                return None
            length, version, msg_type, tag = struct.unpack("<IIII", header_raw)
            payload_len = length - 16
            if payload_len <= 0:
                return None
            
            payload_raw = bytearray()
            while len(payload_raw) < payload_len:
                chunk = sock.recv(min(4096, payload_len - len(payload_raw)))
                if not chunk:
                    break
                payload_raw.extend(chunk)
            
            return plistlib.loads(bytes(payload_raw))
        except Exception:
            return None


class USBMuxClient:
    def __init__(self):
        self.sock: Optional[socket.socket] = None
        self.connected = False
        self.is_windows = sys.platform == "win32"
        self.devices: Dict[int, dict] = {} # device_id -> device info dict

    def connect(self) -> bool:
        """Establish socket connection to usbmuxd"""
        try:
            if self.sock:
                try:
                    self.sock.close()
                except Exception:
                    pass
                self.sock = None

            if self.is_windows:
                # On Windows, Apple Mobile Device Service listens on localhost:27015
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(2.5)
                self.sock.connect(("127.0.0.1", DEFAULT_WINDOWS_PORT))
            else:
                # macOS / Linux use standard Unix domain socket
                if not os.path.exists(DEFAULT_UNIX_SOCKET):
                    return False
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.settimeout(2.5)
                self.sock.connect(DEFAULT_UNIX_SOCKET)

            self.connected = True
            return True
        except Exception:
            self.connected = False
            self.sock = None
            return False

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        self.connected = False

    def listen(self, callback: Optional[Callable[[str, dict], None]] = None):
        """Register client to listen for DeviceAdd and DeviceRemove events"""
        if not self.connect():
            return False

        req = {
            "ClientVersionString": "MacTech-iTool-v2.5",
            "MessageType": "Listen",
            "ProgName": "MacTech-iTool"
        }
        try:
            self.sock.sendall(USBMuxPacket.pack(req))
            resp = USBMuxPacket.unpack(self.sock)
            if not resp or resp.get("Number") != 0:
                return False
            return True
        except Exception:
            self.close()
            return False

    def connect_device_port(self, device_id: int, port: int) -> Optional[socket.socket]:
        """Establish a direct multiplexed tunnel to a port on the iOS device (e.g. 62078 for lockdown)"""
        sock = None
        try:
            if self.is_windows:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4.0)
                sock.connect(("127.0.0.1", DEFAULT_WINDOWS_PORT))
            else:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.settimeout(4.0)
                sock.connect(DEFAULT_UNIX_SOCKET)

            # Usbmuxd uses network byte order (big-endian) for device ports
            net_port = ((port << 8) & 0xFF00) | ((port >> 8) & 0xFF)
            req = {
                "ClientVersionString": "MacTech-iTool-v2.5",
                "MessageType": "Connect",
                "ProgName": "MacTech-iTool",
                "DeviceID": device_id,
                "PortNumber": net_port
            }
            sock.sendall(USBMuxPacket.pack(req))
            resp = USBMuxPacket.unpack(sock)
            if resp and resp.get("Number") == 0:
                sock.settimeout(15.0)
                return sock
            else:
                sock.close()
                return None
        except Exception:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
            return None
