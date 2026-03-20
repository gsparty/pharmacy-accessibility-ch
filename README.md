# Pharmacy Accessibility Switzerland
## Geomarketing-Analyse zur Erreichbarkeit von Apotheken in der Schweiz

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostGIS](https://img.shields.io/badge/PostGIS-3.6-green)
![ZHAW](https://img.shields.io/badge/ZHAW-EGM_FS2026-red)

## Zentrale Ergebnisse

| Kennzahl | Wert |
|----------|------|
| Apotheken in CH | 1640 |
| Analysierte Gemeinden | 2123 |
| Gemeinden ohne eigene Apotheke | 1562 (74%) |
| Bevoelkerung > 5km von Apotheke | 832'482 (9.15%) |
| Bevoelkerung > 10km von Apotheke | 127'106 (1.40%) |
| Schlechteste Versorgung | Rheinwald GR (23.2 km) |
| Best versorgter Kanton (Median) | Basel-Stadt (503 m) |
| Schlechtester Kanton (Median) | Uri (8829 m) |
| Moran's I (Apothekendichte) | 0.361 (p=0.001, signifikant) |

## Projektstruktur

```
pharmacy-accessibility-ch/
├── data/
│   ├── raw/              # Originaldaten (nicht in Git)
│   └── processed/        # Bereinigte Geodaten (nicht in Git)
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_postgis_analysis.ipynb
│   ├── 03_isochrones_ors.ipynb
│   ├── 04_spatial_analysis.ipynb
│   ├── 05_population_coverage.ipynb
│   └── 06_visualization.ipynb
├── outputs/maps/         # 13 generierte Karten
├── scripts/              # Hilfsskripte
├── sql/                  # PostGIS SQL Queries
├── .env.example
└── requirements.txt
```

## Setup

```powershell
git clone https://github.com/gsparty/pharmacy-accessibility-ch.git
cd pharmacy-accessibility-ch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### PostgreSQL + PostGIS
```powershell
$env:PGPASSWORD = "postgres"
psql -U postgres -c "CREATE DATABASE pharmacy_ch;"
psql -U postgres -d pharmacy_ch -c "CREATE EXTENSION postgis CASCADE;"
```

### API Key
```powershell
Copy-Item .env.example .env
# .env oeffnen und ORS_API_KEY eintragen
# Kostenloser Key: https://openrouteservice.org/dev/#/signup
```

### Notebooks ausfuehren
```powershell
jupyter nbconvert --to notebook --execute notebooks\NB.ipynb --output NB.ipynb --output-dir notebooks --ExecutePreprocessor.timeout=300
```

## Datenquellen

| Datei | Quelle | Inhalt |
|-------|--------|--------|
| pharmacies_ch.geojson | OpenStreetMap / Overpass API | 1640 Apotheken |
| gemeinden_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | 2123 Gemeinden |
| plz_ch_lv95.geojson | swisstopo Ortschaftenverzeichnis | 4073 PLZ |
| stadtquartiere_zuerich.geojson | Stadt Zuerich OGD | 34 Quartiere |

**Projektion:** LV95 (EPSG:2056)

## Methoden

- **GeoPandas & Shapely**: Raeumliche Datenverarbeitung
- **PostgreSQL/PostGIS**: ST_Within, ST_Distance, ST_DWithin
- **OpenRouteService API**: Fahrzeitanalyse und Isochronen
- **PySAL/ESDA**: Spatial Autocorrelation (Moran's I, LISA)
- **Matplotlib**: Choropleth-Karten, Boxplots, Histogramme

## Wichtige Hinweise

- `data/raw/` und `data/processed/` sind **nicht im Git** (zu grosse Dateien)
- `.env` ist **nicht im Git** – ORS API Key separat anfragen
- PostgreSQL muss lokal laufen fuer Notebook 02
- ORS Rate Limit: 500 Requests/Tag, 20/Minute

## Gruppe

Haris, Chris & Daniel
ZHAW – Modul: Einsatz von Geodaten im Marketing (EGM) – FS2026

## Quellen

- OpenStreetMap Contributors (2024). Overpass API. https://overpass-api.de
- swisstopo (2026). swissBOUNDARIES3D 2026. https://data.geo.admin.ch
- Stadt Zuerich (2024). Stadtquartiere OGD. https://data.stadt-zuerich.ch
- OpenRouteService (2024). Isochrones API. https://openrouteservice.org
