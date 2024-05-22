import json
import pandas as pd

class DataCleaner:
    def __init__(self, countries_geojson_path, continents_geojson_path, capitals_csv_path):
        self.countries_geojson_path = countries_geojson_path
        self.continents_geojson_path = continents_geojson_path
        self.capitals_csv_path = capitals_csv_path

    def load_data(self):
        with open(self.countries_geojson_path, 'r') as f:
            self.countries_geojson = json.load(f)
        with open(self.continents_geojson_path, 'r') as f:
            self.continents_geojson = json.load(f)
        self.capitals = pd.read_csv(self.capitals_csv_path, delimiter=';')

    def clean_country_names(self):
        # Lowercase country names in capitals CSV
        self.capitals['COUNTRY'] = self.capitals['COUNTRY'].str.lower()

        # Lowercase country names in countries GeoJSON
        for feature in self.countries_geojson['features']:
            feature['properties']['ADMIN'] = feature['properties']['ADMIN'].lower()

        # Find discrepancies
        capitals_countries = set(self.capitals['COUNTRY'].unique())
        geojson_countries = set(feature['properties']['ADMIN'] for feature in self.countries_geojson['features'])
        self.discrepancies = capitals_countries - geojson_countries
        return self.discrepancies

    def save_clean_data(self, output_geojson_path):
        with open(output_geojson_path, 'w') as f:
            json.dump(self.countries_geojson, f)


if __name__ == "__main__":
    cleaner = DataCleaner('countries.geojson', 'continents.geojson', 'capitals.csv')
    cleaner.load_data()
    discrepancies = cleaner.clean_country_names()
    if discrepancies:
        print(f"Discrepàncies trobades: {discrepancies}")
    cleaner.save_clean_data('cleaned_countries.geojson')
