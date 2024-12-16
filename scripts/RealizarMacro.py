import time
import keyboard
import json
import os

def reproducir_macro():
    print("Esperando 5 segundos antes de realizar la Macro...")
    time.sleep(5)
    print("Comenzando la Macro")

    # Obtener la ruta correcta a la carpeta "JSON ACTUAL"
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_folder = os.path.join(base_path, "JSON ACTUAL")

    # Listar los archivos .json en la carpeta "JSON ACTUAL"
    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
    
    if len(json_files) != 1:
        print("Error: Debe haber exactamente un archivo JSON en la carpeta 'JSON ACTUAL'.")
        return "FALLO"  # Devuelves el estado "FALLO" si hay un problema

    json_file = json_files[0] 

    # Leer el archivo JSON
    try:
        with open(os.path.join(json_folder, json_file), "r") as file:
            keystrokes = json.load(file)
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return "FALLO"

    last_time = time.time()

    try:
        for keystroke in keystrokes:
            event_time = keystroke['elapsed_time']
            time.sleep(event_time - (time.time() - last_time))  # Ajustar el tiempo transcurrido

            if keystroke['event'] == 'keydown':
                keyboard.press(keystroke['name'])
            elif keystroke['event'] == 'keyup':
                keyboard.release(keystroke['name'])

            last_time = time.time()

        print("Se ha realizado con éxito el script.")
        return "CORRECTO"  # Devuelves el estado "CORRECTO" si todo salió bien

    except Exception as e:
        print(f"Error durante la ejecución de la macro: {e}")
        return "FALLO"  # Devuelves el estado "FALLO" si ocurre un error

def main():
    status = reproducir_macro()
    print(f"Estado del script: {status}")
    return status

if __name__ == "__main__":
    status = main()
