# Dashboard Solar

Portable Python-App fuer Solaranlagen-Daten einer Hochschule.

## Inhalt

- 5 Python-Module in eigenen Ordnern:
  - `solar_config/config.py`
  - `solar_fetcher/fetcher.py`
  - `solar_storage/storage.py`
  - `solar_processing/processing.py`
  - `solar_server/server.py`
- 5 zugehoerige Testdateien im Ordner `tests`
- Docker Compose mit App, Prometheus und Grafana
- SQLite-Speicherung der Messwerte
- Prometheus-Metriken fuer Grafana

## Lokal testen

```powershell
python -m pip install -e ".[test]"
pytest
```

## Mit Docker starten

```powershell
docker compose up --build
```

Danach sind die Dienste hier erreichbar:

- App/API: <http://localhost:8000>
- API-Dokumentation: <http://localhost:8000/docs>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>

Grafana Login:

- Benutzer: `admin`
- Passwort: `admin`

Das Dashboard liegt in Grafana im Ordner `Solar`.

## Eigene Datenquelle verwenden

Ohne externe Datenquelle erzeugt die App Beispielwerte. Fuer echte Hochschuldaten kann eine JSON-HTTP-Quelle konfiguriert werden:

```powershell
$env:SOLAR_DATA_SOURCE_URL="https://example.edu/solar/latest.json"
```

Erwartetes JSON-Format:

```json
{
  "timestamp": "2026-05-28T10:00:00Z",
  "plant_id": "hochschule-pv-1",
  "power_w": 1234.5,
  "energy_today_kwh": 5.25,
  "temperature_c": 24.1
}
```
