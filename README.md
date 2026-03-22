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
| Bevölkerung > 5km von Apotheke | 832'482 (9.15%) |
| Bevölkerung > 10km von Apotheke | 127'106 (1.40%) |
| Schlechtestversorgte Gemeinde | Rheinwald GR (23.2 km) |
| Best versorgter Kanton (Median) | Basel-Stadt BS (503 m) |
| Schlechtester Kanton (Median) | Uri UR (8829 m) |
| Moran's I (Apothekendichte) | 0.361, p=0.001 (signifikant) |

## Projektstruktur

```
pharmacy-accessibility-ch/
├── data/
│   ├── raw/
│   │   ├── kantone_ch_lv95.geojson         # Kantone (im Repo, 2.6MB)
│   │   └── stadtquartiere_zuerich.geojson  # 34 Quartiere ZH (im Repo, 2.1MB)
│   │   # Grosse Dateien (>60MB) nicht im Repo – via NB01 herunterladen
│   └── processed/
│       ├── pharmacies_ch.geojson           # 1640 Apotheken (im Repo, 0.4MB)
│       ├── stadtquartiere_zuerich.geojson  # Quartiere ZH (im Repo)
│       ├── isochrones_5min_car_sample.geojson  # ORS Stichprobe (im Repo)
│       └── 05_*.csv                        # Auswertungen (im Repo)
│       # gemeinden_ch.geojson (61MB) und plz_ch.geojson (113MB) → via NB01
├── notebooks/
│   ├── 01_data_acquisition.ipynb    # Datenbeschaffung OSM, swisstopo, BFS
│   ├── 02_postgis_analysis.ipynb    # ST_Within, ST_Distance, Choropleth
│   ├── 03_isochrones_ors.ipynb      # ORS Fahrzeitanalyse (API Key nötig)
│   ├── 04_spatial_analysis.ipynb    # Moran's I, LISA, Zürich, Kantone
│   ├── 05_population_coverage.ipynb # Bevölkerungsabdeckung
│   └── 06_visualization.ipynb       # Finale Karten für Präsentation
├── outputs/maps/                    # 13 generierte Karten (PNG)
├── .env.example                     # Vorlage für API Keys
├── requirements.txt
└── README.md
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
# .env öffnen und ORS_API_KEY eintragen
# Kostenloser Key: https://openrouteservice.org/dev/#/signup
```

### 3. PostgreSQL + PostGIS einrichten
PostgreSQL 16 + PostGIS 3.6 muss lokal installiert sein.
```powershell
psql -U postgres -c "CREATE DATABASE pharmacy_ch;"
psql -U postgres -d pharmacy_ch -c "CREATE EXTENSION postgis CASCADE;"
```

### 4. Notebooks ausführen
Notebooks der Reihe nach ausführen – NB01 lädt alle grossen Geodaten herunter.
```powershell
jupyter nbconvert --to notebook --execute notebooks\01_data_acquisition.ipynb --output 01_data_acquisition.ipynb --output-dir notebooks --ExecutePreprocessor.timeout=300
```

### Hinweis für Teammitglieder
- `data/raw/` und `data/processed/` enthalten nur kleine Hilfsdateien im Repo
- Grosse Geodaten (Gemeinden 61MB, PLZ 113MB) werden durch NB01 automatisch heruntergeladen
- `.env` ist nicht im Repo – ORS API Key separat beantragen (kostenlos, openrouteservice.org)
- PostgreSQL muss lokal laufen für Notebook 02

## Datenquellen

| Datei | Quelle | Inhalt | Im Repo |
|-------|--------|--------|---------|
| pharmacies_ch.geojson | OpenStreetMap / Overpass API | 1640 Apotheken | ✅ 0.4MB |
| gemeinden_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | 2123 Gemeinden | ❌ 62MB |
| plz_ch_lv95.geojson | swisstopo Ortschaftenverzeichnis | 4073 PLZ | ❌ 113MB |
| stadtquartiere_zuerich.geojson | Stadt Zürich OGD | 34 Quartiere | ✅ 2.1MB |
| kantone_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | Kantone | ✅ 2.6MB |

**Projektion:** LV95 (EPSG:2056) – Schweizer Landeskoordinaten, Distanzen in Metern

## Methoden

- **GeoPandas & Shapely**: Räumliche Datenverarbeitung in Python
- **PostgreSQL/PostGIS**: ST_Within, ST_Distance, ST_DWithin, GIST-Indizes
- **OpenRouteService API**: Fahrzeitanalyse und Isochronen (5/10/15 Min)
- **PySAL/ESDA**: Spatial Autocorrelation (Moran's I = 0.361, p = 0.001)
- **Matplotlib**: Choropleth-Karten, Boxplots, Histogramme

## Generierte Karten (`outputs/maps/`)

| Datei | Inhalt |
|-------|--------|
| 01_apotheken_uebersicht.png | Alle 1640 Apotheken auf CH-Karte |
| 02_distanz_apotheke.png | Choropleth: Distanz zur nächsten Apotheke |
| 03_einzeltest_isochrone.png | ORS: Zu Fuss vs. Auto Vergleich |
| 03_isochronen_5min_auto.png | Isochronen Stichprobe 20 Apotheken |
| 04_lisa_cluster.png | LISA Cluster Map (Moran's I = 0.361) |
| 04_boxplot_kantone.png | Distanz nach Kanton, sortiert nach Median |
| 04_zuerich_quartiere.png | Zürich: Apotheken pro Stadtquartier |
| 05_bevoelkerungsabdeckung.png | Bevölkerungsanteil nach Distanz |
| 05_unterversorgte_gemeinden.png | Karte unterversorgter Gemeinden |
| 06_hauptkarte_distanz.png | Finale Hauptkarte für Präsentation |
| 06_distanz_histogramm.png | Bevölkerungsverteilung nach Distanz |

## Quellen

- OpenStreetMap Contributors (2024). *Overpass API*. https://overpass-api.de
- swisstopo (2026). *swissBOUNDARIES3D 2026*. https://data.geo.admin.ch
- Stadt Zürich (2024). *Stadtquartiere OGD*. https://data.stadt-zuerich.ch
- OpenRouteService (2024). *Isochrones API*. https://openrouteservice.org

## Gruppe

ZHAW – Modul: Einsatz von Geodaten im Marketing (EGM) – FS2026
