"""SQLite persistence for normalized solar readings."""

from collections.abc import Iterable
from pathlib import Path
import sqlite3
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS solar_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    plant_id TEXT NOT NULL,
    power_w REAL NOT NULL,
    energy_today_kwh REAL NOT NULL,
    temperature_c REAL NOT NULL,
    UNIQUE(timestamp, plant_id)
);
"""


def connect(database_path: str) -> sqlite3.Connection:
    """Open a SQLite connection and ensure its parent directory exists."""

    if database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    """Create required database tables."""

    connection.execute(SCHEMA)
    connection.commit()


def insert_reading(connection: sqlite3.Connection, reading: dict[str, Any]) -> bool:
    """Insert one reading. Return True when a new row was written."""

    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO solar_readings
        (timestamp, plant_id, power_w, energy_today_kwh, temperature_c)
        VALUES (:timestamp, :plant_id, :power_w, :energy_today_kwh, :temperature_c)
        """,
        reading,
    )
    connection.commit()
    return cursor.rowcount > 0


def list_readings(connection: sqlite3.Connection, limit: int = 100) -> list[dict[str, Any]]:
    """Return recent readings ordered from newest to oldest."""

    rows: Iterable[sqlite3.Row] = connection.execute(
        """
        SELECT timestamp, plant_id, power_w, energy_today_kwh, temperature_c
        FROM solar_readings
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )
    return [dict(row) for row in rows]


def latest_reading(connection: sqlite3.Connection) -> dict[str, Any] | None:
    """Return the newest reading or None if the database is empty."""

    row = connection.execute(
        """
        SELECT timestamp, plant_id, power_w, energy_today_kwh, temperature_c
        FROM solar_readings
        ORDER BY timestamp DESC
        LIMIT 1
        """
    ).fetchone()
    return dict(row) if row else None
