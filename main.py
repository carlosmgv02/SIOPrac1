import pandas as pd

from db_manager import process_files
from logger.color_logger import setup_logger
import logging
from utils.scheduled_util import iniciar_tarea_en_hilo
from services import eda

directory = 'Dataset'

if __name__ == '__main__':
    setup_logger()
    #process_files(directory)
    iniciar_tarea_en_hilo()
    # process_files(directory)

    # Carrega el DataFrame amb les dades
    data = pd.read_csv('./Dataset/Amazon_Prime_Titles.csv')
    print(data)

    # Crea una instància de la classe EDA
    eda = eda.EDA(data)

    # Calcula estadístiques descriptives
    descriptive_stats = eda.descriptive_statistics()
    print(descriptive_stats)

    # Ploteja un histograma d'una columna específica
    eda.plot_histogram('genres', bins=15)

    # Ploteja la matriu de correlació
    eda.plot_correlation_matrix()

    # Ploteja un boxplot d'una columna específica
    eda.plot_distribution('imdb_score')

    # Identifica valors perduts
    missing_values = eda.missing_values()
    print(missing_values)

    print("El script principal continúa ejecutándose mientras las tareas programadas corren en segundo plano.")
    # Mantén el programa principal corriendo para que el hilo no termine inmediatamente.
    while True:
        pass




