from pathlib import Path

# ============================================================
# 1. README schreiben
# ============================================================
readme = """# Pharmacy Accessibility Switzerland
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
.\\venv\\Scripts\\Activate.ps1
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
jupyter nbconvert --to notebook --execute notebooks\\NB.ipynb --output NB.ipynb --output-dir notebooks --ExecutePreprocessor.timeout=300
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

ZHAW – Modul: Einsatz von Geodaten im Marketing (EGM) – FS2026

## Quellen

- OpenStreetMap Contributors (2024). Overpass API. https://overpass-api.de
- swisstopo (2026). swissBOUNDARIES3D 2026. https://data.geo.admin.ch
- Stadt Zuerich (2024). Stadtquartiere OGD. https://data.stadt-zuerich.ch
- OpenRouteService (2024). Isochrones API. https://openrouteservice.org
"""
Path('README.md').write_text(readme, encoding='utf-8')
print('README geschrieben!')

# ============================================================
# 2. Notebook 06 fixen: Dashboard + Isochronen-Alpha
# ============================================================
import json

# Fix 06_visualization.ipynb
nb_path = Path('notebooks/06_visualization.ipynb')
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])

    # Fix Dashboard: dunkler Hintergrund damit weisser Text sichtbar ist
    if 'kennzahlen_dashboard' in src and 'fig.patch' in src:
        src = src.replace(
            "fig.patch.set_facecolor('#f8f9fa')",
            "fig.patch.set_facecolor('#2c3e50')"
        )
        # Fix: Text schwarz machen da Hintergrund jetzt dunkel
        src = src.replace(
            "plt.suptitle('Apothekenerreichbarkeit Schweiz – Kennzahlen', fontsize=16, fontweight='bold')",
            "plt.suptitle('Apothekenerreichbarkeit Schweiz – Kennzahlen', fontsize=16, fontweight='bold', color='white')"
        )
        cell['source'] = src
        cell['outputs'] = []
        cell['execution_count'] = None
        print('Dashboard Fix angewendet')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Notebook 06 gepatcht!')

# Fix 03_isochrones: Alpha erhoehen
nb_path3 = Path('notebooks/03_isochrones_ors.ipynb')
with open(nb_path3, encoding='utf-8') as f:
    nb3 = json.load(f)

for cell in nb3['cells']:
    if cell['cell_type'] != 'code':
        continue
    src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
    if 'gdf_iso_sample.plot' in src and 'alpha=0.25' in src:
        src = src.replace('alpha=0.25', 'alpha=0.6')
        cell['source'] = src
        cell['outputs'] = []
        cell['execution_count'] = None
        print('Isochronen Alpha Fix angewendet')

with open(nb_path3, 'w', encoding='utf-8') as f:
    json.dump(nb3, f, indent=1, ensure_ascii=False)
print('Notebook 03 gepatcht!')

# Fix 05: Legende fixen
nb_path5 = Path('notebooks/05_population_coverage.ipynb')
with open(nb_path5, encoding='utf-8') as f:
    nb5 = json.load(f)

for cell in nb5['cells']:
    if cell['cell_type'] != 'code':
        continue
    src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
    if 'unterversorgte_gemeinden' in src and "ax.legend(title='Distanz'" in src:
        src = src.replace(
            "ax.legend(title='Distanz', loc='lower left', fontsize=10)",
            (
                "from matplotlib.patches import Patch\n"
                "legend_els = [\n"
                "    Patch(color='#e8e8e8', label='Gut versorgt (< 5km)'),\n"
                "    Patch(color='#d73027', label='Unterversorgt (5-10km)'),\n"
                "    Patch(color='#7f0000', label='Sehr schlecht (> 10km)'),\n"
                "]\n"
                "ax.legend(handles=legend_els, title='Versorgung', loc='lower left', fontsize=9)"
            )
        )
        cell['source'] = src
        cell['outputs'] = []
        cell['execution_count'] = None
        print('Legende Fix angewendet')

with open(nb_path5, 'w', encoding='utf-8') as f:
    json.dump(nb5, f, indent=1, ensure_ascii=False)
print('Notebook 05 gepatcht!')

print()
print('Alle Fixes angewendet!')
print('Jetzt ausfuehren:')
print('  jupyter nbconvert --to notebook --execute notebooks\\03_isochrones_ors.ipynb ...')
print('  jupyter nbconvert --to notebook --execute notebooks\\05_population_coverage.ipynb ...')
print('  jupyter nbconvert --to notebook --execute notebooks\\06_visualization.ipynb ...')
