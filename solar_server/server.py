"""FastAPI server that updates, stores, exposes, and exports solar metrics."""

from contextlib import asynccontextmanager
import logging
import threading
import time

from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest
from starlette.responses import Response

from solar_config.config import load_config, validate_config
from solar_fetcher.fetcher import fetch_reading, normalize_reading
from solar_processing.processing import build_dashboard_summary
from solar_storage.storage import (
    connect,
    initialize_database,
    insert_reading,
    latest_reading,
    list_readings,
)


logger = logging.getLogger(__name__)

CURRENT_POWER = Gauge("solar_current_power_w", "Current photovoltaic power in watts")
AVERAGE_POWER = Gauge("solar_average_power_w", "Average photovoltaic power in watts")
DAILY_ENERGY = Gauge("solar_daily_energy_kwh", "Daily photovoltaic energy in kWh")
TEMPERATURE = Gauge("solar_temperature_c", "Solar plant temperature in Celsius")


def collect_once(app: FastAPI) -> dict:
    """Fetch, normalize, store, and publish one solar reading."""

    raw = fetch_reading(app.state.config.data_source_url)
    reading = normalize_reading(raw)
    insert_reading(app.state.connection, reading)
    update_prometheus_metrics(list_readings(app.state.connection, limit=500))
    return reading


def update_prometheus_metrics(readings: list[dict]) -> None:
    """Update Prometheus gauges from current stored readings."""

    summary = build_dashboard_summary(readings)
    latest = summary["latest"]
    AVERAGE_POWER.set(summary["average_power_w"])
    DAILY_ENERGY.set(summary["energy_today_kwh"])
    if latest:
        CURRENT_POWER.set(float(latest["power_w"]))
        TEMPERATURE.set(float(latest["temperature_c"]))


def polling_loop(app: FastAPI, stop_event: threading.Event) -> None:
    """Run the recurring data collection loop."""

    while not stop_event.wait(app.state.config.fetch_interval_seconds):
        try:
            collect_once(app)
        except Exception:
            logger.exception("failed to collect solar reading")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start storage and background polling for the API process."""

    config = validate_config(load_config())
    connection = connect(config.database_path)
    initialize_database(connection)
    app.state.config = config
    app.state.connection = connection

    try:
        collect_once(app)
    except Exception:
        logger.exception("initial solar collection failed")

    stop_event = threading.Event()
    thread = threading.Thread(target=polling_loop, args=(app, stop_event), daemon=True)
    thread.start()
    app.state.stop_event = stop_event
    app.state.polling_thread = thread

    try:
        yield
    finally:
        stop_event.set()
        thread.join(timeout=2)
        connection.close()


app = FastAPI(title="Hochschule Solar Dashboard", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint for Docker and monitoring."""

    return {"status": "ok"}


@app.post("/collect")
def collect_now() -> dict:
    """Manually collect one fresh reading."""

    return collect_once(app)


@app.get("/readings")
def readings(limit: int = 100) -> list[dict]:
    """Return recent stored readings."""

    bounded_limit = max(1, min(limit, 1000))
    return list_readings(app.state.connection, limit=bounded_limit)


@app.get("/latest")
def latest() -> dict:
    """Return the latest stored reading."""

    return latest_reading(app.state.connection) or {}


@app.get("/summary")
def summary(limit: int = 500) -> dict:
    """Return prepared values for a dashboard."""

    bounded_limit = max(1, min(limit, 5000))
    data = list_readings(app.state.connection, limit=bounded_limit)
    return build_dashboard_summary(data)


@app.get("/metrics")
def metrics() -> Response:
    """Expose Prometheus metrics."""

    update_prometheus_metrics(list_readings(app.state.connection, limit=500))
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
