# Solarenergie-Dashboard

Kleine Python-Anwendung fuer Solaranlagen-Daten einer Hochschule. Die App sammelt Messwerte, speichert sie, berechnet einfache Kennzahlen und stellt die Werte fuer ein Grafana-Dashboard bereit.

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

Eine kurze fachliche Erklaerung steht in `PROJEKT_ERKLAERUNG.md`.
Das Campusbild im Dashboard stammt aus Wikimedia Commons; die genaue Quelle steht in `dashboard/assets/README.md`.

## In PyCharm starten

1. Repository in PyCharm oeffnen: `File > Open` und diesen Projektordner auswaehlen.
2. Python Interpreter einrichten: `File > Settings > Project > Python Interpreter`.
3. Abhaengigkeiten installieren:

```powershell
py -m pip install -r requirements.txt
```

4. Oben rechts die Run Configuration `Solar Dashboard API` auswaehlen.
5. Gruenen Run-Button starten.

Danach laeuft die App direkt aus PyCharm:

- Dashboard: <http://localhost:8000>
- API-Dokumentation: <http://localhost:8000/docs>
- Metriken fuer Prometheus: <http://localhost:8000/metrics>

Die Hauptnavigation im Dashboard bleibt auf der grafischen Seite. Technische Rohdaten und API-Ansichten sind im Bereich `Technik` verlinkt.

Die Testdaten werden beim PyCharm-Start automatisch aus `testdata/solar_testdaten.json` geladen.

Wichtig: Die App startet in PyCharm ueber `main.py`. Docker ist dafuer nicht notwendig.

## In PyCharm testen

Oben rechts die Run Configuration `Solar Dashboard Tests` auswaehlen und starten.

Alternativ im PyCharm-Terminal:

```powershell
py -m pytest
```

## Mit Docker starten

```powershell
docker compose up --build
```

Danach sind die Dienste hier erreichbar:

- Dashboard: <http://localhost:8000>
- API-Dokumentation: <http://localhost:8000/docs>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>

Grafana Login:

- Benutzer: `admin`
- Passwort: `admin`

Das Dashboard liegt in Grafana im Ordner `Solar`.

## Testdaten

Damit das Dashboard sofort Daten anzeigen kann, werden beim Start markierte Testdaten geladen:

- Datei: `testdata/solar_testdaten.json`
- Markierung je Datensatz: `"is_test_data": true`
- Datenquelle je Datensatz: `"data_source": "TESTDATEN_DATEI"`
- Prometheus-Marker: `solar_test_data_active`

Die Testdaten sind synthetische Beispielwerte und keine echten Hochschuldaten.

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
