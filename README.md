# Pharmacy Accessibility Switzerland
## Geomarketing-Analyse zur Erreichbarkeit von Apotheken in der Schweiz

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostGIS](https://img.shields.io/badge/PostGIS-3.6-green)
![ZHAW](https://img.shields.io/badge/ZHAW-EGM_FS2026-red)
![License](https://img.shields.io/badge/License-MIT-orange)

## Zentrale Ergebnisse

| Kennzahl | Wert |
|----------|------|
| Apotheken in CH (OSM) | 1640 |
| Analysierte Gemeinden | 2123 |
| Gemeinden ohne eigene Apotheke | 1562 (74%) |
| Bevoelkerung > 5km von Apotheke | 832482 (9.15%) |
| Bevoelkerung > 10km von Apotheke | 127106 (1.40%) |
| Schlechtestversorgte Gemeinde | Rheinwald GR (23.2 km) |
| Best versorgter Kanton Median | Basel-Stadt BS (503 m) |
| Schlechtester Kanton Median | Uri UR (8829 m) |
| Morans I Apothekendichte | 0.361 p=0.001 signifikant |

## Projektstruktur
```
pharmacy-accessibility-ch/
??? data/
?   ??? raw/
?   ?   ??? kantone_ch_lv95.geojson        # Kantone (im Repo)
?   ?   ??? stadtquartiere_zuerich.geojson # 34 Quartiere ZH (im Repo)
?   ?   # Grosse Dateien (>60MB) nicht im Repo - via NB01 herunterladen
?   ??? processed/
?       ??? pharmacies_ch.geojson          # 1640 Apotheken (im Repo)
?       ??? stadtquartiere_zuerich.geojson # Quartiere ZH (im Repo)
?       ??? isochrones_5min_car_sample.geojson # ORS Stichprobe (im Repo)
?       ??? 05_*.csv                       # Auswertungen (im Repo)
?       # gemeinden_ch.geojson (61MB) und plz_ch.geojson (113MB) nicht im Repo
??? notebooks/
?   ??? 01_data_acquisition.ipynb   # Datenbeschaffung OSM, swisstopo, BFS
?   ??? 02_postgis_analysis.ipynb   # ST_Within, ST_Distance, Choropleth
?   ??? 03_isochrones_ors.ipynb     # ORS Fahrzeitanalyse (API Key noetig)
?   ??? 04_spatial_analysis.ipynb   # Morans I, LISA, Zuerich, Kantone
?   ??? 05_population_coverage.ipynb # Bevoelkerungsabdeckung
?   ??? 06_visualization.ipynb      # Finale Karten fuer Praesentation
??? outputs/maps/                   # 13 generierte Karten (PNG)
??? .env.example                    # Vorlage fuer API Keys
??? requirements.txt
??? README.md
```

## Setup

### 1. Repo klonen
```powershell
git clone https://github.com/gsparty/pharmacy-accessibility-ch.git
cd pharmacy-accessibility-ch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. API Key setzen
```powershell
Copy-Item .env.example .env
# .env oeffnen und ORS_API_KEY eintragen
# Kostenloser Key: https://openrouteservice.org/dev/#/signup
```

### 3. PostgreSQL + PostGIS einrichten
PostgreSQL 16 + PostGIS 3.6 muss lokal installiert sein.
```powershell
$env:PGPASSWORD = "postgres"
psql -U postgres -c "CREATE DATABASE pharmacy_ch;"
psql -U postgres -d pharmacy_ch -c "CREATE EXTENSION postgis CASCADE;"
```

### 4. Notebooks ausfuehren
Notebooks der Reihe nach ausfuehren - NB01 laedt alle grossen Geodaten herunter.
```powershell
jupyter nbconvert --to notebook --execute notebooks\01_data_acquisition.ipynb --output 01_data_acquisition.ipynb --output-dir notebooks --ExecutePreprocessor.timeout=300
```

### Hinweis fuer Teammitglieder
- `data/raw/` und `data/processed/` enthalten nur kleine Hilfsdateien im Repo
- Grosse Geodaten (Gemeinden 61MB, PLZ 113MB) werden durch NB01 automatisch heruntergeladen
- `.env` ist nicht im Repo - ORS API Key separat beantragen (kostenlos)

## Datenquellen

| Datei | Quelle | Inhalt | Im Repo |
|-------|--------|--------|---------|
| pharmacies_ch.geojson | OpenStreetMap / Overpass API | 1640 Apotheken | Ja (0.4MB) |
| gemeinden_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | 2123 Gemeinden | Nein (62MB) |
| plz_ch_lv95.geojson | swisstopo Ortschaftenverzeichnis | 4073 PLZ | Nein (113MB) |
| stadtquartiere_zuerich.geojson | Stadt Zuerich OGD | 34 Quartiere | Ja (2.1MB) |
| kantone_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | Kantone | Ja (2.6MB) |

Projektion: LV95 EPSG:2056 - Schweizer Landeskoordinaten, Distanzen in Metern

## Methoden

- GeoPandas & Shapely: Raeumliche Datenverarbeitung in Python
- PostgreSQL/PostGIS: ST_Within, ST_Distance, ST_DWithin, GIST-Indizes
- OpenRouteService API: Fahrzeitanalyse und Isochronen (5/10/15 Min)
- PySAL/ESDA: Spatial Autocorrelation (Morans I = 0.361, p = 0.001)
- Matplotlib: Choropleth-Karten, Boxplots, Histogramme

## Generierte Karten (outputs/maps/)

| Datei | Inhalt |
|-------|--------|
| 01_apotheken_uebersicht.png | Alle 1640 Apotheken auf CH-Karte |
| 02_distanz_apotheke.png | Choropleth: Distanz zur naechsten Apotheke |
| 03_einzeltest_isochrone.png | ORS: Zu Fuss vs. Auto Vergleich |
| 03_isochronen_5min_auto.png | Isochronen Stichprobe 20 Apotheken |
| 04_lisa_cluster.png | LISA Cluster Map (Morans I = 0.361) |
| 04_boxplot_kantone.png | Distanz nach Kanton sortiert nach Median |
| 04_zuerich_quartiere.png | Zuerich: Apotheken pro Stadtquartier |
| 05_bevoelkerungsabdeckung.png | Bevoelkerungsanteil nach Distanz |
| 05_unterversorgte_gemeinden.png | Karte unterversorgter Gemeinden |
| 06_hauptkarte_distanz.png | Finale Hauptkarte fuer Praesentation |
| 06_distanz_histogramm.png | Bevoelkerungsverteilung nach Distanz |

## Quellen

- OpenStreetMap Contributors (2024). Overpass API. https://overpass-api.de
- swisstopo (2026). swissBOUNDARIES3D 2026. https://data.geo.admin.ch
- Stadt Zuerich (2024). Stadtquartiere OGD. https://data.stadt-zuerich.ch
- OpenRouteService (2024). Isochrones API. https://openrouteservice.org

## Gruppe

ZHAW - Modul: Einsatz von Geodaten im Marketing (EGM) - FS2026