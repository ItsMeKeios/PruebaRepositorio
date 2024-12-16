from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

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
    app.run(port=7899, host='0.0.0.0')

