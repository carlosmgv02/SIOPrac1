import time
from db_manager import process_files
from utils.scheduled_util import programar_tareas
import schedule

directory = 'Dataset'
if __name__ == '__main__':
    # Programa las tareas
    # process_files(directory)
    programar_tareas()


