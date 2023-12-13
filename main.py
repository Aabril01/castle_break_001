import sys
import json
from jugador import *
from estados import *
from pantallas import inicial
from pantallas import nivel_i
from pantallas import pausa
from pantallas import puntajes
from recursos import *

pygame.init()

pantalla = pygame.display.set_mode(TAMANIO_PANTALLA)
reloj = pygame.time.Clock()
fuente = cargarFuente("Luminari", 40)
#vidas = 5
while obtenerEstadoActual() != estatesDic["SALIR"]:
    if obtenerEstadoActual() == estatesDic["INICIAL"]:
        inicial.pant_inic(pantalla, reloj, fuente)
    elif obtenerEstadoActual() == estatesDic["JUGANDO"]:
        nivel_i.play(pantalla, reloj, fuente)
    elif obtenerEstadoActual() == estatesDic["PAUSA"]:
        pausa.pant_pausa(pantalla, reloj, fuente)
    elif obtenerEstadoActual() == estatesDic["FINALIZADO"]:
        puntajes.scores(pantalla, reloj, fuente)

    pygame.display.flip()

print("Juego Finalizado")
pygame.quit()
sys.exit(0)