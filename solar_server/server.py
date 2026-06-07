"""FastAPI server that updates, stores, exposes, and exports solar metrics."""

import logging
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest
from starlette.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles

from solar_config.config import load_config, validate_config
from solar_fetcher.fetcher import fetch_reading, load_test_readings, normalize_reading
from solar_processing.processing import build_dashboard_summary
from solar_storage.storage import (
    connect,
    initialize_database,
    insert_reading,
    latest_reading,
    list_readings,
)

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

CURRENT_POWER = Gauge("solar_current_power_w", "Current photovoltaic power in watts")
AVERAGE_POWER = Gauge("solar_average_power_w", "Average photovoltaic power in watts")
DAILY_ENERGY = Gauge("solar_daily_energy_kwh", "Daily photovoltaic energy in kWh")
TEMPERATURE = Gauge("solar_temperature_c", "Solar plant temperature in Celsius")
TEST_DATA_ACTIVE = Gauge(
    "solar_test_data_active", "1 when the latest solar reading is marked as test data"
)


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
    TEST_DATA_ACTIVE.set(1 if summary["latest_is_test_data"] else 0)
    if latest:
        CURRENT_POWER.set(float(latest["power_w"]))
        TEMPERATURE.set(float(latest["temperature_c"]))


def seed_test_data(app: FastAPI) -> int:
    """Insert marked test data so dashboards have values immediately after startup."""

    if not app.state.config.seed_test_data or not app.state.config.test_data_path:
        return 0
    if not Path(app.state.config.test_data_path).exists():
        logger.warning("test data file not found: %s", app.state.config.test_data_path)
        return 0

    inserted_count = 0
    for raw_reading in load_test_readings(app.state.config.test_data_path):
        reading = normalize_reading(raw_reading)
        if insert_reading(app.state.connection, reading):
            inserted_count += 1
    update_prometheus_metrics(list_readings(app.state.connection, limit=500))
    return inserted_count


def polling_loop(app: FastAPI, stop_event: threading.Event) -> None:
    """Run the recurring data collection loop."""

    # Der Thread holt im Hintergrund regelmaessig neue Messwerte.
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
        seed_test_data(app)
        collect_once(app)
    except Exception:
        logger.exception("initial solar collection failed")

    # FastAPI laeuft weiter, waehrend dieser Thread neue Werte sammelt.
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
app.mount("/dashboard", StaticFiles(directory=DASHBOARD_DIR), name="dashboard")


@app.get("/")
def dashboard() -> FileResponse:
    """Return the visual dashboard page."""

    return FileResponse(DASHBOARD_DIR / "index.html")


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
