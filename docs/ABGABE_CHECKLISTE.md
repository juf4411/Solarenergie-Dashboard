# Abgabe-Checkliste

| Vorgabe | Umsetzung im Repository |
| --- | --- |
| Git Repository | GitHub Repository `juf4411/Solarenergie-Dashboard` |
| Backend-Server | `solar_server/server.py` |
| Code-Geruest aus Stub-Struktur | `docs/CODE_GERUEST.md`, Module `solar_*` |
| PV-Werte aus URL holen | `solar_fetcher/fetcher.py`, Variable `SOLAR_DATA_SOURCE_URL` |
| Data Cleaning Modul | `solar_cleaning/cleaning.py` |
| Data Storage Modul | `solar_storage/storage.py` |
| Berechnungsmodul | `solar_processing/processing.py` |
| Frontend Dashboard | `dashboard/index.html`, `dashboard/styles.css`, `dashboard/app.js` |
| Mock-up/Testdaten | `testdata/solar_testdaten.json` |
| Unit- und Integrationtests | Ordner `tests` |
| Directory Struktur | getrennte Ordner `solar_*`, `dashboard`, `docs`, `testdata` |
| Abhaengigkeitskontrolle | `pyproject.toml`, `requirements.txt` |
| Versionskontrolle | Git-Historie mit thematischen Commits |
| CI/CD readiness | `.github/workflows/ci.yml` |
| Containerization readiness | `Dockerfile`, `docker-compose.yml` |
| Prometheus/Grafana | `prometheus`, `grafana` |
| Dokumentation | `README.md`, `PROJEKT_ERKLAERUNG.md`, `docs` |
| Dashboard-Grafik | `docs/dashboard-grafik.svg` |
| Metrik-Spezifikation | `docs/DASHBOARD_SPEZIFIKATION.md` |
| Aufgabenverteilung | `docs/AUFGABENVERTEILUNG.md` |
| Formatting/Linting | Ruff-Konfiguration in `pyproject.toml` |

## Befehle fuer die Abgabepruefung

```powershell
py -m pip install -r requirements.txt
py -m ruff format --check .
py -m ruff check .
py -m pytest
py main.py
```
