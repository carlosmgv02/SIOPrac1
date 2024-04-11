from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model.warehouse import Titles  # Asumiendo que tienes este modelo
from config.warehouse_config import POSTGRES_URI  # Asegúrate de tener esta configuración
from config.elastic_config import get_es_client
from elasticsearch.exceptions import NotFoundError

# Configuración de la conexión a PostgreSQL
engine = create_engine(POSTGRES_URI)
Session = sessionmaker(bind=engine)

def get_titles_not_in_es():
    """Extrae títulos de PostgreSQL que aún no están en Elasticsearch."""
    session = Session()
    es = get_es_client()
    titles_not_in_es = []

    for title in session.query(Titles).all():
        try:
            es.get(index="titles", id=title.id)
        except NotFoundError:
            # Este título no está en ES, lo agregamos a la lista
            titles_not_in_es.append(title)

    session.close()
    return titles_not_in_es

def index_titles_in_es(titles):
    """Indexa una lista de títulos en Elasticsearch."""
    es = get_es_client()
    for title in titles:
        doc = {
            "title": title.title,
            "description": title.description,
            "release_year": title.release_year,
            # Agrega más campos según sea necesario
        }
        es.index(index="titles", id=title.id, document=doc)
        print(f"Indexed title {title.id} in Elasticsearch.")

if __name__ == "__main__":
    titles_to_index = get_titles_not_in_es()
    if titles_to_index:
        index_titles_in_es(titles_to_index)
    else:
        print("No new titles to index in Elasticsearch.")
