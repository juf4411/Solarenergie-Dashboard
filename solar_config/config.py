"""Configuration helpers for the solar dashboard service."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Runtime settings loaded from environment variables."""

    data_source_url: str | None
    database_path: str
    fetch_interval_seconds: int
    test_data_path: str | None
    seed_test_data: bool


def _optional_env(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> AppConfig:
    """Load application configuration from environment variables."""

    return AppConfig(
        data_source_url=_optional_env("SOLAR_DATA_SOURCE_URL"),
        database_path=os.getenv("SOLAR_DATABASE_PATH", "data/solar.db"),
        fetch_interval_seconds=int(os.getenv("SOLAR_FETCH_INTERVAL_SECONDS", "60")),
        test_data_path=_optional_env("SOLAR_TEST_DATA_PATH") or "testdata/solar_testdaten.json",
        seed_test_data=_env_bool("SOLAR_SEED_TEST_DATA", True),
    )


def validate_config(config: AppConfig) -> AppConfig:
    """Validate configuration values and return the unchanged config."""

    if config.fetch_interval_seconds <= 0:
        raise ValueError("SOLAR_FETCH_INTERVAL_SECONDS must be greater than zero")
    if not config.database_path.strip():
        raise ValueError("SOLAR_DATABASE_PATH must not be empty")
    return config
