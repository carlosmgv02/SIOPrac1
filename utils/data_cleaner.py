import math
import json
import pandas as pd
import re
import ast

import pandas as pd
import json


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


'''
    This function is used to clean the list of genres and production countries from the dataset.
'''
def clean_list(value):
    if pd.isna(value) or value == "[]":
        return []
    try:
        return eval(value)
    except:
        return []


'''
    This function is used to convert the name of the country to its initials if the name is too long.
'''
def convert_to_initials(country_name):
    if len(country_name) > 10:
        initials = ''.join([word[0] for word in country_name.split()])
        return initials.upper()
    else:
        return country_name


'''
    This function is used to clean the list of characters from the dataset.
'''
def clean_characters(characters):
    # Comprobamos si characters es un valor NaN numérico o None
    if characters is None or (isinstance(characters, float) and math.isnan(characters)):
        return []

    # Asumiendo que quieres mantener la comprobación de la cadena 'nan' también
    if characters == 'nan':
        return []

    cleaned_characters = []
    # Dividimos los nombres de personajes usando diferentes delimitadores
    for character in characters.split('/'):
        # Eliminamos los espacios en blanco al principio y al final del nombre del personaje
        character = character.strip()

        # Si el nombre del personaje contiene un paréntesis, solo mantenemos el nombre antes del paréntesis
        character = re.sub(r'\s*\(.*\)', '', character)

        # Si el nombre del personaje contiene un guion, solo mantenemos el nombre antes del guion
        character = character.split(' - ')[0]

        # Si el nombre del personaje contiene una coma, lo dividimos y agregamos cada parte a la lista de personajes
        if ',' in character:
            cleaned_characters.extend([part.strip() for part in character.split(',')])
        else:
            cleaned_characters.append(character)

    return cleaned_characters
