import json

import pytest

from solar_fetcher.fetcher import generate_sample_reading, load_test_readings, normalize_reading


def test_generate_sample_reading_contains_required_fields():
    reading = generate_sample_reading("campus-roof")

    assert reading["plant_id"] == "campus-roof"
    assert reading["power_w"] >= 0
    assert "timestamp" in reading
    assert reading["is_test_data"] is True
    assert reading["data_source"] == "TESTDATEN_GENERATOR"


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
    assert normalized["is_test_data"] is False


def test_normalize_reading_rejects_missing_fields():
    with pytest.raises(ValueError):
        normalize_reading({"timestamp": "2026-05-28T10:00:00Z"})


def test_load_test_readings_marks_all_entries(tmp_path):
    testdata_file = tmp_path / "solar_testdaten.json"
    testdata_file.write_text(
        json.dumps(
            {
                "readings": [
                    {
                        "timestamp": "2026-05-28T10:00:00Z",
                        "plant_id": "hochschule-pv-testanlage",
                        "power_w": 1000,
                        "energy_today_kwh": 2.5,
                        "temperature_c": 22.0,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    readings = load_test_readings(str(testdata_file))

    assert readings[0]["is_test_data"] is True
    assert readings[0]["data_source"] == "TESTDATEN_DATEI"
