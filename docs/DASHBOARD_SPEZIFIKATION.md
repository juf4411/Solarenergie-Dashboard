# Dashboard-Spezifikation

Diese Spezifikation beschreibt, welche Inhalte im PV-Dashboard angezeigt werden.

Eine schematische Grafik des Dashboards liegt in `docs/dashboard-grafik.svg`.

## Hauptansicht

URL: `http://localhost:8000`

Die Hauptansicht zeigt eine kompakte Uebersicht der PV-Anlage mit Testdaten oder echten Daten aus einer konfigurierten URL.

## KPIs

| KPI | Beschreibung | Einheit | Datenbasis |
| --- | --- | --- | --- |
| Aktuelle Leistung | Neuester gespeicherter Leistungswert | W | `power_w` aus `/latest` |
| Mittelwert | Durchschnitt der gespeicherten Leistungswerte | W | `/summary` |
| Energie heute | Hoechster Tagesenergie-Wert des aktuellen Datensatzes | kWh | `energy_today_kwh` |
| Temperatur | Neuester Temperaturwert der Anlage | C | `temperature_c` |
| Datenstatus | Kennzeichnung, ob Testdaten oder Echtdaten verwendet werden | Text | `is_test_data` |

## Grafiken

| Grafik | Beschreibung | Quelle |
| --- | --- | --- |
| Tagesverlauf Leistung | Liniendiagramm der PV-Leistung ueber die Zeit | `/readings` |
| Ertrag je Messpunkt | Liniendiagramm der Tagesenergie ueber die Zeit | `/readings` |
| Auslastung | Donut-Anzeige auf Basis der aktuellen Leistung gegen 5.500 W Referenzleistung | `/summary` |
| Messwert-Tabelle | Tabelle der letzten Messwerte mit Zeit, Leistung und Energie | `/readings` |

## Technische Datenquellen

| Endpoint | Aufgabe |
| --- | --- |
| `/` | Grafisches Dashboard |
| `/health` | einfacher Health Check |
| `/readings` | gespeicherte Messwerte als JSON |
| `/latest` | neuester Messwert |
| `/summary` | berechnete Kennzahlen fuer das Dashboard |
| `/metrics` | Prometheus-Metriken |
| `/docs` | automatische API-Dokumentation |

## Testdaten

Die Mock-up-Daten liegen in `testdata/solar_testdaten.json`. Jeder Datensatz ist markiert:

```json
"is_test_data": true,
"data_source": "TESTDATEN_DATEI"
```

Damit ist in der Vorfuehrung klar erkennbar, dass keine echten Hochschuldaten verwendet werden.
