"""Prepare solar data for API responses and dashboards."""

from statistics import mean
from typing import Any


def calculate_average_power(readings: list[dict[str, Any]]) -> float:
    """Calculate the average power in watts for a list of readings."""

    if not readings:
        return 0.0
    return round(mean(float(reading["power_w"]) for reading in readings), 2)


def calculate_total_energy(readings: list[dict[str, Any]]) -> float:
    """Return the highest reported daily energy value in kWh."""

    if not readings:
        return 0.0
    return round(max(float(reading["energy_today_kwh"]) for reading in readings), 3)


def build_dashboard_summary(readings: list[dict[str, Any]]) -> dict[str, Any]:
    """Build compact values that are easy to display in Grafana or an API client."""

    latest = readings[0] if readings else None
    return {
        "reading_count": len(readings),
        "latest": latest,
        "average_power_w": calculate_average_power(readings),
        "energy_today_kwh": calculate_total_energy(readings),
    }


def format_reading_for_display(reading: dict[str, Any]) -> dict[str, str]:
    """Format one reading as strings for simple dashboard display."""

    return {
        "time": str(reading["timestamp"]),
        "plant": str(reading["plant_id"]),
        "power": f"{float(reading['power_w']):.2f} W",
        "energy_today": f"{float(reading['energy_today_kwh']):.3f} kWh",
        "temperature": f"{float(reading['temperature_c']):.2f} C",
    }
