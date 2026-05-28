from solar_processing.processing import (
    build_dashboard_summary,
    calculate_average_power,
    calculate_total_energy,
    format_reading_for_display,
)


READINGS = [
    {
        "timestamp": "2026-05-28T11:00:00+00:00",
        "plant_id": "hochschule-pv-1",
        "power_w": 300.0,
        "energy_today_kwh": 2.5,
        "temperature_c": 20.0,
    },
    {
        "timestamp": "2026-05-28T10:00:00+00:00",
        "plant_id": "hochschule-pv-1",
        "power_w": 100.0,
        "energy_today_kwh": 1.5,
        "temperature_c": 19.5,
    },
]


def test_dashboard_calculations():
    assert calculate_average_power(READINGS) == 200.0
    assert calculate_total_energy(READINGS) == 2.5


def test_build_dashboard_summary_uses_latest_first():
    summary = build_dashboard_summary(READINGS)

    assert summary["reading_count"] == 2
    assert summary["latest"]["timestamp"] == "2026-05-28T11:00:00+00:00"
    assert summary["average_power_w"] == 200.0


def test_format_reading_for_display():
    formatted = format_reading_for_display(READINGS[0])

    assert formatted["power"] == "300.00 W"
    assert formatted["energy_today"] == "2.500 kWh"
