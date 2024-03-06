import os

from sqlalchemy.exc import IntegrityError
from models import session, Titles, Genres, ProductionCountries, Credits, TitleGenres, TitleCountries
import pandas as pd
from data_cleaner import clean_list, convert_to_initials, clean_characters

'''
    This function is used to import the data from a row of the dataset into the database.
'''
def import_data_from_row(row, is_credit=False):
    if is_credit:
        characters = clean_characters(row['character'])
        for character in characters:
            try:
                credit = Credits(person_id=row['person_id'], title_id=row['id'], name=row['name'],
                                 character=character,
                                 role=row['role'])
                session.add(credit)
                session.commit()
            except IntegrityError as e:
                session.rollback()
    else:
        try:

            description = row['description'] if pd.notnull(row['description']) else None
            age_certification = row['age_certification'] if pd.notnull(row['age_certification']) else None
            imdb_id = row['imdb_id'] if pd.notnull(row['imdb_id']) else None
            imdb_score = row['imdb_score'] if pd.notnull(row['imdb_score']) else None
            imdb_votes = row['imdb_votes'] if pd.notnull(row['imdb_votes']) else None
            tmdb_popularity = row['tmdb_popularity'] if pd.notnull(row['tmdb_popularity']) else None
            tmdb_score = row['tmdb_score'] if pd.notnull(row['tmdb_score']) else None
            genres = clean_list(row['genres'])

            new_title = Titles(
                id=row['id'],
                title=row['title'],
                type=row['type'],
                description=description,
                release_year=row['release_year'],
                age_certification=age_certification,
                runtime=row['runtime'],
                seasons=int(row['seasons']) if pd.notnull(row['seasons']) else None,
                imdb_id=imdb_id,
                imdb_score=imdb_score,
                imdb_votes=imdb_votes,
                tmdb_popularity=tmdb_popularity,
                tmdb_score=tmdb_score
            )
            session.add(new_title)
            session.flush()

            for genre_name in genres:
                genre = session.query(Genres).filter_by(name=genre_name).first()
                if not genre:
                    genre = Genres(name=genre_name)
                    session.add(genre)
                    session.flush()
                new_title.genres.append(genre)

            for country_name in clean_list(row['production_countries']):
                # Convierte el nombre del país a iniciales si es necesario
                country_code = convert_to_initials(country_name)
                country = session.query(ProductionCountries).filter_by(country_code=country_code).first()
                if not country:
                    country = ProductionCountries(country_code=country_code)
                    session.add(country)
                    session.flush()
                new_title.countries.append(country)

            session.commit()
        except IntegrityError as e:
            session.rollback()


'''
    This function is used to process all the files in the given directory.
'''
def process_files(directory):
    title_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Titles' in f]
    credit_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Credits' in f]


    # Procesar primero todos los archivos de títulos
    for file_name in title_files:
        print(f"Processing Titles: {file_name}...")
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            import_data_from_row(row, is_credit=False)


    # Luego procesar todos los archivos de créditos
    for file_name in credit_files:
        print(f"Processing Credits: {file_name}...")
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            import_data_from_row(row, is_credit=True)