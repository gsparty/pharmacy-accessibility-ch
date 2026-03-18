# Pharmacy Accessibility Switzerland
## Geomarketing-Analyse zur Erreichbarkeit von Apotheken in der Schweiz

![Python](https://img.shields.io/badge/python-3.13-blue) ![PostGIS](https://img.shields.io/badge/PostGIS-3.6-green)

## Zentrale Ergebnisse
- 1562 von 2123 Gemeinden (74%) haben keine eigene Apotheke
- 9.15% der Bevoelkerung (832'482 Personen) leben >5km von einer Apotheke
- 1.40% (127'106 Personen) leben >10km von einer Apotheke
- Schlechtestversorgte Gemeinde: Rheinwald (GR) mit 23.2km
- Zuerich: 103 Apotheken, Genf: 84, Basel: 60

## Projektstruktur
```
pharmacy-accessibility-ch/
├── data/
│   ├── raw/           # Originaldaten (nicht in Git)
│   └── processed/     # Bereinigte Geodaten (nicht in Git)
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_postgis_analysis.ipynb
│   ├── 03_isochrones_ors.ipynb
│   ├── 04_spatial_analysis.ipynb
│   ├── 05_population_coverage.ipynb
│   └── 06_visualization.ipynb
├── outputs/maps/      # Generierte Karten
├── sql/               # PostGIS Queries
├── src/               # Hilfsfunktionen
├── requirements.txt
└── .env.example
```

## Setup
```powershell
git clone https://github.com/gsparty/pharmacy-accessibility-ch.git
cd pharmacy-accessibility-ch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# .env oeffnen und ORS_API_KEY eintragen
```

### PostgreSQL + PostGIS
```powershell
psql -U postgres -c "CREATE DATABASE pharmacy_ch;"
psql -U postgres -d pharmacy_ch -c "CREATE EXTENSION postgis CASCADE;"
```

## Umgebungsvariablen
```
ORS_API_KEY=your_openrouteservice_api_key
```
Kostenlosen Key: https://openrouteservice.org/dev/#/signup

## Datenquellen
| Datei | Quelle | Inhalt |
|-------|--------|--------|
| pharmacies_ch.geojson | OpenStreetMap / Overpass API | 1640 Apotheken CH |
| gemeinden_ch_lv95.geojson | swisstopo swissBOUNDARIES3D 2026 | 2123 Gemeinden |
| plz_ch_lv95.geojson | swisstopo Ortschaftenverzeichnis | 4073 PLZ-Gebiete |
| stadtquartiere_zuerich.geojson | Stadt Zuerich OGD | 34 Stadtquartiere |

## Methoden
- **GeoPandas**: Raeumliche Datenverarbeitung in Python
- **PostGIS**: ST_Within, ST_Distance, ST_DWithin
- **OpenRouteService**: Isochrone- und Fahrzeitanalysen
- **PySAL/ESDA**: Spatial Autocorrelation (Morans I)
- **QGIS**: Visuelle Exploration

## Quellen
- OpenStreetMap Contributors (2024). Overpass API. https://overpass-api.de
- swisstopo (2026). swissBOUNDARIES3D 2026. https://data.geo.admin.ch
- Stadt Zuerich (2024). Stadtquartiere OGD. https://data.stadt-zuerich.ch
- OpenRouteService (2024). Isochrones API. https://openrouteservice.org

## Gruppe
ZHAW - Modul: Einsatz von Geodaten im Marketing (EGM) - FS2026
