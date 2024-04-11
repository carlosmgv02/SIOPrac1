import subprocess
import schedule
def ejecutar_script():
    try:
        # Ejecuta el script data_sync_Service.py
        subprocess.run(["python", "data_sync_Service.py"])
        print("Sincronizacion completada.")
    except Exception as e:
        print("Error al ejecutar el script de sincronizacion de datos:", e)


def programar_tareas():
    # Programa la tarea para ejecutar data_sync_Service.py cada 15 segundos
    schedule.every(15).seconds.do(ejecutar_script)