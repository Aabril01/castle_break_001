import json

from jugador import*


def guardar_datos(vidas, puntaje):
    guardar_datos = {"vidas": vidas, "puntaje": puntaje}
    try:
        with open("datos_juego.json", "w") as file:
            json.dump(guardar_datos, file)
    except Exception as e:
        print("error añ guardar datos:", e)

def cargar_datos():
    try:
        with open("datos_juego.json", "r") as file:
            datos = json.load(file)
            return datos["vidas"], datos["puntaje"]
    except FileNotFoundError:
        return 5, 0  # Valores predeterminados si el archivo no existe