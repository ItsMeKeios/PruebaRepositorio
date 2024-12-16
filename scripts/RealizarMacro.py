import time
import keyboard
import json
import os
import subprocess
import psutil
import signal

def cerrar_aplicaciones():
    subprocess.run(["taskkill", "/f", "/im", "Minecraft.Windows.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def apagar_computadora():
    subprocess.run(["shutdown", "/s", "/f", "/t", "0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def cerrar_ngrok_y_flask():
    try:
        # Encontrar y enviar SIGINT (Ctrl + C) al proceso de Flask
        for proc in psutil.process_iter(['pid', 'name']):
            if 'python' in proc.info['name'] and 'server.py' in proc.info['cmdline']:
                print("Cerrando Flask...")
                proc.send_signal(signal.SIGINT)  # Simula un Ctrl + C en el proceso de Flask
                print("Flask cerrado correctamente.")
                break

        # Encontrar y enviar SIGINT (Ctrl + C) al proceso de ngrok
        for proc in psutil.process_iter(['pid', 'name']):
            if 'ngrok' in proc.info['name']:
                print("Cerrando Ngrok...")
                proc.send_signal(signal.SIGINT)  # Simula un Ctrl + C en el proceso de Ngrok
                print("Ngrok cerrado correctamente.")
                break

    except Exception as e:
        print(f"Error al cerrar ngrok y Flask: {e}")

def reproducir_macro():
    print("Esperando 5 segundos antes de realizar la Macro...")
    time.sleep(5)
    print("Comenzando la Macro")

    base_path = os.path.dirname(os.path.abspath(__file__))
    json_folder = os.path.join(base_path, "JSON ACTUAL")
    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
    
    if len(json_files) != 1:
        print("Error: Debe haber exactamente un archivo JSON en la carpeta 'JSON ACTUAL'.")
        return "FALLO"

    json_file = json_files[0] 
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
            time.sleep(event_time - (time.time() - last_time)) 

            if keystroke['event'] == 'keydown':
                keyboard.press(keystroke['name'])
            elif keystroke['event'] == 'keyup':
                keyboard.release(keystroke['name'])

            last_time = time.time()

        print("Se ha realizado con éxito el script.")
        return "CORRECTO"  

    except Exception as e:
        print(f"Error durante la ejecución de la macro: {e}")
        return "FALLO" 

def main():
    status = reproducir_macro()
    print(f"Estado del script: {status}")
    
    # Llamar a las funciones para cerrar aplicaciones y servicios después de ejecutar la macro
    cerrar_aplicaciones()
    cerrar_ngrok_y_flask()
    #apagar_computadora()

    return status

if __name__ == "__main__":
    status = main()
