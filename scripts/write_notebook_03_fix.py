import json
from pathlib import Path

path = Path(r'C:\Projects\pharmacy-accessibility-ch\notebooks\03_isochrones_ors.ipynb')

# Read existing notebook
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

# Find and fix the batch isochrone cell - add sleep + sample
new_cells = []
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
        
        # Fix rate limit: add sleep and sample to any cell doing batch requests
        if 'ors_isochrones' in src and ('for ' in src or 'apply' in src):
            src = (
                'import time\n\n'
                '# Nur 20 Apotheken als Stichprobe (Rate Limit: 40 req/min)\n'
                'SAMPLE_SIZE = 20\n'
                'gdf_sample = gdf_pharm.sample(SAMPLE_SIZE, random_state=42).reset_index(drop=True)\n'
                'print(f"Stichprobe: {SAMPLE_SIZE} von {len(gdf_pharm)} Apotheken")\n'
                '\n'
                'results = []\n'
                'ranges_s = [300, 600, 900]  # 5, 10, 15 Minuten\n'
                '\n'
                'for i, row in gdf_sample.iterrows():\n'
                '    pt_lv95 = row.geometry\n'
                '    pt_wgs84 = gpd.GeoSeries([pt_lv95], crs=gdf_pharm.crs).to_crs(4326).iloc[0]\n'
                '    lon, lat = float(pt_wgs84.x), float(pt_wgs84.y)\n'
                '    try:\n'
                '        res = ors_isochrones("driving-car", lon, lat, ranges_s)\n'
                '        for feat in res.get("features", []):\n'
                '            feat["properties"]["pharmacy_id"] = row.get("osm_id", i)\n'
                '            results.append(feat)\n'
                '        print(f"{i+1}/{SAMPLE_SIZE} OK")\n'
                '    except Exception as e:\n'
                '        if "429" in str(e):\n'
                '            print(f"{i+1}/{SAMPLE_SIZE} Rate limit - warte 15s...")\n'
                '            time.sleep(15)\n'
                '        else:\n'
                '            print(f"{i+1}/{SAMPLE_SIZE} Fehler: {e}")\n'
                '    time.sleep(2)  # 2s zwischen Requests\n'
                '\n'
                'print(f"Isochronen berechnet: {len(results)} Features")\n'
            )
            cell['source'] = src
            cell['outputs'] = []
            cell['execution_count'] = None
    new_cells.append(cell)

nb['cells'] = new_cells

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Notebook 03 gepatcht!')
