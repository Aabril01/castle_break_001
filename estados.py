# Crear un diccionario llamado estatesDic con nombres de estados y sus valores asociados
estatesDic = {
    "INICIAL": 1,
    "JUGANDO": 2,
    "PAUSA": 3,
    "FINALIZADO": 4,
    "SALIR": 0
}

# Inicializar una variable global llamada estadoActual con el valor asociado al estado "INICIAL"
estadoActual = estatesDic["INICIAL"]

# Definir una función llamada obtenerEstadoActual que devuelve el valor de estadoActual
def obtenerEstadoActual():
    return estadoActual

# Definir una función llamada setEstado que actualiza el valor de estadoActual con el valor proporcionado como argumento
def setEstado(estado):
    global estadoActual
    estadoActual = estado