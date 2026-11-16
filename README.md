# 🍎 MacTech iTool v2.5 (Universal Edition)
### *Cross-Platform Apple Hardware Forensics, Parts Authenticity Auditor, Battery Life Extender & Device Revival Suite*
**Engineered by MacTech Solutions Lab** | **Author:** Mark Vollan Barracks (`markvollanbarracks@gmail.com`)

[![License](https://img.shields.io/badge/License-Proprietary%20%2F%20Lab-blue.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux%20%7C%20macOS-0071E3.svg)](https://mactechsolutionslab.vercel.app/products.html#mactech-itool)
[![PayPal Donate](https://img.shields.io/badge/Donate-PayPal-0070BA.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=markvollanbarracks@gmail.com&currency_code=USD&item_name=Support+MacTech+iTool+Development)

---

## 📌 Overview

**MacTech iTool** is a high-performance, cross-platform diagnostic and device revival suite engineered specifically for **Apple hardware devices**, including **iPhones**, **iPads**, **Apple Watches**, **iPods**, and **Apple TVs**. Built natively for **Windows**, **macOS** (Apple Silicon M1/M2/M3/M4 & Intel), and **Linux**, it provides electronics repair technicians, diagnostic specialists, and service laboratories with deep low-level hardware interrogation, parts authenticity verification, battery electrochemical analysis, AI-assisted kernel panic diagnostics, and official firmware restoration.

Unlike generic tools, **MacTech iTool** operates directly over Apple's native **usbmuxd** and **lockdown** protocols, featuring an automated driver installer that configures all necessary kernel drivers, Apple Mobile Device Support (AMDS), and udev rules across all operating systems.

---

## 💻 Cross-Platform Support

| Platform | Supported Environments | Quick Launch |
| :--- | :--- | :--- |
| **Windows** | Windows 10 & 11 (64-bit) | Run `Launch_Tool.bat` or `python main.py` |
| **Linux** | Ubuntu, Debian, Arch, Fedora, openSUSE | Run `./launch_linux.sh` (or `./setup_linux.sh`) |
| **macOS** | Apple Silicon (M1/M2/M3/M4) & Intel (macOS 11+) | Double-click `launch_mac.command` |

---

## 🌟 Key Diagnostic & Technician Features

### 1. 📱 Low-Level Apple Hardware Forensics
- **Complete Hardware Specifications:** Resolves internal Apple ProductTypes (e.g. `iPhone16,2` → iPhone 15 Pro Max) to marketing names, hardware board IDs (`D84AP`), chip IDs, launch years, and memory sizes.
- **Microprocessor Telemetry:** Identifies Apple Silicon architectures (Apple A-series Bionic/Pro, Apple M-series, Apple S-series SiP) and instruction sets.
- **Hardware Serial Number Auditing:** Interrogates Serial Number, IMEI, IMEI2, MEID, Unique Device ID (UDID), ECID (hex/decimal), and regulatory model numbers (e.g. `MU773LL/A`).
- **NAND Solid-State Health & Storage Breakdown:** Displays total storage capacity, used system/user partition space, and free space.
- **Telecom & Carrier Lock Status:** Reports real-time SIM hardware status, SIM-Lock carrier state, and baseband modem firmware version.

### 2. 🔍 Factory Parts & Authenticity Auditor
- **Hardware Component Serial Matching:** Queries factory calibration records written to device NVRAM and Secure Enclave at manufacture and compares them against installed physical hardware.
- **Display / True Tone Audit:** Checks screen serial number (`FMS...` / `C0...`) to detect replaced non-OEM displays and missing True Tone calibrations.
- **Battery Serial Verification:** Matches battery pack serial against logic board factory calibration tables to flag aftermarket battery swaps.
- **Front Camera & TrueDepth Face ID Sensor:** Audits front sensor and flood illuminator pairing to ensure Face ID hardware integrity.
- **Rear Camera Assembly:** Inspects multi-lens module serials and optical image stabilization (OIS) calibration tables.
- **Authenticity Scorecard:** Computes an instant percentage score (e.g., `100% Genuine Apple Parts` vs `Replaced Components Detected`).

### 3. 🔋 Battery Telemetry & Life Extender Engine
- **Electrochemical State of Health (SoH):** Computes true battery health percentage based on raw Full Charge Capacity (FCC in mAh) divided by OEM Design Capacity.
- **Cycle Count Auditing:** Tracks total recharge cycles against Apple's standard 500-cycle design rating.
- **Real-Time Power Telemetry:** Live monitoring of cell voltage (mV), instant current draw (mA), instantaneous wattage (W), and thermal sensor temperature (°C and °F).
- **Technician Longevity & Life Extension Strategies:**
  - **80% Optimized Charge Profile:** Reduces continuous high-voltage chemical stress on cathode materials.
  - **Thermal Regulation Advice:** Prevents charging above 35°C to avoid irreversible electrolyte breakdown.
  - **OLED Pure Black Efficiency:** Maximizes screen-on time by leveraging 0mA black pixel draw on OLED panels.
  - **Background Refresh Triage:** Audits runaway background location services and wake-locks.
  - **Gas Gauge Calibration Cycle:** Protocol to recalibrate Texas Instruments / Apple fuel gauge ICs.

### 4. 🩺 AI Kernel Panic & Hardware Fault Diagnostician
- **Automated Panic Log Parser:** Pulls and analyzes Apple `panic-full-*.ips` crash logs directly from the device.
- **Signature Detection Engine:** Automatically decodes hardware sensor failure signatures:
  - **`mic2` Sensor Missing (3-Minute Reboot Loop):** Pinpoints damaged charging port dock flex cables on iPhone 11 through 15 series.
  - **`prsid: 1` / `i2c0` Failure:** Identifies torn front ear speaker / ambient light sensor flex cables common after screen replacements.
  - **NAND Flash Memory / NVMe I/O Panic:** Detects cold solder joints or corrupted sectors under the NAND BGA chip.
  - **Watchdog (WDT) Gas Gauge Timeout:** Identifies communication failures on the battery HDQ data line or Tristar/Hydra charging IC.
  - **Baseband Modem Panic:** Detects baseband PMU or Qualcomm/Apple modem rail issues.
  - **AOP Panic:** Decodes audio codec or Always-On Processor sensor hub crashes.
- **Step-by-Step Repair Protocols:** Outputs exact technician procedures, diode mode test points, and component replacement steps.

### 5. ⚡ Apple Firmware (IPSW) & Device Revival Suite
- **Real-Time Signed IPSW Verification:** Connects to Apple's official signing catalog (via IPSW API) to list all currently signed and unsigned iOS releases for the exact model.
- **Direct Official Apple CDN Downloads:** One-click downloads hosted directly on Apple's ultra-fast content delivery network (`updates.cdn-apple.com`).
- **Flashing Strategies:**
  - **Clean Restore (Full Erase):** Formats NAND partitions, wipes corrupted caches, and flashes fresh iOS firmware to revive boot-looping devices.
  - **Retain User Data (Update / Repair):** Reinstalls system partitions while safeguarding client photos, messages, apps, and settings.
- **Hardware Recovery Controls:** One-click buttons to put devices into Apple Recovery Mode or kick them back into Normal Mode.
- **Interactive DFU Mode Guide:** Exact button-timing countdown for iPhone 8 through iPhone 16 Pro Max, iPhone 7, and legacy home button iPads.

### 6. 🎮 Device Command Center & Application Manager
- **Hardware Commands:** Trigger soft reboot, normal power down, SpringBoard UI respring (without kernel reboot), and display sleep/wake.
- **Live Screenshot Capture:** Grabs high-resolution display frames via developer lockdown services.
- **IPA Application Manager:** Lists installed User and System applications with bundle IDs, version numbers, and container disk usage. Allows installing custom `.ipa` packages.

### 7. 💻 Real-Time Apple Syslog Terminal
- Continuous low-latency streaming of Darwin kernel messages and daemon events (`idevicesyslog`).
- Subsystem filter pills (`ALL`, `ERRORS`, `KERNEL`, `THERMAL`, `BATTERY`) for instant root-cause analysis.

### 8. 🛠️ Universal Driver & Dependency Doctor
- **Windows:** Automatically detects Apple Mobile Device Support (AMDS), Apple Application Support (AAS), and `usbaapl64.sys` USB drivers.
- **Linux:** Manages `usbmuxd` service, `libimobiledevice` utilities, and sets up `/etc/udev/rules.d/51-apple-device.rules` for non-root USB access.
- **macOS:** Integrates seamlessly with native Apple lockdown services and Homebrew diagnostics.

---

## 🛠️ Installation & Setup by Operating System

### 🪟 Windows (10 / 11 64-bit)
1. **Automated Driver Setup:**
   Run `setup_windows.bat` to install all Python dependencies and verify Apple Mobile Device Support (AMDS).
2. **Launch Application:**
   Double-click `Launch_Tool.bat` or run:
   ```cmd
   python main.py
   ```
3. Connect your Apple device via USB-C or Lightning cable and tap **"Trust This Computer"** on the screen.

### 🐧 Linux (Ubuntu, Debian, Fedora, Arch)
1. **Run One-Step Setup:**
   ```bash
   chmod +x setup_linux.sh launch_linux.sh
   sudo ./setup_linux.sh
   ```
2. **Launch Application:**
   ```bash
   ./launch_linux.sh
   ```

### 🍎 macOS (Apple Silicon M1-M4 & Intel)
1. **Run Setup:**
   ```bash
   chmod +x setup_mac.sh launch_mac.command
   ./setup_mac.sh
   ```
2. **Launch Application:**
   Double-click `launch_mac.command` or run `python3 main.py`.

---

## ☕ Support the Developer & Lab

If MacTech iTool assisted your laboratory diagnostics or helped recover client hardware, please consider supporting development:
- **PayPal Donation Link:** [Donate to MacTech Solutions Lab](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=markvollanbarracks@gmail.com&currency_code=USD&item_name=Support+MacTech+iTool+Development)
- **PayPal Direct Account:** `markvollanbarracks@gmail.com`
