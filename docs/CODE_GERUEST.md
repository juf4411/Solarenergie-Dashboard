# Code-Geruest

Das Projekt ist als modulares Code-Geruest aufgebaut. Jedes Modul hat eine klare Aufgabe und kann einzeln getestet werden.

## Modulstruktur

| Modul | Aufgabe | Wichtige Funktionen |
| --- | --- | --- |
| `solar_config/config.py` | Konfiguration laden und pruefen | `load_config`, `validate_config` |
| `solar_fetcher/fetcher.py` | Daten aus URL holen oder Testdaten laden | `fetch_reading`, `load_test_readings` |
| `solar_cleaning/cleaning.py` | Rohdaten bereinigen | `clean_reading`, `parse_timestamp`, `parse_float` |
| `solar_storage/storage.py` | Daten speichern und lesen | `connect`, `insert_reading`, `list_readings` |
| `solar_processing/processing.py` | Kennzahlen berechnen | `calculate_average_power`, `build_dashboard_summary` |
| `solar_server/server.py` | Server und API bereitstellen | `collect_once`, `summary`, `metrics` |

## Stub-Gedanke

Die Module sind so geschnitten, dass sie zuerst als einfache Stub-Dateien mit Funktionsnamen angelegt und danach schrittweise implementiert werden koennen. Beispiel fuer den Entwicklungsablauf:

1. Datei und Funktionssignaturen anlegen
2. passenden Test schreiben
3. Funktion implementieren
4. Test ausfuehren
5. Linting/Formatting ausfuehren

Dadurch bleibt nachvollziehbar, welche Aufgabe jedes Modul im Gesamtsystem uebernimmt.
