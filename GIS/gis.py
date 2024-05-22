import pandas as pd
import json

# Carrega el CSV
capitals = pd.read_csv('capitals.csv', delimiter=';')

# Carrega el fitxer GeoJSON dels països
with open('countries.geojson', 'r') as f:
    countries_geojson = json.load(f)

# Verifica la nomenclatura dels països
capitals_countries = capitals['country'].unique()
geojson_countries = [feature['properties']['name'] for feature in countries_geojson['features']]

# Normalitza els noms (exemple bàsic)
capitals['country'] = capitals['country'].str.lower()
for feature in countries_geojson['features']:
    feature['properties']['name'] = feature['properties']['name'].lower()

# Verifica les discrepàncies
discrepancies = set(capitals_countries) - set(geojson_countries)
print(f"Discrepàncies: {discrepancies}")
