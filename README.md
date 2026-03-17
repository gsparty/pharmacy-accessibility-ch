# Pharmacy Accessibility Switzerland
Geomarketing-Analyse zur Erreichbarkeit von Apotheken in der Schweiz.

## Projektbeschreibung
Analyse der räumlichen Versorgung mit Apotheken auf Gemeinde-, PLZ- und Stadtquartierebene,
unter Berücksichtigung der Bevölkerungsdichte und Fahrzeitanalysen.

## Setup
\\\powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
\\\

## Projektstruktur
- data/raw         – Rohdaten (OSM, BFS, swisstopo)
- data/processed   – Bereinigte Geodaten
- notebooks/       – Jupyter Notebooks (nummeriert)
- sql/             – PostGIS Queries
- src/             – Hilfsfunktionen
- outputs/maps/    – Exportierte Karten

## Gruppe
[Eure Namen]

## Deadline
27.05.2026
