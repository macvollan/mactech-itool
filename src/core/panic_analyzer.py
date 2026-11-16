"""
MacTech iTool - Apple Kernel Panic & Crash Log Forensic Analyzer
Automated Fault Identification & Step-by-Step Hardware Repair Solutions Engine
"""

import re
from typing import Dict, Any, List, Optional

PANIC_SIGNATURES = [
    {
        "id": "MIC2_CHARGING_FLEX",
        "keywords": ["mic2", "prsid: 2", "prsid: 0x2", "thermal sensor 2"],
        "fault_name": "Charging Port Flex / Mic2 Sensor Missing (3-Minute Reboot Loop)",
        "component": "Charging Port Dock Flex Cable Assembly",
        "severity": "CRITICAL",
        "explanation": "iOS watchdog detected that 'mic2' (the primary thermal sensor embedded in the charging dock flex) failed to respond over the I2C bus. On iPhone 11 through 15 series, iOS triggers a hard system reboot every 180 seconds when this sensor is absent.",
        "solution": [
            "1. Disconnect battery and inspect the Lightning / USB-C charging dock flex connector on the logic board.",
            "2. Check for bent pins, debris, or corrosion in the charging flex socket.",
            "3. Test with a known-good OEM charging port flex assembly.",
            "4. If new flex still panics, check diode mode readings on the I2C0_SDA and I2C0_SCL pull-up lines."
        ]
    },
    {
        "id": "EAR_SPEAKER_PROXIMITY_FLEX",
        "keywords": ["prsid: 1", "prsid: 0x1", "i2c0", "i2c1", "ambient light sensor", "als"],
        "fault_name": "Front Ambient / Proximity / Ear Speaker Sensor Flex Failure",
        "component": "Upper Sensor / Ear Speaker Assembly",
        "severity": "HIGH",
        "explanation": "The upper ear speaker flex cable containing the ambient light sensor (ALS) or proximity sensor is torn, corroded by liquid ingress, or unseated. Often occurs after aftermarket screen replacements.",
        "solution": [
            "1. Inspect the ear speaker flex cable under a microscope for micro-tears near the fold.",
            "2. Clean liquid residue or flux near the flood illuminator / ambient light sensor.",
            "3. If damaged, transfer the original flood illuminator / ALS chip to a replacement flex to preserve Face ID pairing."
        ]
    },
    {
        "id": "NAND_FLASH_CORRUPTION",
        "keywords": ["AppleEmbeddedPCIE", "ANS2", "nand", "nvme", "storage crash", "nand read error"],
        "fault_name": "NAND Flash Memory / NVMe Controller I/O Failure",
        "component": "NAND Flash Memory BGA IC",
        "severity": "CRITICAL",
        "explanation": "The Apple storage controller encountered unrecoverable read/write errors or a fractured solder ball on the NVMe PCIe bus under the NAND flash chip.",
        "solution": [
            "1. Attempt a software firmware restore with 'Retain User Data' first.",
            "2. If error 4013 or error 9 appears during restore, inspect the NAND power rails (0.9V, 1.2V, 1.8V, 2.5V).",
            "3. Perform a reball or chip replacement of the NAND flash IC using a BGA rework station."
        ]
    },
    {
        "id": "WATCHDOG_BATTERY_GAUGE",
        "keywords": ["WDT timeout", "watchdog", "gas gauge", "battery communication", "smc", "pmu watchdog"],
        "fault_name": "Battery Fuel Gauge Communication Failure (HDQ / I2C)",
        "component": "Battery Connector / Gas Gauge / Tristar-Hydra IC",
        "severity": "HIGH",
        "explanation": "The Power Management IC (PMIC) lost telemetry communication with the battery's onboard fuel gauge IC (Texas Instruments BQ series). Can cause battery percentage stuck at 1% or random shutdowns.",
        "solution": [
            "1. Inspect the battery connector middle pins (Battery SWI / Gas Gauge HDQ data line).",
            "2. Replace the battery with a tested OEM pack.",
            "3. If problem persists, inspect the SWI diode reading on the logic board; replace the USB Charging Controller (Tristar / Hydra / Tigris IC)."
        ]
    },
    {
        "id": "BASEBAND_MODEM_PANIC",
        "keywords": ["baseband", "bb_err", "modem", "qc_modem", "qcom", "mcu crash"],
        "fault_name": "Baseband Modem / Baseband PMU Power Rail Failure",
        "component": "Baseband Processor / Baseband PMU IC",
        "severity": "CRITICAL",
        "explanation": "Kernel panic occurred due to modem processor freezing or missing baseband power rails. Device typically shows 'No Service' or missing modem firmware in Settings > General > About.",
        "solution": [
            "1. Check if IMEI and Modem Firmware appear in Settings > General > About.",
            "2. Split the sandwich logic board (on iPhone X through 16 series) on a heating preheater.",
            "3. Reball the Baseband PMU or Baseband Processor, and check for fractured interposer solder pads."
        ]
    },
    {
        "id": "AOP_AUDIO_PANIC",
        "keywords": ["AOP PANIC", "audio_codec", "cs42l", "speaker amp", "i2s"],
        "fault_name": "Audio Subsystem / Always-On Processor (AOP) Failure",
        "component": "Audio Codec IC / Sensor Hub",
        "severity": "MEDIUM",
        "explanation": "Always-On Processor crashed while polling digital audio or motion sensors. Often accompanied by grayed-out speakerphone buttons or voice memo recording failures.",
        "solution": [
            "1. Test microphone and speaker functions in Voice Memos.",
            "2. On iPhone 7/8, jump the C12 pad under the Audio IC.",
            "3. On newer models, inspect audio amplifier ICs and proximity flex sensor hub."
        ]
    },
    {
        "id": "THERMAL_SHUTDOWN",
        "keywords": ["thermal_pressure", "temp_sensor", "overtemp", "hot reboot"],
        "fault_name": "Critical Thermal Sensor Trip (Overheating Protection)",
        "component": "Logic Board Thermistor / Power Amplifier / Battery",
        "severity": "HIGH",
        "explanation": "Device reached critical temperature threshold or an onboard NTC thermistor line is shorted to ground, falsely reporting extreme temperatures.",
        "solution": [
            "1. Feel the logic board with thermal camera or freeze spray during boot to identify hot components.",
            "2. Inspect the cellular Power Amplifier (PA) module and main PMIC for short circuits.",
            "3. Verify battery temperature sensor reading using MacTech iTool Battery Monitor."
        ]
    }
]

class PanicAnalyzer:
    @staticmethod
    def analyze_panic_log(raw_log_text: str) -> Dict[str, Any]:
        """
        Scans Apple panic logs (.ips / panic-full) for known hardware signatures
        and returns automated diagnostics and actionable repair solutions.
        """
        log_lower = raw_log_text.lower()
        matched_faults = []

        for sig in PANIC_SIGNATURES:
            for kw in sig["keywords"]:
                if kw.lower() in log_lower:
                    matched_faults.append(sig)
                    break

        if not matched_faults:
            # Check for generic panic
            if "panic" in log_lower or "kernel" in log_lower:
                matched_faults.append({
                    "id": "GENERIC_KERNEL_PANIC",
                    "fault_name": "Generic Kernel Panic / Software Memory Inconsistency",
                    "component": "Operating System / Userland Daemon",
                    "severity": "MEDIUM",
                    "explanation": "A general iOS kernel panic occurred without an identifiable hardware sensor signature. This can be caused by corrupted system caches, full storage (0 bytes free), or jailbreak tweaks.",
                    "solution": [
                        "1. Perform an iOS firmware update/reinstall using MacTech iTool Firmware Suite.",
                        "2. Inspect device free storage space to verify NAND is not 100% saturated.",
                        "3. If reboots persist, perform full factory restore."
                    ]
                })
            else:
                return {
                    "has_panic": False,
                    "message": "No active kernel panic signatures detected in the provided log.",
                    "faults": []
                }

        # Extract timestamp, OS version, panic string if available
        os_match = re.search(r"OS version:\s*([^\n\r]+)", raw_log_text, re.IGNORECASE)
        panic_str_match = re.search(r"panicString\"?\s*:\s*\"([^\"]+)\"", raw_log_text, re.IGNORECASE)

        return {
            "has_panic": True,
            "os_version": os_match.group(1).strip() if os_match else "iOS / iPadOS",
            "panic_string": panic_str_match.group(1) if panic_str_match else "Kernel panic detected",
            "faults_detected_count": len(matched_faults),
            "primary_fault": matched_faults[0],
            "all_faults": matched_faults
        }

    @staticmethod
    def get_sample_panic_log(fault_type: str = "mic2") -> str:
        """Returns realistic sample panic log for technician diagnostic demonstration"""
        if fault_type == "mic2":
            return (
                "{\"bug_type\":\"210\",\"timestamp\":\"2026-11-14 14:22:10.00 +0300\",\"os_version\":\"iPhone OS 18.1 (22B83)\"}\n"
                "panic(cpu 1 caller 0xfffffff01a42b100): \"Missing sensor: mic2, i2c0 target 0x36 not responding! Watchdog reset triggered.\"\n"
                "Debugger message: panic\n"
                "OS version: 22B83\n"
                "Kernel version: Darwin Kernel Version 24.1.0\n"
                "Panicked task 0xfffffff1928000: 450 pages, 32 threads: pid 0: kernel_task\n"
            )
        elif fault_type == "nand":
            return (
                "{\"bug_type\":\"210\",\"timestamp\":\"2026-11-12 09:15:30.00 +0300\",\"os_version\":\"iPhone OS 17.5.1 (21F90)\"}\n"
                "panic(cpu 0 caller 0xfffffff018d91040): \"AppleEmbeddedPCIE::Fatal PCIe link down on port 0! ANS2 NVMe controller unresponsive.\"\n"
                "Debugger message: panic\n"
                "OS version: 21F90\n"
                "Kernel version: Darwin Kernel Version 23.5.0\n"
            )
        elif fault_type == "battery":
            return (
                "{\"bug_type\":\"210\",\"timestamp\":\"2026-11-15 18:40:02.00 +0300\",\"os_version\":\"iPhone OS 18.0 (22A3354)\"}\n"
                "panic(cpu 2 caller 0xfffffff01b223010): \"WDT timeout! Gas Gauge HDQ SWI communication failure. PMU watchdog reset.\"\n"
                "Debugger message: panic\n"
                "OS version: 22A3354\n"
            )
        return ""
