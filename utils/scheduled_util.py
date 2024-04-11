import threading
import time
# Importa las funciones del script de sincronización
from services.data_sync_service import get_titles_not_in_es, index_titles_in_es

def ejecutar_data_sync_service():
    try:
        titles_to_index = get_titles_not_in_es()
        if titles_to_index:
            index_titles_in_es(titles_to_index)
        else:
            print("No new titles to index in Elasticsearch.")
    except Exception as e:
        print(f"Error durante la sincronización de datos: {e}")

def tarea_periodica():
    while True:
        ejecutar_data_sync_service()
        time.sleep(15)  # Espera 15 segundos antes de ejecutar la tarea nuevamente

def iniciar_tarea_en_hilo():
    hilo_de_tarea = threading.Thread(target=tarea_periodica)
    hilo_de_tarea.daemon = True  # Esto hace que el hilo se cierre cuando el programa principal termina
    hilo_de_tarea.start()
