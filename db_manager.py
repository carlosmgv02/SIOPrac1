from sqlalchemy.exc import IntegrityError
from model.warehouse import *
import pandas as pd
from utils.data_cleaner import clean_characters
from utils.processing_utils import get_or_create_age_certification, normalize_data, process_genres, process_countries, \
    get_or_create_person
from utils.processing_utils import extract_provider_name

'''
    This function is used to import the data from a row of the dataset into the database.
'''
def import_data_from_row(row, provider_name, is_credit=False):
    # Buscar o crear la plataforma basada en provider_name
    platform = session.query(Platforms).filter_by(name=provider_name).first()
    if not platform:
        platform = Platforms(name=provider_name)
        session.add(platform)
        session.commit()
    if is_credit:
        characters = clean_characters(row['character'])
        for character in characters:
            try:
                person = get_or_create_person(session, row['name'])  # Asume que 'name' es el nombre de la persona

                role = session.query(Roles).filter_by(name=row['role']).first()
                if not role:
                    role = Roles(name=row['role'])
                    session.add(role)
                    session.flush()

                existing_credit = session.query(Credits).filter_by(person_id=person.id, title_id=row['id'],
                                                                   role_id=role.id).first()
                if existing_credit:
                    existing_credit.character = character
                else:
                    credit = Credits(person_id=person.id, title_id=row['id'], character=character, role_id=role.id)
                    session.add(credit)

                session.commit()
            except IntegrityError as e:
                print(f"Error processing credit {row['id']}: {e}")
                session.rollback()

    else:
        try:
            description = None if pd.isna(row['description']) else row['description']
            imdb_id = None if pd.isna(row['imdb_id']) else row['imdb_id']
            imdb_score = None if pd.isna(row['imdb_score']) else float(row['imdb_score'])
            imdb_votes = None if pd.isna(row['imdb_votes']) else int(row['imdb_votes'])
            tmdb_popularity = None if pd.isna(row['tmdb_popularity']) else float(row['tmdb_popularity'])
            tmdb_score = None if pd.isna(row['tmdb_score']) else float(row['tmdb_score'])

            # Obteniendo o creando la certificación de edad si no es NaN.
            age_certification = None
            if pd.notna(row['age_certification']):
                age_certification = get_or_create_age_certification(session, row['age_certification'])

            existing_title = session.query(Titles).filter_by(id=row['id']).first()
            if existing_title:
                # Normaliza y actualiza los datos si el título ya existe.
                normalize_data(session, existing_title, {
                    'description': description,
                    'imdb_id': imdb_id,
                    'imdb_score': imdb_score,
                    'imdb_votes': imdb_votes,
                    'tmdb_popularity': tmdb_popularity,
                    'tmdb_score': tmdb_score,
                    # Incluye cualquier otro campo que necesites actualizar.
                })
            else:
                new_title = Titles(
                    id=row['id'],
                    title=row['title'],
                    type=row['type'],
                    description=description,
                    release_year=int(row['release_year']),
                    runtime=int(row['runtime']),
                    seasons=int(row['seasons']) if pd.notnull(row['seasons']) else None,
                    imdb_id=imdb_id,
                    imdb_score=imdb_score,
                    imdb_votes=imdb_votes,
                    tmdb_popularity=tmdb_popularity,
                    tmdb_score=tmdb_score,
                    platform_id=platform.id,
                    age_certification_id=age_certification.id if age_certification else None
                )
                session.add(new_title)
                session.flush()

            if not existing_title:
                # Solo procesa géneros y países si es un nuevo título
                process_genres(row.get('genres'), new_title)
                process_countries(row.get('production_countries'), new_title)


            session.commit()
        except Exception as e:
            print(f"Error processing title {row['id']}: {e}")
            session.rollback()



'''
    This function is used to process all the files in the given directory.
'''
def process_files(directory):
    title_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Titles' in f]
    credit_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Credits' in f]

    for file_name in title_files:
        print(f"Processing Titles: {file_name}...")
        raw_provider_name = (file_name)  # Extrae correctamente el nombre del proveedor
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            provider_name = extract_provider_name(raw_provider_name)
            import_data_from_row(row, provider_name, is_credit=False)


    # Procesar archivos de créditos
    for file_name in credit_files:
        print(f"Processing Credits: {file_name}...")
        raw_provider_name = (file_name)  # Extrae correctamente el nombre del proveedor
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            provider_name = extract_provider_name(raw_provider_name)
            import_data_from_row(row, provider_name, is_credit=True)
