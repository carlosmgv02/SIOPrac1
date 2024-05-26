import json

from GIS.queries import fetch_genre_preferences_by_country
from GIS.data_cleaner import DataCleaner

# Suponiendo que DataCleaner y el dataframe de géneros ya están importados y configurados
cleaner = DataCleaner('countries.geojson', 'continents.geojson', 'capitals.csv')
cleaner.load_data()
cleaner.clean_country_names()

# DataFrame de géneros por país
df_genres_by_country = fetch_genre_preferences_by_country()  # esta función debe estar definida en otro lugar del código

# Cargar el JSON de conversión de códigos de país
with open('country_conversion.json', 'r') as f:
    code_conversion = json.load(f)

# Convertir códigos de país de dos letras a tres letras para alinear con los datos GeoJSON
df_genres_by_country['country_code'] = df_genres_by_country['country_code'].apply(lambda x: code_conversion.get(x, "Código no encontrado"))

# Agrupar y sumar las ocurrencias de género por país
df_country_genre_counts = df_genres_by_country.groupby('country_code').agg({'genre_count': 'sum'}).reset_index()

# Unir con GeoJSON de países
for feature in cleaner.countries_geojson['features']:
    country_code = feature['properties']['ISO_A3']
    try:
        # Asignar la cuenta de género al GeoJSON directamente
        feature['properties']['genre_count'] = int(df_country_genre_counts.loc[df_country_genre_counts['country_code'] == country_code, 'genre_count'])
    except TypeError:
        feature['properties']['genre_count'] = 0  # Para países sin datos

# Guardar el GeoJSON modificado para su uso en la visualización
cleaned_geojson_path = 'cleaned_countries.geojson'
cleaner.save_clean_data(cleaned_geojson_path)
