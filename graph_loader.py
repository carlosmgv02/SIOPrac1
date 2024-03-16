import os
import pandas as pd
from py2neo import Graph, Node, Relationship
from data_cleaner import clean_list
import logging

# Configurar el logging
logging.basicConfig(filename='neo4j_data_load.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Conexión a la base de datos de Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Función para crear nodos de personas
def create_person_node(name):
    return Node("Person", name=name)

# Función para crear nodos de películas/series
def create_show_movie_node(title, release_year):
    return Node("ShowMovie", title=title, release_year=release_year)

# Función para crear relaciones entre personas y películas/series
def create_relationship(person, movie, role, character=None):
    if role == "ACTED_IN":
        return Relationship(person, role, movie, character=character)
    elif role == "DIRECTED":
        return Relationship(person, role, movie)
    else:
        return None

# Función para cargar datos en el grafo de Neo4j
def load_data_into_graph(directory):
    title_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Titles' in f]
    credit_files = [f for f in os.listdir(directory) if f.endswith('.csv') and 'Credits' in f]

    # Procesar primero todos los archivos de títulos
    for file_name in title_files:
        logging.info(f"Processing Titles: {file_name}")
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            # Creamos el nodo de la película/serie
            movie_node = create_show_movie_node(row['title'], row['release_year'])
            graph.create(movie_node)
            logging.info(f"Created ShowMovie node: {row['title']}")

            # Cargamos los datos relacionados con la película/serie
            genres = clean_list(row['genres'])
            for genre_name in genres:
                genre_node = Node("Genre", name=genre_name)
                graph.create(genre_node)
                graph.create(Relationship(movie_node, "BELONGS_TO", genre_node))
                logging.info(f"Created Genre node and relationship for {row['title']}: {genre_name}")

            countries = clean_list(row['production_countries'])
            for country_name in countries:
                country_node = Node("Country", name=country_name)
                graph.create(country_node)
                graph.create(Relationship(movie_node, "PRODUCED_IN", country_node))
                logging.info(f"Created Country node and relationship for {row['title']}: {country_name}")

    # Luego procesar todos los archivos de créditos
    for file_name in credit_files:
        logging.info(f"Processing Credits: {file_name}")
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            person_node = create_person_node(row['name'])
            graph.create(person_node)

            movie_node = graph.nodes.match("ShowMovie", title=row['title']).first()
            if movie_node:
                relationship = create_relationship(person_node, movie_node, row['role'], row['character'])
                if relationship:
                    graph.create(relationship)
                    logging.info(f"Created relationship between {row['name']} and {row['title']}: {row['role']}")

if __name__ == "__main__":
    directory = "Dataset"  # Asegúrate de cambiar esto por la ruta real a tu directorio de datos
    load_data_into_graph(directory)
