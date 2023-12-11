from recursos import *

# Inicializar una lista global
castillo = [] # se utilizará para almacenar las imágenes relacionadas con el castillo.

# Definir una función llamada "loadCastillo" que carga las imágenes del castillo
def loadCastillo():
    # Acceder a la lista global "castillo"
    global castillo
    # Obtener sprites del castillo del módulo "recursos" y almacenarlos en la lista "castillo"
    castillo = getSprites("castillo") #  Obtener sprites del castillo utilizando la función getSprites
    # Devolver la imagen inicial del castillo
    return castillo["castillo_ini"]



# Definir una función llamada "getCastillo" que obtiene imágenes del castillo según el estado
def getCastillo(estado=0): # Definir una función llamada "getCastillo" que obtiene imágenes del castillo según el estado proporcionado (por defecto, el estado es 0).
    # Acceder a la lista global "castillo"
    global castillo
     # Verificar el estado del castillo
    if estado == 0:
        # Si el estado es 0, devolver la imagen inicial del castillo
        return castillo["castillo_ini"]
    # Si el estado es diferente de 0, devolver la imagen correspondiente al estado específico
    return castillo["castillo_d" + str(estado)] 
# Devolver la imagen correspondiente al estado específico concatenando la cadena "castillo_d" con el número de estado convertido a cadena. 
# Esto asume que existen claves en el diccionario castillo que siguen el formato "castillo_dX", donde X es el estado.







