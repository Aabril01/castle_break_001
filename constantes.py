import pygame

VELOCIDAD = 9
VELOCIDAD_DISPARO = 5
VELOCIDAD_OBJETO = 5  # Ajusta la velocidad según sea necesario

TAMANIO_PANTALLA = (900, 600)

TIMER_CENTER = (TAMANIO_PANTALLA[0] // 2, TAMANIO_PANTALLA[1] // 15)
PUNTOS_CENTER = (TAMANIO_PANTALLA[0] // 15, TAMANIO_PANTALLA[1] // 15)

NEGRO = (0, 0, 0)
NARANJA = (255, 165, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
ROSA = (192,87,169)
CYAN = (0, 255, 255)
AMARILLO = (255, 255, 0)

#  Este objeto representa un rectángulo en una pantalla y se inicializa con cuatro parámetros: la posición 
# horizontal (X), la posición vertical (Y), el ancho y la altura del rectángulo.
# La posición X es el 2.3% del ancho de la pantalla (TAMANIO_PANTALLA[0] // 2.3), la posición Y es el 2.3% de la altura 
# de la pantalla (TAMANIO_PANTALLA[1] // 2.3), el ancho es 150 píxeles y la altura es 75 píxeles.
RECTANGULO_CERRAR = pygame.Rect(TAMANIO_PANTALLA[0] // 2.3, TAMANIO_PANTALLA[1] // 2.3, 150, 75)
RECTANGULO_JUEGO = pygame.Rect(TAMANIO_PANTALLA[0] // 5, TAMANIO_PANTALLA[1] // 2.3, 200, 75)
RECTANGULO_SALIR = pygame.Rect(TAMANIO_PANTALLA[0] // 2, TAMANIO_PANTALLA[1] // 2.3, 200, 75)