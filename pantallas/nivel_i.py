import copy
import math
import random

import pygame
from pygame.locals import KEYDOWN, K_q, K_p, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_ESCAPE

from castillo import *
from dragon import *
from estados import *
from flecha import *
from jugador import *
from recursos import *

timer = 60
vidas = 5


def play(pantalla, reloj, fuente):
    global timer
    global vidas
    print("juegando")
    fondo = getFondo("nivel_i")

    # dibujar timer
    tiempo_texto = fuente.render(str(timer), None, NEGRO)
    tiempo_rect = tiempo_texto.get_rect()
    tiempo_rect.center = TIMER_CENTER  # lo ubico en esta posicion

    # dibujar puntos
    puntos_texto = fuente.render(str(getPuntajeJugador()), None, NEGRO)
    puntos_rect = puntos_texto.get_rect()
    puntos_rect.center = PUNTOS_CENTER  # lo ubico en esta posicion

    # dibujar castillo
    castillo_img = loadCastillo()
    castillo_rect = castillo_img.get_rect()
    castillo_rect.center = (TAMANIO_PANTALLA[0] - (castillo_rect.width // 2), TAMANIO_PANTALLA[1] - 140)

    # dibujar vidas
    corazones = getVidas(vidas)

    # Dragones
    newDragon(True) #  Crea un nuevo dragón.
    ld = getListaDragones() # Obtiene la lista de dragones actual.

    flecha = loadFlecha(20, TAMANIO_PANTALLA[1] - 120) # Crea una nueva flecha en la posición inicial.

    # dibujo los elem iniciales
    actualizar_superficie(pantalla, fondo, tiempo_texto, tiempo_rect, puntos_texto, puntos_rect, corazones, ld, castillo_img, castillo_rect, flecha, False)

    disparando = False

    timer_event = pygame.USEREVENT + 1 #  Se crea un evento personalizado 
    pygame.time.set_timer(timer_event, 1000) #1000 milis. # evento  para actualizar el temporizador en el juego.
    dragon_event = pygame.USEREVENT + 2 
    pygame.time.set_timer(dragon_event, 3500) # evento para generar nuevos dragones en el juego.
    falling_dragon_event = pygame.USEREVENT + 3 # evento perso
    pygame.time.set_timer(falling_dragon_event, 2000) # dragones existentes caigan en el juego.
    while True:
        reloj.tick(60)
        t = pygame.time.get_ticks() / 980 #  t se utiliza para calcular el tiempo en función de los milisegundos transcurridos.
                                    # ajusto el tiempo
        #si el timer llega a cero o las vidas a cero
        if timer <= 0 or vidas == 0:
            setEstatoJugador("timeout") # se agoto el tiempo
            if vidas == 0:
                setEstatoJugador("dead") # moriste

            setEstado(estatesDic["FINALIZADO"])
            # reestablesco el timer y las vidas
            timer = 60
            vidas = 5
            return True # el juego termino, salir del bucle

        moverDragones()
        actualizar_dragones(pantalla, fondo, getListaDragones())

        detectar_colisiones(pantalla, get_jugador_img(), castillo_img, get_flecha_img(), disparando)

        for evento in pygame.event.get():
            if (evento.type == pygame.QUIT):
                setEstado(estatesDic["SALIR"])
                return True
            if evento.type == timer_event: # paso un segundo
                timer -= 1 # resto temporizador
                tiempo_texto = fuente.render(str(timer), None, NEGRO)
                tiempo_rect.center = TIMER_CENTER
            if evento.type == dragon_event:
                newDragon() # crea un dragon
            if evento.type == falling_dragon_event: # un dragon cae
                drLista = getListaDragones() 
                drLen = len(drLista) # calculo la long
                if drLen >= 2: # si hay al menos 2 dragones en la lista. requerimiento de la caida
                    keys = [i for i in range(1, drLen)] # lista que contiene indx de dragones, lo pongo en 1 porq el primero (0) no cae
                    item = random.choice(keys) # seleccionar al azar un indice, el dragon q cae es al azar
                    setFalling(item) # el dragon debe cambiar su estado a cayendo 
            if evento.type == KEYDOWN:
                if evento.key == K_q:
                    setEstado(estatesDic["SALIR"])
                    return True

                if evento.key == K_ESCAPE:
                    setEstado(estatesDic["FINALIZADO"])
                    timer = 60
                    vidas = 5
                    return True

                if evento.key == K_p:
                    setEstado(estatesDic["PAUSA"])
                    return True
                ## movimientos jugador
                if evento.key == K_RIGHT and not disparando:
                    cambiar_potencia("inc")

                if evento.key == K_LEFT and not disparando:
                    cambiar_potencia("dec")

                if evento.key == K_DOWN and not disparando:
                    cambiar_angulo("down")
                    changeAlpha("down")

                if evento.key == K_UP and not disparando:
                    cambiar_angulo("up")
                    changeAlpha("up")
                # proceso de disparo
                if evento.key == K_SPACE and not disparando: # con el not disparando no se puede disparar otra mientras hay una en vuelo
                    # inicializa direccion de la flecha
                    disparando = True # se disparo una flecha
                    y0 = TAMANIO_PANTALLA[1] - 120 # inicializo pos inicial de la flecha vertical
                    x0 = 20 # horizontal x borde izq
                    disparar(x0, y0, getPotencia(), getAngle(), t) # le paso las posi actual, potencia actual, angulo actual, tiempo actual

        if disparando: # flecha en vuelo
            moverFlecha(t) # nueva posi en funcion del time
            if origen_x(get_x_flecha()) >= TAMANIO_PANTALLA[0] or origen_y(get_y_flecha()) >= TAMANIO_PANTALLA[1] or  y < 0: # verifico si se salio de los limites de la pantalla
                
                disparando = False  # ya no esta en vuelo
                loadFlecha(get_x_jugador(), get_y_jugador()) # cargo la flecha en la ballista nuevamente
        else:
            flecha = loadFlecha(20, TAMANIO_PANTALLA[1] - 120) # si no esta en vuelo esta en esta posi

        corazones = getVidas(vidas) # actualiza la represen grafica de las vidas 
        puntos_texto = fuente.render(str(getPuntajeJugador()), None, NEGRO) # actualizo los puntos
        puntos_rect = puntos_texto.get_rect()
        puntos_rect.center = PUNTOS_CENTER
        actualizar_superficie(pantalla, fondo, tiempo_texto, tiempo_rect, puntos_texto, puntos_rect, corazones, getListaDragones(), castillo_img,
                              castillo_rect, flecha, disparando)
        pygame.display.flip()


def actualizar_tiempo(pantalla, fondo, tiempo_texto, tiempo_rect):
    tiempo_rect.center = TIMER_CENTER
    pantalla.blit(tiempo_texto, tiempo_rect)

# dibujar los cora en las posi correspondientes en la pantalla
def actualizar_vidas(pantalla, corazones):
    for corazon in corazones:
        pantalla.blit(corazon[0], corazon[1]) # img y posi pantalla


def actualizar_jugador(pantalla, fondo, angle, potencia):
    img = loadBallista() # carga las img del jugador
    # itero sobre las img
    for key in img:
        rect = img[key].get_rect()
        rect.x = 10 # posi inicial en x
        # establece la posi en el eje y segun el tipo de img
        if key == "chasis":
            rect.y = TAMANIO_PANTALLA[1] - 105
        elif key == "reda_delantera":
            rect.y = TAMANIO_PANTALLA[1] - 74
            rect.x = 52
        elif key == "rueda_trasera":
            rect.y = TAMANIO_PANTALLA[1] - 68
            rect.x = 24
        elif key == "arco":
            rect.y = TAMANIO_PANTALLA[1] - 120
            rect.x = 20
            if angle != 0: # si el angulo no es 0, rota la imagen del arco
               
                new_center = rect.center
                img[key] = pygame.transform.rotate(img[key], angle)
                rect = img[key].get_rect(center=new_center)

        pantalla.blit(img[key], rect) # dibujo la img del jugador en pantalla

    #carga fuente y renderizo las etiquetas del angulo y potencia
    fuenteData = cargarFuente("Geneva", 14)
    angulo_label = fuenteData.render("Angulo: " + str(angle), None, BLANCO)
    angulo_rect = angulo_label.get_rect()
    angulo_rect.y = TAMANIO_PANTALLA[1] - 45
    angulo_rect.x = 30
    potencia_label = fuenteData.render("Potencia: " + str(potencia), None, BLANCO)
    potencia_rect = potencia_label.get_rect()
    potencia_rect.y = TAMANIO_PANTALLA[1] - 25
    potencia_rect.x = 30

   
    # dibujo las etiquetas
    pantalla.blit(angulo_label, angulo_rect)
    pantalla.blit(potencia_label, potencia_rect)


def actualizar_dragones(pantalla, fondo, dragones):
    for idx, x in enumerate(dragones):  
        frame = getCurrentFrame(idx) # frame actual del dragon
        rect = frame.get_rect()
        rect.y = x[2]
        rect.x = x[3]
        
        pantalla.blit(frame, rect)

# esta función se encarga de actualizar la posición y apariencia de la flecha en la pantalla, considerando su ángulo de disparo y su estado (disparando o no).
def actualizar_flecha(pantalla, x, y, flecha, disparando):
    if disparando: # esto se ejecuta si disparando es verdadera, osea la flecha se esta disparando
        if get_vx_flecha() == 0:
            alpha = 1 # se establece en 1 si la componente x de la velocidad de la flecha es igual a cero para evitar divisiones por cero
        else:
            alpha = atan(get_vy_flecha() / get_vx_flecha()) # en caso contrario se calcula alpha utilizando la función atan para obtener el ángulo correspondiente a las componentes de velocidad de la flecha.
            #  alpha es el ángulo de disparo de la flecha, y su valor se utiliza para determinar la trayectoria y la posición de la flecha en la pantalla.
        coseno_alpha = cos(alpha) #  Estos valores se utilizan para
        seno_alpha = sin(alpha)  #determinar las nuevas coordenadas de la flecha.
        ori_x = origen_x(get_x_flecha() - 20 * coseno_alpha * 1.3) # calculo las nuevas coordenadas de la flecha desp de aplicar desplazamientos basados en el ángulo de disparo.
        ori_y = origen_y(get_y_flecha() - 45 * seno_alpha * 1.3)
        rect = flecha.get_rect() # creo un rect de la imagen de lfecha
        rect.x = ori_x # asigno las nuevas coord. al rect
        rect.y = ori_y
        pantalla.set_at((ori_x, ori_y), ROJO) # se cambia el color del píxel en la posición de la flecha en la pantalla a ROJO.
    else: # si la flecha no esta disparando se obtienen las coord. origin. de la flecha
        rect = flecha.get_rect()
        rect.x = get_x_flecha()
        rect.y = get_y_flecha()

        new_center = rect.center
        flecha.set_at((x, y), ROJO)
        flecha = pygame.transform.rotate(flecha, getAlpha()) # realiza una rotacion en base al angulo de rotacion (getAlpha) y se establecen las nuevas
        rect = flecha.get_rect(center=new_center)

    pantalla.blit(flecha, rect)


# esta función actualiza y dibuja los elementos clave del juego en la pantalla en cada iteración del bucle principal del juego.
def actualizar_superficie(pantalla, fondo, tiempo_texto, tiempo_rect, puntos_texto, puntos_rect, corazones, dragones, castillo_img, castillo_rect, flecha, disparando):
    pantalla.blit(fondo, (0, 0)) # dibuja fondo
    pantalla.blit(tiempo_texto, tiempo_rect) # coloca el texto del tiempo en la pos deter. en la pantalla
    pantalla.blit(puntos_texto, puntos_rect) #  coloca el texto de los puntos en la pantalla.
    pantalla.blit(castillo_img, castillo_rect) # Dibuja la imagen del castillo en la posición determinada 

    angulo = getAngle() # ángulo actual del jugador.
    potencia = getPotencia() # potencia actual del jugador.
    actualizar_jugador(pantalla, fondo, angulo, potencia) #  Llama a la función (actualizar_jugador) para dibujar al jugador en la pantalla con el ángulo y la potencia obtenidos.
    actualizar_flecha(pantalla, get_x_flecha(), get_y_flecha(), flecha, disparando) # llama a otra función (actualizar_flecha) para dibujar la flecha en la pantalla con la posición actual y si está disparando.

    for corazon in corazones:
        pantalla.blit(corazon[0], corazon[1])  # Dibuja los corazones (representando las vidas) en la pantalla.
                    #   img     ,  rect      
    for idx, x in enumerate(dragones): 
        #Itera sobre la lista de dragones y dibuja cada frame del dragón en su posición actual en la pantalla.
        frame = getCurrentFrame(idx)
        rect = frame.get_rect()
        rect.y = x[2] # posic vertical y, en pantalla
        rect.x = x[3] # posic horizontal x, en pantalla
        pantalla.blit(frame, rect)

# preparo el rect de la flecha para la deteccion de colisiones 
def detectar_colisiones(pantalla, jugador, castillo, flecha, disparando):
    global vidas
    flecha_rect = flecha.get_rect() # rect de la imagen
    flecha_rect.width *= 0.1 # lo achico 10% de su tam original, para q la colision sea mejor 
    flecha_rect.height *= 0.1
    flecha_rect.x = get_x_flecha() # establesco posi horiz en pantalla segun la posi de la flecha
    flecha_rect.y = origen_y(get_y_flecha()) # establesco posi verti en la pantalla y convierto en coordenadas la posi y .

    #pygame.draw.rect(pantalla, NARANJA, flecha_rect, 2)

    jugador_rect = jugador.get_rect() # rect de la img
    jugador_rect.y = TAMANIO_PANTALLA[1] - 120 # posi vert
    jugador_rect.x = 20 # posi hor.


    #pygame.draw.rect(pantalla, VERDE, jugador_rect, 2)

    lista_dragones = getListaDragones() 
    for idx, dragon in enumerate(lista_dragones): # obtengo el indice y el obejto en cada itera
        dragon_rect = getFrameRect(index=idx) # frame especif segun el indx pasado
        #pygame.draw.rect(pantalla,  ROJO, dragon_rect, 2)
        if disparando:
            # flecha - dragones
            flecha_dragon_collide = pygame.Rect.colliderect(flecha_rect, dragon_rect)
            if disparando and flecha_dragon_collide:
                remove_de_la_lista(dragon)
                puntaje = getPuntajeJugador()
                setPuntajeJugador(puntaje + 20)

        # dragones - jugador
        jugador_dragon_collide = pygame.Rect.colliderect(jugador_rect, dragon_rect)
        if jugador_dragon_collide:
            remove_de_la_lista(dragon)
            vidas -= 1
            actualizar_vidas(pantalla, getVidas(vidas))

    castillo_rect = castillo.get_rect()
    castillo_rect.center = (TAMANIO_PANTALLA[0] - (castillo_rect.width // 2), TAMANIO_PANTALLA[1] - 140)
    #pygame.draw.rect(pantalla, AZUL, castillo_rect, 2)
    # flecha - castillo
    collide_castillo = pygame.Rect.colliderect(flecha_rect, castillo_rect)
    if collide_castillo:
        setEstatoJugador("win")
        evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        pygame.event.post(evt)
        reproducirSonidoCastilloRoto()
    #pygame.display.flip()
