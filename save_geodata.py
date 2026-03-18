import geopandas as gpd
from pathlib import Path

RAW = Path('data/raw')
gpkg_path = RAW / 'boundaries_raw/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg'

gdf = gpd.read_file(gpkg_path, layer='tlm_hoheitsgebiet')

gemeinden = gdf[gdf['objektart'] == 'Gemeindegebiet'].copy()
print('Gemeinden:', len(gemeinden))
print('CRS:', gemeinden.crs)
print('Einwohnerzahl total:', gemeinden['einwohnerzahl'].sum())

gemeinden.to_file(RAW / 'gemeinden_ch_lv95.geojson', driver='GeoJSON')
print('Gespeichert: gemeinden_ch_lv95.geojson')

kantone = gdf[gdf['objektart'] == 'Kantonsgebiet'].copy()
kantone.to_file(RAW / 'kantone_ch_lv95.geojson', driver='GeoJSON')
print('Kantone gespeichert:', len(kantone))

gdf_plz = gpd.read_file(RAW / 'plz_raw/AMTOVZ_SHP_LV95/AMTOVZ_ZIP.shp')
print('PLZ-Gebiete:', len(gdf_plz))
print('PLZ Spalten:', gdf_plz.columns.tolist())
gdf_plz.to_file(RAW / 'plz_ch_lv95.geojson', driver='GeoJSON')
print('Gespeichert: plz_ch_lv95.geojson')
