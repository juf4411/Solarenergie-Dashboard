import pytest

from solar_config.config import AppConfig, load_config, validate_config


def test_load_config_uses_defaults(monkeypatch):
    monkeypatch.delenv("SOLAR_DATA_SOURCE_URL", raising=False)
    monkeypatch.delenv("SOLAR_DATABASE_PATH", raising=False)
    monkeypatch.delenv("SOLAR_FETCH_INTERVAL_SECONDS", raising=False)

    config = load_config()

    assert config.data_source_url is None
    assert config.database_path == "data/solar.db"
    assert config.fetch_interval_seconds == 60


def test_validate_config_rejects_invalid_interval():
    config = AppConfig(
        data_source_url=None,
        database_path="data/solar.db",
        fetch_interval_seconds=0,
    )

    with pytest.raises(ValueError):
        validate_config(config)
