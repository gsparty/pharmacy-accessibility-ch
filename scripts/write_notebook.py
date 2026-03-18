import json

ZH_URL = (
    'https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Statistische_Quartiere'
    '?service=WFS&version=1.1.0&request=GetFeature'
    '&typename=adm_statistische_quartiere_map&outputFormat=GeoJSON'
)

nb = {
    'cells': [],
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.13.0'}
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

cells = [
    ('markdown', 'md-01', (
        '# 01 - Data Acquisition\n'
        'Liest lokale Rohdaten aus data/raw/ - kein Download.\n\n'
        '| Datei | Quelle | Inhalt |\n'
        '|-------|--------|--------|\n'
        '| pharmacies_ch.geojson | OpenStreetMap | 1640 Apotheken |\n'
        '| gemeinden_ch_lv95.geojson | swisstopo 2026 | 2123 Gemeinden |\n'
        '| plz_ch_lv95.geojson | swisstopo | 4073 PLZ |\n'
        '| stadtquartiere_zuerich.geojson | Stadt Zuerich OGD | 34 Quartiere ZH |\n\n'
        '**Projektion:** LV95 (EPSG:2056)'
    )),
    ('code', 'c1', (
        'import geopandas as gpd\n'
        'import pandas as pd\n'
        'import matplotlib.pyplot as plt\n'
        'import requests\n'
        'import io\n'
        'from pathlib import Path\n'
        '\n'
        "RAW = Path('../data/raw')\n"
        "PROCESSED = Path('../data/processed')\n"
        'PROCESSED.mkdir(parents=True, exist_ok=True)\n'
        "print('RAW:      ', RAW.resolve())\n"
        "print('PROCESSED:', PROCESSED.resolve())"
    )),
    ('code', 'c2', (
        '# 1. Apotheken\n'
        "gdf_pharmacies = gpd.read_file(RAW / 'pharmacies_ch.geojson')\n"
        'if gdf_pharmacies.crs.to_epsg() != 2056:\n'
        "    gdf_pharmacies = gdf_pharmacies.to_crs('EPSG:2056')\n"
        "print('Apotheken:', len(gdf_pharmacies))\n"
        "print('CRS:      ', gdf_pharmacies.crs)\n"
        'gdf_pharmacies.head()'
    )),
    ('code', 'c3', (
        '# 2. Gemeinden (swisstopo swissBOUNDARIES3D 2026)\n'
        "gdf_gemeinden = gpd.read_file(RAW / 'gemeinden_ch_lv95.geojson')\n"
        "print('Gemeinden:       ', len(gdf_gemeinden))\n"
        "print('CRS:             ', gdf_gemeinden.crs)\n"
        "print('Einwohner total: ', gdf_gemeinden['einwohnerzahl'].sum())\n"
        "gdf_gemeinden[['name','bfs_nummer','einwohnerzahl','gem_flaeche','kantonsnummer']].head()"
    )),
    ('code', 'c4', (
        '# 3. PLZ-Gebiete\n'
        "gdf_plz = gpd.read_file(RAW / 'plz_ch_lv95.geojson')\n"
        'if gdf_plz.crs.to_epsg() != 2056:\n'
        "    gdf_plz = gdf_plz.to_crs('EPSG:2056')\n"
        "print('PLZ-Gebiete:', len(gdf_plz))\n"
        "print('CRS:        ', gdf_plz.crs)\n"
        'gdf_plz.head()'
    )),
    ('code', 'c5', (
        '# 4. Stadtquartiere Zuerich\n'
        '# Quelle: Stadt Zuerich OGD - Statistische Quartiere WFS\n'
        "ZH_URL = (\n"
        "    'https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Statistische_Quartiere'\n"
        "    '?service=WFS&version=1.1.0&request=GetFeature'\n"
        "    '&typename=adm_statistische_quartiere_map&outputFormat=GeoJSON'\n"
        ")\n"
        'r = requests.get(ZH_URL, timeout=60)\n'
        "print('Status:', r.status_code)\n"
        'gdf_quartiere = gpd.read_file(io.BytesIO(r.content))\n'
        'if gdf_quartiere.crs and gdf_quartiere.crs.to_epsg() != 2056:\n'
        "    gdf_quartiere = gdf_quartiere.to_crs('EPSG:2056')\n"
        "gdf_quartiere.to_file(RAW / 'stadtquartiere_zuerich.geojson', driver='GeoJSON')\n"
        "print('Stadtquartiere ZH:', len(gdf_quartiere))\n"
        "print('Spalten:', gdf_quartiere.columns.tolist())\n"
        'gdf_quartiere.head()'
    )),
    ('code', 'c6', (
        '# 5. Uebersichtskarte\n'
        "gdf_kantone = gpd.read_file(RAW / 'kantone_ch_lv95.geojson')\n"
        'fig, ax = plt.subplots(figsize=(14, 9))\n'
        "gdf_kantone.plot(ax=ax, color='#f0f0f0', edgecolor='#999999', linewidth=0.8)\n"
        "gdf_gemeinden.plot(ax=ax, color='none', edgecolor='#cccccc', linewidth=0.2)\n"
        "gdf_pharmacies.plot(ax=ax, color='#e63946', markersize=3, alpha=0.7, label='Apotheke')\n"
        "ax.set_title('Apotheken-Standorte Schweiz (OSM 2024) - 1640 Standorte', fontsize=14, fontweight='bold')\n"
        'ax.set_axis_off()\n'
        "ax.legend(loc='lower right')\n"
        'plt.tight_layout()\n'
        "out = Path('../outputs/maps/01_apotheken_uebersicht.png')\n"
        'out.parent.mkdir(parents=True, exist_ok=True)\n'
        "plt.savefig(out, dpi=150, bbox_inches='tight')\n"
        'plt.show()\n'
        "print('Karte gespeichert:', out)"
    )),
    ('code', 'c7', (
        '# 6. Processed speichern\n'
        "gdf_pharmacies[['osm_id','name','postcode','city','lat','lon','geometry']].to_file(PROCESSED / 'pharmacies_ch.geojson', driver='GeoJSON')\n"
        "gdf_gemeinden[['bfs_nummer','name','einwohnerzahl','gem_flaeche','kantonsnummer','geometry']].to_file(PROCESSED / 'gemeinden_ch.geojson', driver='GeoJSON')\n"
        "gdf_plz.to_file(PROCESSED / 'plz_ch.geojson', driver='GeoJSON')\n"
        "gdf_quartiere.to_file(PROCESSED / 'stadtquartiere_zuerich.geojson', driver='GeoJSON')\n"
        "for fname in ['pharmacies_ch.geojson','gemeinden_ch.geojson','plz_ch.geojson','stadtquartiere_zuerich.geojson']:\n"
        '    p = PROCESSED / fname\n'
        "    size = str(round(p.stat().st_size/1024)) + ' KB' if p.exists() else 'FEHLT'\n"
        "    print(f'{fname:<40} {size}')\n"
        "print('Weiter mit: 02_postgis_analysis.ipynb')"
    )),
]

for ctype, cid, src in cells:
    cell = {'cell_type': ctype, 'id': cid, 'metadata': {}, 'source': src}
    if ctype == 'code':
        cell['execution_count'] = None
        cell['outputs'] = []
    nb['cells'].append(cell)

path = r'C:\Projects\pharmacy-accessibility-ch\notebooks\01_data_acquisition.ipynb'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Notebook geschrieben:', path)
