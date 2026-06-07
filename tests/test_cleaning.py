import pytest

from solar_cleaning.cleaning import clean_reading, parse_float, parse_timestamp


def test_parse_timestamp_returns_utc_iso_format():
    assert parse_timestamp("2026-05-28T10:00:00Z") == "2026-05-28T10:00:00+00:00"


def test_parse_float_rejects_negative_values():
    with pytest.raises(ValueError):
        parse_float("-1", "power_w")


def test_clean_reading_strips_plant_id_and_marks_live_data():
    cleaned = clean_reading(
        {
            "timestamp": "2026-05-28T10:00:00Z",
            "plant_id": " hochschule-pv-1 ",
            "power_w": "1200.5",
            "energy_today_kwh": "3.4",
            "temperature_c": "21.2",
        }
    )

    assert cleaned["plant_id"] == "hochschule-pv-1"
    assert cleaned["power_w"] == 1200.5
    assert cleaned["data_source"] == "live"
    assert cleaned["is_test_data"] is False
