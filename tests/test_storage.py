from solar_storage.storage import (
    connect,
    initialize_database,
    insert_reading,
    latest_reading,
    list_readings,
)


def sample_reading(timestamp="2026-05-28T10:00:00+00:00"):
    return {
        "timestamp": timestamp,
        "plant_id": "hochschule-pv-1",
        "power_w": 1200.0,
        "energy_today_kwh": 4.5,
        "temperature_c": 23.0,
    }


def test_insert_and_list_readings():
    connection = connect(":memory:")
    initialize_database(connection)

    assert insert_reading(connection, sample_reading()) is True

    readings = list_readings(connection)
    assert len(readings) == 1
    assert readings[0]["power_w"] == 1200.0


def test_duplicate_reading_is_ignored():
    connection = connect(":memory:")
    initialize_database(connection)
    reading = sample_reading()

    assert insert_reading(connection, reading) is True
    assert insert_reading(connection, reading) is False
    assert latest_reading(connection)["plant_id"] == "hochschule-pv-1"
