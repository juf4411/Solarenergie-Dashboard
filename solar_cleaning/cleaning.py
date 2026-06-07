"""Data cleaning for raw photovoltaic readings."""

from datetime import UTC, datetime
from typing import Any

REQUIRED_FIELDS = {
    "timestamp",
    "plant_id",
    "power_w",
    "energy_today_kwh",
    "temperature_c",
}


def parse_timestamp(value: Any) -> str:
    """Convert timestamps to UTC ISO format."""

    timestamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)
    return timestamp.astimezone(UTC).isoformat()


def parse_float(value: Any, field_name: str) -> float:
    """Convert a numeric value to float and reject negative measurements."""

    number = float(value)
    if number < 0:
        raise ValueError(f"{field_name} must not be negative")
    return number


def clean_reading(raw: dict[str, Any]) -> dict[str, Any]:
    """Validate and clean one raw PV reading."""

    missing = REQUIRED_FIELDS.difference(raw)
    if missing:
        raise ValueError(f"reading is missing fields: {', '.join(sorted(missing))}")

    is_test_data = bool(raw.get("is_test_data", False))
    data_source = str(raw.get("data_source", "TESTDATEN" if is_test_data else "live"))

    return {
        "timestamp": parse_timestamp(raw["timestamp"]),
        "plant_id": str(raw["plant_id"]).strip(),
        "power_w": parse_float(raw["power_w"], "power_w"),
        "energy_today_kwh": parse_float(raw["energy_today_kwh"], "energy_today_kwh"),
        "temperature_c": parse_float(raw["temperature_c"], "temperature_c"),
        "data_source": data_source,
        "is_test_data": is_test_data,
    }
