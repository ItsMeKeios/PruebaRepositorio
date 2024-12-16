import time
import keyboard
import json
import os

def grabar_teclas():
    macro_name = input("Ingresa el nombre de la macro (sin extensión .json): ")
    print(f"Grabando macro: {macro_name}.json")
    print("Esperando 5 segundos antes de comenzar la grabación...")
    time.sleep(5)
    print("Comenzando la grabación. Presiona ESC para detener.")

    keystrokes = []
    last_time = time.time()
    pressed_keys = set()
    ctrl_e_count = 0  # Contador de la combinación de teclas Ctrl + E

    def mostrar_tecla(event):
        nonlocal last_time, ctrl_e_count

        current_time = time.time()
        elapsed_time = current_time - last_time

        if event.event_type == keyboard.KEY_DOWN:
            pressed_keys.add(event.name)
            keystrokes.append({'name': event.name, 'event': 'keydown', 'elapsed_time': elapsed_time})
        elif event.event_type == keyboard.KEY_UP:
            pressed_keys.discard(event.name)
            keystrokes.append({'name': event.name, 'event': 'keyup', 'elapsed_time': elapsed_time})

        if "ctrl" in pressed_keys and "e" in pressed_keys:
            ctrl_e_count += 1
            print(f"¡Combinación de teclas detectada: Ctrl + E! (Conteo: {ctrl_e_count})")

        last_time = current_time

    keyboard.hook(mostrar_tecla)
    keyboard.wait('esc')

    with open(f"{macro_name}.json", "w") as file:
        json.dump(keystrokes, file, indent=4)

    print(f"Macro guardada en {macro_name}.json.")

def main():
    grabar_teclas()

if __name__ == "__main__":
    main()
