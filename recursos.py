import pygame.sprite
from pygame import sprite

from constantes import *

sonido_activado = True

# funcion para obtener dif img en dif pantallas del juego
def getFondo(pantalla):
    if pantalla == "menu":
        fondo = pygame.image.load("assets/img/fondos/splash.jpg")
    elif pantalla == "nivel_i":
        fondo = pygame.image.load("assets/img/fondos/landscape.jpg")
    elif pantalla == "final.jpg":
        fondo = pygame.image.load("assets/img/fondos/final.jpg")
    else:  # pausa
        fondo = pygame.image.load("assets/img/fondos/pausa.gif")

    return pygame.transform.scale(fondo, TAMANIO_PANTALLA)


def getIcono(nombre):
    if nombre == "sonido_on":
        return pygame.image.load("assets/iconos/sonido_on.png")
    if nombre == "sonido_off":
        return pygame.image.load("assets/iconos/sonido_off.png")


def sonidoActivo():
    return sonido_activado

# funcion para crear y posicionar imágenes de corazones que representan la cantidad de vidas en un juego.
def getVidas(cantidad): # El parámetro cantidad controla cuántos de los cinco corazones se muestran como llenos (rojos), representando las vidas actuales del jugador.
    corazones = []
    for x in range(5): # 5 vidas
        if x <= cantidad - 1: # si x es menor o igual a la cantidad de vidas menos uno
            vida_img = pygame.transform.scale(pygame.image.load("assets/img/vidas/corazon.png"), (30, 30))
        else:
            vida_img = pygame.transform.scale(pygame.image.load("assets/img/vidas/corazon_black.png"), (30, 30))

        rect_vida = vida_img.get_rect() # rect de la imagen
        corazones.append([vida_img, rect_vida, x]) # Se agrega una lista que contiene la imagen de corazón, su rectángulo y la posición x a la lista corazones.

    corazones[0][1].center = (TAMANIO_PANTALLA[0] // 7, TAMANIO_PANTALLA[1] // 15)  # le paso la cord x = 7 y la cord y = 30 pixeles
    corazones[1][1].center = (TAMANIO_PANTALLA[0] // 6, TAMANIO_PANTALLA[1] // 15)
    corazones[2][1].center = (TAMANIO_PANTALLA[0] // 5.5, TAMANIO_PANTALLA[1] // 15)
    corazones[3][1].center = (TAMANIO_PANTALLA[0] // 5, TAMANIO_PANTALLA[1] // 15)
    corazones[4][1].center = (TAMANIO_PANTALLA[0] // 4.5, TAMANIO_PANTALLA[1] // 15)
    return corazones


def cargarFuente(nombre, size):
    return pygame.font.Font("assets/fuentes/" + nombre + ".ttf", size)

# función utilizada para cargar imágenes asociadas a diferentes personajes del juego.
def getSprites(personaje):
    sprites = {}
    if personaje == "jugador": # ballista
        sprites["chasis"] = pygame.image.load("assets/img/jugador/chassis.png")
        sprites["reda_delantera"] = pygame.image.load("assets/img/jugador/front-wheel.png")
        sprites["rueda_trasera"] = pygame.image.load("assets/img/jugador/backwheel.png")
        sprites["arco"] = pygame.image.load("assets/img/jugador/bow.png")
    elif personaje == "flecha": # flecha
        sprites["flecha"] = pygame.image.load("assets/img/jugador/spear.png")
    elif personaje == "dragon": # dragon
        sprites["dragon"] = pygame.image.load("assets/img/dragon/flying_dragon-red.png").convert()
    elif personaje == "castillo": # casti
        sprites["castillo_ini"] = pygame.image.load("assets/img/castillo/Tower.png")
        sprites["castillo_d1"] = pygame.image.load("assets/img/castillo/Tower_damage1.png").convert()
        sprites["castillo_d2"] = pygame.image.load("assets/img/castillo/Tower_damage2.png").convert()
        sprites["castillo_d3"] = pygame.image.load("assets/img/castillo/Tower_damage3.png").convert()
        sprites["castillo_d4"] = pygame.image.load("assets/img/castillo/Tower_damage4.png").convert()

    return sprites


# funcion para dividir una imagen en una matriz de frames, y opcionalmente, aplicar transformaciones como volteo y escalado a cada frame. 
def toMatrix(image, columnas, filas, flip=False, scale=1): # flip es el booleano que indica si se debe aplicar volteo, y scale es un factor de escala
    lista = []
    # Se calculan las dimensiones de cada frame y las dimensiones escaladas basándose en el número de columnas y filas.
    ancho_frame = int(image.get_width() / columnas)
    alto_frame = int(image.get_height() / filas)
    ancho_scaled = int(ancho_frame * scale)
    alto_scaled = int(alto_frame * scale)

    # Se utiliza un bucle anidado para iterar sobre las filas y columnas especificadas.
    for fila in range(filas):
        row = []
        for columna in range(0, columnas):
            x = columna * ancho_frame # Se calculan las coordenadas x para definir la región de la imagen original que se tomará como un frame.
            y = fila * alto_frame # se calculan las coordenadas y para definir la región de la imagen original que se tomará como un frame.
            frame = image.subsurface(x, y, ancho_frame, alto_frame) #  utiliza el método subsurface para extraer el frame de la imagen original.

            if flip: # Si el parámetro flip es True se aplica un volteo horizontal al frame 
                frame = pygame.transform.flip(frame, True, False).convert_alpha()

            if scale != 1: # Si el parámetro scale no es igual a 1, se escala el frame utilizando
                frame = pygame.transform.scale(frame,(ancho_scaled, alto_scaled))

            # Se añade la fila actual (una lista de frames) a la lista lista, que representa la matriz de frames.
            row.append(frame)
        lista.append(row)
    return lista # retorna la matriz de frames generada.


def reproducirSonidoCastilloRoto():
    pygame.mixer.Sound("assets/sonidos/sonido_castillo.mp3").play()