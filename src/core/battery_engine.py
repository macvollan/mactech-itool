"""
MacTech iTool - Battery Health, Telemetry & Life Extension Engine
Deep Electrochemical Analysis, Gas Gauge Auditing & Life-Extending Technician Advice
"""

from typing import Dict, Any, List

class BatteryEngine:
    @staticmethod
    def analyze_battery(battery_data: Dict[str, Any], design_capacity: int = 3200) -> Dict[str, Any]:
        """
        Calculates battery state of health, wear level, instant draw, and electrochemical safety
        """
        current_capacity = battery_data.get("CurrentCapacity", 85)
        raw_fcc = battery_data.get("FullChargeCapacity", int(design_capacity * 0.94))
        cycle_count = battery_data.get("CycleCount", 142)
        voltage_mv = battery_data.get("Voltage", 4120)
        temp_c = battery_data.get("Temperature", 27.5)
        if temp_c > 100:
            # Some lockdown versions return temp in 0.01 deg C
            temp_c = temp_c / 100.0
        
        is_charging = battery_data.get("IsCharging", True)
        amperage_ma = battery_data.get("InstantAmperage", 1250 if is_charging else -320)
        
        # Calculate State of Health (SoH)
        health_pct = round((raw_fcc / design_capacity) * 100.0, 1) if design_capacity > 0 else 100.0
        health_pct = max(1.0, min(100.0, health_pct))

        # Battery Health Status Classification
        if health_pct >= 90:
            condition = "EXCELLENT"
            condition_color = "#30D158" # Apple Green
            desc = "Battery cell health is optimal. No electrochemical degradation observed."
        elif health_pct >= 80:
            condition = "NORMAL"
            condition_color = "#00C7BE" # Apple Cyan
            desc = "Normal chemical aging. Device supports peak performance capability."
        elif health_pct >= 70:
            condition = "SERVICE RECOMMENDED"
            condition_color = "#FF9F0A" # Apple Amber
            desc = "Battery capacity depleted below 80%. iOS performance management throttling active."
        else:
            condition = "CRITICAL DEGRADATION"
            condition_color = "#FF453A" # Apple Red
            desc = "Severe electrochemical wear. High risk of unexpected shutdowns and swelling."

        # Safety & Anomaly Flags
        warnings: List[str] = []
        if cycle_count > 500:
            warnings.append(f"High Cycle Count ({cycle_count} cycles): Surpassed standard 500-cycle OEM design rating.")
        if temp_c > 42.0:
            warnings.append(f"Thermal Alert ({temp_c:.1f}°C): Operating temperature exceeds safe threshold (40°C).")
        if voltage_mv < 3400 and not is_charging:
            warnings.append("Low Cutoff Voltage: Risk of abrupt system reboot under peak CPU/GPU loads.")

        # Battery Life Extension Strategies & Technician Recommendations
        preservation_tips = [
            {
                "title": "80% Optimized Charge Limit",
                "impact": "+35% Lifespan Extension",
                "detail": "Restricting continuous peak charging to 80% prevents high-voltage stress on the cobalt-oxide cathode."
            },
            {
                "title": "Thermal Management & Fast Charge Dissipation",
                "impact": "+20% Cell Preservation",
                "detail": "Avoid charging in thick cases or direct sunlight. Heat above 35°C accelerates irreversible electrolyte decomposition."
            },
            {
                "title": "Pure OLED Black Mode Activation",
                "impact": "+15-25% Daily Screen-On Time",
                "detail": "OLED panels draw 0mA on black pixels (#000000). System-wide Dark Mode reduces display power consumption by up to 40%."
            },
            {
                "title": "Background App Refresh Triage",
                "impact": "+10-18% Daily Battery Life",
                "detail": "Disable background telemetry for social media and navigation apps to stop wake-lock CPU battery drain."
            },
            {
                "title": "Gas Gauge Re-Calibration Cycle",
                "impact": "Accurate % Reading",
                "detail": "Discharge to 1% until auto-shutdown, then charge uninterrupted to 100% plus 2 hours trickle to calibrate the fuel gauge IC."
            }
        ]

        return {
            "health_pct": health_pct,
            "condition": condition,
            "condition_color": condition_color,
            "description": desc,
            "fcc_mah": raw_fcc,
            "design_capacity_mah": design_capacity,
            "cycle_count": cycle_count,
            "voltage_mv": voltage_mv,
            "temp_c": temp_c,
            "temp_f": round(temp_c * 9 / 5 + 32, 1),
            "is_charging": is_charging,
            "amperage_ma": amperage_ma,
            "wattage": round((voltage_mv / 1000.0) * (abs(amperage_ma) / 1000.0), 2),
            "warnings": warnings,
            "preservation_tips": preservation_tips
        }
