import pytest

from solar_fetcher.fetcher import generate_sample_reading, normalize_reading


def test_generate_sample_reading_contains_required_fields():
    reading = generate_sample_reading("campus-roof")

    assert reading["plant_id"] == "campus-roof"
    assert reading["power_w"] >= 0
    assert "timestamp" in reading


def test_normalize_reading_converts_values_to_stable_types():
    normalized = normalize_reading(
        {
            "timestamp": "2026-05-28T10:00:00Z",
            "plant_id": 12,
            "power_w": "1234.5",
            "energy_today_kwh": "5.25",
            "temperature_c": "24.1",
        }
    )

    assert normalized["timestamp"] == "2026-05-28T10:00:00+00:00"
    assert normalized["plant_id"] == "12"
    assert normalized["power_w"] == 1234.5


def test_normalize_reading_rejects_missing_fields():
    with pytest.raises(ValueError):
        normalize_reading({"timestamp": "2026-05-28T10:00:00Z"})
