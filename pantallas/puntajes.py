import copy

from pygame.locals import KEYDOWN, K_q, K_r

from estados import *
from recursos import *
from jugador import getPuntajeJugador, getEstatoJugador

# Función para mostrar la pantalla de puntuación
def scores(pantalla, reloj, fuente):
    print("pantalla de puntos")
    # Obtener el fondo de la función getFondo en el módulo recursos
    fondo = getFondo("final.jpg")

    # Crear una leyenda con las instrucciones para reiniciar y salir
    instrucciones_center = pygame.Rect(TAMANIO_PANTALLA[0] // 2.3, TAMANIO_PANTALLA[1] // 30, 80, 75)
    instrucciones = fuente.render(" R: REINICIAR - Q: SALIR ", None, AMARILLO)
    instrucciones_rect = instrucciones.get_rect(center=instrucciones_center.center)

    # Obtener el estado y puntaje del jugador
    estadoJugador = getEstatoJugador()
    puntaje = getPuntajeJugador()

    # Definir el texto de la puntuación según el estado del jugador
    if estadoJugador == "timeout":
        score_text = "Tiempo agotado\nTu puntaje es: x\n"
    elif estadoJugador == "dead":
        score_text = "Perdiste! :(\nTu puntaje es: x\n"
    elif estadoJugador == "win":
        score_text = "Has GANADO!!\n Destruiste el castillo!\nTu puntaje es: x\n"

    # Reemplazar la 'x' en el texto de la puntuación con el puntaje real
    score_text = score_text.replace("x", str(puntaje))

    # Crear un texto de puntuación renderizado
    score = fuente.render(score_text, None, AMARILLO)

    # Actualizar la superficie de la pantalla con el fondo, la instruccion y la puntuación
    actualizar_superficie(pantalla, fondo, fuente, instrucciones, instrucciones_rect, score_text)

    while True:
        reloj.tick(60)

        for evento in pygame.event.get():
            if (evento.type == pygame.QUIT):
                setEstado(estatesDic["SALIR"])
                return True
            if (evento.type == KEYDOWN):
                if evento.key == K_q:
                    setEstado(estatesDic["SALIR"])
                    return True
                if evento.key == K_r:
                    setEstado(estatesDic["INICIAL"])
                    return True

        pygame.display.flip()

# Función para actualizar la superficie de la pantalla con el fondo, la instruccion y la puntuación
def actualizar_superficie(pantalla, fondo, fuente, instrucciones, instrucciones_rect, score_text):
    pantalla.blit(fondo, (0, 0))

    # Crear un rectángulo de borde alrededor de la instruccion
    border_rect = copy.deepcopy(instrucciones_rect)
    border_rect.width += 15
    border_rect.height += 15

     # Dibujar el rectángulo de borde alrededor de la leyenda
    pygame.draw.rect(pantalla, NEGRO, border_rect, 0, 15)
    pygame.draw.rect(pantalla, ROJO, border_rect, 4, 15)

    # Mostrar la leyenda en la pantalla
    pantalla.blit(instrucciones, instrucciones_rect)

    # Crear un rectángulo para mostrar la puntuación
    score_rect = pygame.Rect(TAMANIO_PANTALLA[0] // 5, TAMANIO_PANTALLA[1] // 2.3, (TAMANIO_PANTALLA[0] // 5) * 3, 200)

    # Dibujar un rectángulo de borde alrededor de la puntuación
    pygame.draw.rect(pantalla, NEGRO, score_rect, 0, 15)
    pygame.draw.rect(pantalla, ROJO, score_rect, 4, 15)
    # Llamar a la función drawText para mostrar el texto de la puntuación en el rectángulo
    drawText(pantalla, score_text, AMARILLO, score_rect, fuente)

# Función para dibujar texto con salto de línea
def drawText(surface, text, color, rect, font):
    # Convertir el rectángulo pasado como parámetro a un objeto Rect de Pygame
    rect = pygame.Rect(rect)
    
    # Establecer la posición inicial y en qué altura empezar a dibujar el texto
    y = rect.top
    
    # Establecer el espacio vertical entre líneas de texto
    lineSpacing = -2
    
    # Obtener la altura de la fuente (tamaño de fuente)
    fontHeight = font.size("18")

    # Inicializar una lista para almacenar las líneas de texto
    textLines = []

    # Encontrar índices de todos los saltos de línea en el texto
    idx = [i for i in range(len(text)) if text.startswith("\n", i)]
    
    # Inicializar una variable de corte para recorrer el texto
    slice = 0 
    # Esta variable se utiliza para determinar los segmentos del texto entre dos saltos de línea consecutivos y dividirlo en líneas individuales.
    # Si no se utilizara la variable de corte (slice), no se podría rastrear dónde comienza cada nueva línea de texto en el texto original. 
    # El valor de i se utiliza para determinar dónde termina la línea actual, y slice se actualiza para marcar el inicio del próximo segmento.

    # Crear las líneas de texto dividiendo el texto en función de los saltos de línea
    for i in idx:
        textLines.append(text[slice:i]) # Añade cada línea de texto al final de la lista textLines.
        slice = i + 1 # Cada vez que se encuentra un salto de línea, slice se actualiza a i + 1, marcando el inicio del próximo segmento.

    # Dibujar cada línea de texto en la superficie
    for singleLine in textLines:
        # Renderizar cada línea de texto en una superficie
        image = font.render(singleLine, None, color)

        # Dibujar la superficie de texto en la posición adecuada en la superficie principal
        surface.blit(image, (rect.left + (rect.width // 5), y + 15))
        
        # Actualizar la posición vertical para la próxima línea de texto
        y += fontHeight[1] + lineSpacing
