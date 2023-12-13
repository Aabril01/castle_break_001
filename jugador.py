import math
from math import *

from recursos import *

ballista = []
angle = 30
potencia = 30
puntaje = 0
estato = "Vivo"
dragones_eliminados = 0
# La función carga los sprites asociados al jugador
def loadBallista():
    global ballista
    ballista = getSprites("jugador")
    for key in ballista:
        rect = ballista[key].get_rect() # Para cada sprite del jugador, se obtiene el rectángulo (rect) asociado al sprite utilizando get_rect().
        N_ancho = rect.width * 0.1 # calculo nuevas dimenciones
        N_alto = rect.height * 0.1 # multiplicando el ancho y el alto originales por 0.1, lo que reduce las dimensiones al 10% del tamaño original.
        ballista[key] = pygame.transform.scale(ballista[key], (N_ancho, N_alto)) # escalo el sprite a las nuevas dimenciones
    return ballista

# La función permite cambiar el ángulo global (angle) basándose en la dirección proporcionada. 
def cambiar_angulo(direction="up", step=3): # step = se refiere a la cantidad de cambio que se desea aplicar al ángulo, se puede ajustar este valor al llamar a la función para controlar la velocidad o magnitud del cambio en el ángulo.
    global angle
    if direction == "up": #  el ángulo se incrementa
        angle += step
    else:
        angle -= step #  el ángulo se decrementa


def getAngle():
    global angle
    return angle

# Modificar la potencia del jugador 
def cambiar_potencia(direction="inc", step=3):
    global potencia
    if direction == "inc":
        potencia += step
    else:
        potencia -= step

def getPotencia():
    global potencia
    return potencia

# Establece el puntaje del jugador
def setPuntajeJugador(nuevo_puntaje):
    global puntaje
    puntaje = nuevo_puntaje


def getPuntajeJugador():
    global puntaje
    return puntaje

# Establece el estado del jugador
def setEstatoJugador(nuevo_estato):
    global estato
    estato = nuevo_estato


def getEstatoJugador():
    global estato
    return estato

# Retorna la posición en el eje x del sprite del jugador ("arco").
def get_x_jugador():
    global ballista
    return ballista["arco"].get_rect().x

# Retorna la posición en el eje y del sprite del jugador ("arco").
def get_y_jugador():
    global ballista
    return ballista["arco"].get_rect().y

# Retorna la imagen (superficie) asociada al sprite del jugador ("arco").
def get_jugador_img():
    global ballista
    return ballista["arco"]


def setDragones_eliminados():
    global dragones_eliminados
    dragones_eliminados += 1

def getDragones_eliminados():
    global dragones_eliminados
    return dragones_eliminados