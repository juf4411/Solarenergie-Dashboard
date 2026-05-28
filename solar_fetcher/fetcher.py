"""Fetch and normalize raw solar plant readings."""

from datetime import datetime, timezone
import math
import random
from typing import Any

import requests


REQUIRED_FIELDS = {
    "timestamp",
    "plant_id",
    "power_w",
    "energy_today_kwh",
    "temperature_c",
}


def generate_sample_reading(plant_id: str = "hochschule-pv-1") -> dict[str, Any]:
    """Create a realistic sample reading when no external data source is configured."""

    now = datetime.now(timezone.utc)
    hour_angle = (now.hour + now.minute / 60) / 24 * 2 * math.pi
    daylight_factor = max(0.0, math.sin(hour_angle - math.pi / 2))
    power_w = round(5500 * daylight_factor + random.uniform(0, 120), 2)

    return {
        "timestamp": now.isoformat(),
        "plant_id": plant_id,
        "power_w": power_w,
        "energy_today_kwh": round(power_w / 1000 * 4.2, 3),
        "temperature_c": round(18 + daylight_factor * 14 + random.uniform(-1.5, 1.5), 2),
    }


def fetch_reading(source_url: str | None = None) -> dict[str, Any]:
    """Fetch one reading from an HTTP endpoint or generate sample data."""

    if not source_url:
        return generate_sample_reading()

    response = requests.get(source_url, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list):
        if not payload:
            raise ValueError("data source returned an empty list")
        payload = payload[-1]
    if not isinstance(payload, dict):
        raise ValueError("data source must return a JSON object or list of objects")
    return payload


def normalize_reading(raw: dict[str, Any]) -> dict[str, Any]:
    """Validate and convert a raw reading into stable internal types."""

    missing = REQUIRED_FIELDS.difference(raw)
    if missing:
        raise ValueError(f"reading is missing fields: {', '.join(sorted(missing))}")

    timestamp = datetime.fromisoformat(str(raw["timestamp"]).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return {
        "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
        "plant_id": str(raw["plant_id"]),
        "power_w": float(raw["power_w"]),
        "energy_today_kwh": float(raw["energy_today_kwh"]),
        "temperature_c": float(raw["temperature_c"]),
    }
