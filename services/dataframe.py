import pandas as pd
from model.warehouse import *

# Consulta los datos de las tablas Titles, Genres y ProductionCountries
titles_data = session.query(Titles).all()
genres_data = session.query(Genres).all()
countries_data = session.query(ProductionCountries).all()

# Convierte los datos en diccionarios
titles_dict = [{column.name: getattr(instance, column.name) for column in Titles.__table__.columns} for instance in titles_data]
genres_dict = [{column.name: getattr(instance, column.name) for column in Genres.__table__.columns} for instance in genres_data]
countries_dict = [{column.name: getattr(instance, column.name) for column in ProductionCountries.__table__.columns} for instance in countries_data]

# Crea DataFrames de Pandas
titles_df = pd.DataFrame(titles_dict)
genres_df = pd.DataFrame(genres_dict)
countries_df = pd.DataFrame(countries_dict)
