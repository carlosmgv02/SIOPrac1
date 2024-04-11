from db_manager import process_files
from logger.color_logger import setup_logger
import logging
from utils.scheduled_util import iniciar_tarea_en_hilo

directory = 'Dataset'

if __name__ == '__main__':
    setup_logger()
    #process_files(directory)
    iniciar_tarea_en_hilo()
    # process_files(directory)
    print("El script principal continúa ejecutándose mientras las tareas programadas corren en segundo plano.")
    # Mantén el programa principal corriendo para que el hilo no termine inmediatamente.
    while True:
        pass



