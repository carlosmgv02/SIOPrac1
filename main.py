import pandas as pd

from db_manager import process_files
from logger.color_logger import setup_logger
import logging
from utils.scheduled_util import iniciar_tarea_en_hilo
from services import eda
from config.warehouse_config import get_db_engine

directory = 'Dataset'
sql_query = 'SELECT * FROM titles limit 100'
session = get_db_engine()

if __name__ == '__main__':
    setup_logger()
    #process_files(directory)
    iniciar_tarea_en_hilo()
    # process_files(directory)

    # Carrega el DataFrame amb les dades
    #data = pd.read_csv('./Dataset/Amazon_Prime_Titles.csv')
    data = pd.read_sql(sql_query, session)
    data.set_index('id', inplace=True)
    # Crea una instància de la classe EDA
    eda = eda.EDA(data)

    # Ploteja un histograma d'una columna específica
    eda.plot_histogram('imdb_score', bins=15)
    eda.plot_heatmap(['imdb_score', 'type'], "Mapa de Calor")
    eda.plot_scatter('imdb_score', 'release_year', "Scatter Puntuación-Votos")
    eda.plot_violin('imdb_score', "Gráfico de Violín Géneros")

    # Ploteja la matriu de correlació
    eda.plot_correlation_matrix()

    # Ploteja un boxplot d'una columna específica
    eda.plot_distribution('imdb_score')

    # Identifica valors perduts
    missing_values = eda.missing_values()
    print(missing_values)

    print("El script principal continúa ejecutándose mientras las tareas programadas corren en segundo plano.")





