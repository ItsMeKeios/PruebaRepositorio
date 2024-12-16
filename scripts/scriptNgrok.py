import subprocess
import json
import time

def iniciar_ngrok():
    ngrok_process = subprocess.Popen(['ngrok', 'http', '7899'])
    time.sleep(2) 

    response = subprocess.run(['curl', 'http://127.0.0.1:4040/api/tunnels'], capture_output=True, text=True)
    tunnels_info = json.loads(response.stdout)

    ngrok_url = tunnels_info['tunnels'][0]['public_url']
    with open('ngrok_url.txt', 'w') as file:
        file.write(ngrok_url)

    print(f"URL de ngrok: {ngrok_url}")
    return ngrok_url

if __name__ == '__main__':
    iniciar_ngrok()
