# Projekt-Erklaerung

Diese Datei fasst zusammen, wie das Projekt aufgebaut ist und welche Idee hinter den einzelnen Dateien steckt. Sie ist als Lern- und Abgabehilfe gedacht.

## Grundidee

Die Anwendung sammelt Messwerte einer Solaranlage, speichert sie lokal und bereitet sie fuer ein Dashboard auf. Wenn noch keine echten Hochschuldaten vorhanden sind, werden markierte Testdaten verwendet. Dadurch kann man die App direkt starten und im eingebauten Dashboard Kurven und Werte sehen.

Der Datenfluss ist:

1. Daten holen oder Testdaten verwenden
2. Daten pruefen und in ein einheitliches Format bringen
3. Daten in SQLite speichern
4. Kennzahlen berechnen, zum Beispiel Mittelwert
5. Daten ueber API, eigenes Dashboard und Prometheus bereitstellen

## Dashboard, Prometheus und Grafana

Prometheus und Grafana sind nicht das Gleiche.

Prometheus sammelt Messwerte. In diesem Projekt ruft Prometheus den Endpunkt `/metrics` ab und speichert technische Zeitreihen wie aktuelle Leistung, Durchschnittsleistung und Temperatur.

Grafana visualisiert solche Zeitreihen. Es ist praktisch, wenn man Monitoring mit Docker zeigen moechte.

Fuer die eigentliche Projektvorfuehrung ist aber das eingebaute Dashboard unter `http://localhost:8000` praktischer. Es ist direkt in der App enthalten, laeuft in PyCharm ohne Docker und zeigt die Testdaten sofort grafisch an.

## Warum die Module getrennt sind

Die Vorgabe war, mehrere einzelne Python-Dateien bzw. Module zu verwenden. Deshalb ist die Logik bewusst aufgeteilt:

- `solar_config/config.py`: liest Einstellungen aus Umgebungsvariablen
- `solar_fetcher/fetcher.py`: holt Daten oder erzeugt Testdaten
- `solar_storage/storage.py`: speichert Messwerte in SQLite
- `solar_processing/processing.py`: berechnet Werte fuer das Dashboard
- `solar_server/server.py`: stellt API-Endpunkte und Prometheus-Metriken bereit

So kann man jedes Modul einzeln testen und erklaeren.

## Testdaten

Die Datei `testdata/solar_testdaten.json` enthaelt synthetische Beispielwerte. Jeder Datensatz ist markiert:

```json
"is_test_data": true,
"data_source": "TESTDATEN_DATEI"
```

Diese Markierung ist wichtig, damit klar ist: Das sind keine echten Daten der Hochschule.

## Wichtige API-Endpunkte

- `/health`: einfacher Test, ob der Server laeuft
- `/readings`: gespeicherte Messwerte
- `/latest`: neuester Messwert
- `/summary`: vorbereitete Kennzahlen fuer das Dashboard
- `/metrics`: Prometheus-Metriken fuer optionales Monitoring

## Was man in der Abgabe erklaeren kann

- SQLite wurde gewaehlt, weil es ohne extra Datenbankserver lokal funktioniert.
- Das eingebaute Dashboard ist die praktische Hauptansicht fuer die Vorfuehrung.
- Prometheus liest regelmaessig die Metriken vom Server, wenn Docker Compose genutzt wird.
- Grafana kann diese Metriken zusaetzlich als Monitoring-Dashboard visualisieren.
- Docker Compose startet App, Prometheus und Grafana zusammen.
- PyCharm kann die App ueber `main.py` direkt starten.
- Die Tests pruefen die Funktionen in den einzelnen Modulen.

## Typische Aenderungen fuer echte Daten

Wenn spaeter echte Daten vorhanden sind, kann man `SOLAR_DATA_SOURCE_URL` setzen. Dann fragt die App diese HTTP-Quelle ab. Das erwartete Format steht in der README.

Wenn keine Testdaten geladen werden sollen:

```powershell
$env:SOLAR_SEED_TEST_DATA="false"
```

Dann startet die App ohne die Datei `testdata/solar_testdaten.json`.
