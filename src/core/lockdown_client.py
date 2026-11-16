"""
MacTech iTool - Apple Lockdown Protocol Client
Communicates with 'com.apple.mobile.lockdown' service (port 62078) to extract
device attributes, hardware serials, battery telemetry, and diagnostics.
"""

import sys
import os
import ssl
import socket
import struct
import plistlib
from typing import Optional, Dict, Any

LOCKDOWN_PORT = 62078

class LockdownPacket:
    @staticmethod
    def pack(payload: dict) -> bytes:
        data = plistlib.dumps(payload)
        return struct.pack(">I", len(data)) + data

    @staticmethod
    def unpack(sock) -> Optional[dict]:
        try:
            len_bytes = sock.recv(4)
            if len(len_bytes) < 4:
                return None
            length = struct.unpack(">I", len_bytes)[0]
            raw = bytearray()
            while len(raw) < length:
                chunk = sock.recv(min(4096, length - len(raw)))
                if not chunk:
                    break
                raw.extend(chunk)
            return plistlib.loads(bytes(raw))
        except Exception:
            return None


class LockdownClient:
    def __init__(self, raw_socket: socket.socket):
        self.raw_sock = raw_socket
        self.sock = raw_socket
        self.is_ssl = False
        self.all_values: Dict[str, Any] = {}

    def query_type(self) -> Optional[str]:
        req = {"Request": "QueryType"}
        self.sock.sendall(LockdownPacket.pack(req))
        resp = LockdownPacket.unpack(self.sock)
        if resp and resp.get("Request") == "QueryType":
            return resp.get("Type")
        return None

    def get_value(self, domain: Optional[str] = None, key: Optional[str] = None) -> Any:
        req = {"Request": "GetValue"}
        if domain:
            req["Domain"] = domain
        if key:
            req["Key"] = key
        
        try:
            self.sock.sendall(LockdownPacket.pack(req))
            resp = LockdownPacket.unpack(self.sock)
            if resp and "Value" in resp:
                return resp["Value"]
        except Exception:
            pass
        return None

    def get_all_device_info(self) -> Dict[str, Any]:
        """Fetch complete hardware & software overview across all lockdown domains"""
        info = {}
        # 1. Root domain query
        root_values = self.get_value()
        if isinstance(root_values, dict):
            info.update(root_values)

        # 2. Battery domain query
        bat = self.get_value(domain="com.apple.mobile.battery")
        if isinstance(bat, dict):
            info["Battery"] = bat

        # 3. Disk usage domain query
        disk = self.get_value(domain="com.apple.disk_usage")
        if isinstance(disk, dict):
            info["Disk"] = disk

        # 4. International / Region query
        intl = self.get_value(domain="com.apple.international")
        if isinstance(intl, dict):
            info["International"] = intl

        self.all_values = info
        return info

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass
