import pandas as pd

from utils.data_cleaner import clean_list, convert_to_initials
from model.warehouse import *


def get_or_create_age_certification(session, age_certification_name):
    if pd.isna(age_certification_name):  # Verifica si es NaN y trata adecuadamente
        age_certification_name = None  # O podrías usar una cadena vacía: ''

    if age_certification_name:
        age_certification = session.query(AgeCertifications).filter_by(name=age_certification_name).first()
        if not age_certification:
            age_certification = AgeCertifications(name=age_certification_name)
            session.add(age_certification)
            session.commit()
        return age_certification
    return None


def normalize_data(session, existing_title: Titles, new_data: dict):
    # Suponiendo que new_data es un diccionario con los nuevos valores
    # y existing_title es una instancia del modelo Titles ya existente.
    if existing_title.imdb_score and new_data['imdb_score']:
        existing_title.imdb_score = (existing_title.imdb_score + new_data['imdb_score']) / 2
    if existing_title.imdb_votes and new_data['imdb_votes']:
        existing_title.imdb_votes = (existing_title.imdb_votes + new_data['imdb_votes']) / 2
    if existing_title.tmdb_popularity and new_data['tmdb_popularity']:
        existing_title.tmdb_popularity = (existing_title.tmdb_popularity + new_data['tmdb_popularity']) / 2
    if existing_title.tmdb_score and new_data['tmdb_score']:
        existing_title.tmdb_score = (existing_title.tmdb_score + new_data['tmdb_score']) / 2
    # Agrega aquí cualquier otra normalización que necesites
    session.commit()

def process_genres(genres_str, title_obj):
    genres = clean_list(genres_str)
    for genre_name in genres:
        genre = session.query(Genres).filter_by(name=genre_name).first()
        if not genre:
            genre = Genres(name=genre_name)
            session.add(genre)
            session.flush()
        title_obj.genres.append(genre)

def get_or_create_person(session, name):
    person = session.query(People).filter_by(name=name).first()
    if not person:
        person = People(name=name)
        session.add(person)
        session.commit()  # Asegúrate de hacer commit solo si es necesario
    return person


def process_countries(countries_str, title_obj):
    countries = clean_list(countries_str)
    for country_name in countries:
        country_code = convert_to_initials(country_name)
        country = session.query(ProductionCountries).filter_by(country_code=country_code).first()
        if not country:
            country = ProductionCountries(country_code=country_code)
            session.add(country)
            session.flush()
        title_obj.countries.append(country)

def extract_provider_name(file_name):
    parts = file_name.rsplit('_', 1)  # Dividir por la última aparición de '_'
    provider_name = parts[0].replace('_', ' ')  # Reemplazar los restantes '_' por espacios
    return provider_name

