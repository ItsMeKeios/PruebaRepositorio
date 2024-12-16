import subprocess
import json
import time
from flask import Flask, jsonify

app = Flask(__name__)

def iniciar_ngrok():
    # Iniciar ngrok en un proceso independiente
    ngrok_process = subprocess.Popen(['ngrok', 'http', '7899'])
    time.sleep(2)  # Esperar que ngrok inicie

    # Obtener la URL de ngrok desde la API
    response = subprocess.run(['curl', 'http://127.0.0.1:4040/api/tunnels'], capture_output=True, text=True)
    tunnels_info = json.loads(response.stdout)

    # Obtener la URL pública de ngrok
    ngrok_url = tunnels_info['tunnels'][0]['public_url']

    # Guardar la URL de ngrok en un archivo
    with open('ngrok_url.txt', 'w') as file:
        file.write(ngrok_url)

    print(f"URL de ngrok: {ngrok_url}")
    return ngrok_url

def obtener_ngrok_url():
    try:
        with open('ngrok_url.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

@app.route('/macro', methods=['POST'])
def ejecutar_macro():
    try:
        # Ejecutar el script RealizarMacro.py y capturar el resultado
        result = subprocess.run(['python', 'scripts/RealizarMacro.py'], capture_output=True, text=True)

        # Obtener el estado del script
        estatus = result.stdout.strip()

        if estatus == "CORRECTO":
            return jsonify({"message": "Macro ejecutada con éxito"}), 200
        else:
            return jsonify({"message": "Hubo un error al ejecutar la macro"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"message": f"Error al ejecutar el script: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Error inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    # Iniciar ngrok y obtener la URL
    ngrok_url = iniciar_ngrok()

    # Iniciar el servidor Flask
    app.run(port=7899, host='0.0.0.0')
