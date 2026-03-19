import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

PROCESSED = Path('data/processed')
OUTPUTS   = Path('outputs/maps')

print('1. Lade optimierte Daten...')
gdf_gem   = gpd.read_file(PROCESSED / 'gemeinden_mit_distanz.gpkg')
gdf_pharm = gpd.read_file(PROCESSED / 'pharmacies_ch.geojson')
gdf_kant  = gpd.read_file('data/raw/kantone_ch_lv95.geojson')

gdf_gem_plot = gdf_gem.copy()
gdf_gem_plot['geometry'] = gdf_gem_plot.geometry.simplify(50)
gdf_kant_plot = gdf_kant.copy()
gdf_kant_plot['geometry'] = gdf_kant_plot.geometry.simplify(50)

print('2. Erstelle Kennzahlen-Dashboard (Gefixt)...')
total_bev = gdf_gem['einwohnerzahl'].sum()
bev_5km   = gdf_gem[gdf_gem['min_distanz_m'] > 5000]['einwohnerzahl'].sum()
bev_10km  = gdf_gem[gdf_gem['min_distanz_m'] > 10000]['einwohnerzahl'].sum()
gem_ohne  = (gdf_gem['apotheken_anzahl'] == 0).sum()
max_dist  = gdf_gem['min_distanz_m'].max()
worst = gdf_gem_plot.nlargest(1, 'min_distanz_m').iloc[0]

fig2, axes = plt.subplots(2, 3, figsize=(16, 8))
fig2.patch.set_facecolor('#f8f9fa')
kennzahlen = [
    ('1640', 'Apotheken\nin der Schweiz', '#2ecc71'), ('2123', 'Gemeinden\nanalysiert', '#3498db'),
    (f'{gem_ohne}\n(74%)', 'Gemeinden\nohne Apotheke', '#e74c3c'),
    (f'{bev_5km/1e6:.2f} Mio', f'Personen\n> 5 km ({bev_5km/total_bev*100:.1f}%)', '#e67e22'),
    (f'{bev_10km/1e3:.0f} Tsd', f'Personen\n> 10 km ({bev_10km/total_bev*100:.1f}%)', '#c0392b'),
    (f'{max_dist/1000:.1f} km', f'Groesste Distanz\n({worst["name"]})', '#8e44ad')
]
for ax, (wert, label, farbe) in zip(axes.flat, kennzahlen):
    ax.set_facecolor(farbe)
    ax.text(0.5, 0.55, wert, transform=ax.transAxes, fontsize=24, fontweight='bold', color='white', ha='center', va='center')
    ax.text(0.5, 0.2, label, transform=ax.transAxes, fontsize=13, color='white', ha='center', va='center')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
fig2.suptitle('Apothekenerreichbarkeit Schweiz – Kennzahlen', fontsize=18, fontweight='bold')
fig2.tight_layout()

# FIX: bbox_inches entfernt, damit der Text nicht weggeschnitten wird!
fig2.savefig(OUTPUTS / '06_kennzahlen_dashboard.png', dpi=150)
plt.close(fig2)

print('Dashboard erfolgreich generiert! Checke das Bild.')
