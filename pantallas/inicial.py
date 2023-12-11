import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_q, K_j

#from ajustes import *
from estados import *
from recursos import *


def pant_inic(pantalla, reloj, fuente):
    print("pantalla inicial")
    # Obtener el fondo de la función getFondo en el módulo recursos
    fondo = getFondo("menu")

    pygame.mixer.music.load("assets/sonidos/sonido_juego.mp3")
    if sonidoActivo():
         pygame.mixer.music.play()
         icn_sonido = getIcono("sonido_on")
    else:
         pygame.mixer.music.pause()
         icn_sonido = getIcono("sonido_off")
    
    # Crear texto para el botón "Jugar"
    boton = fuente.render("[J] Jugar!", None, AZUL)
    boton_rect = boton.get_rect(center=RECTANGULO_JUEGO.center)
    
    # Crear texto para el botón "Salir"
    boton_salir = fuente.render("[Q] Salir", None, AZUL)
    boton_salir_rect = boton.get_rect(center=RECTANGULO_SALIR.center)

    sonido_rect = icn_sonido.get_rect(center=(TAMANIO_PANTALLA[0] // 3, TAMANIO_PANTALLA[1] // 2.7))
    
    # Actualizar la superficie de la pantalla con el fondo y los botones
    actualizar_superficie(pantalla, fondo, boton, boton_salir,icn_sonido, boton_rect, boton_salir_rect, sonido_rect)

    while True:
        reloj.tick(60)
        # Manejar eventos de pygame
        for evento in pygame.event.get():
            if (evento.type == pygame.QUIT):
                setEstado(estatesDic["SALIR"])
                return True
            if (evento.type == MOUSEBUTTONDOWN):
                if (sonido_rect.collidepoint(pygame.mouse.get_pos())):
                     #alternar_sonido()
                    if sonidoActivo():
                         pygame.mixer.music.play()
                         icn_sonido = getIcono("sonido_on")
                    else:
                         pygame.mixer.music.pause()
                         icn_sonido = getIcono("sonido_off")
                    return True
                if (RECTANGULO_JUEGO.collidepoint(pygame.mouse.get_pos())):
                    pygame.mixer.music.pause()
                    setEstado(estatesDic["JUGANDO"])
                    return True
            if evento.type == KEYDOWN:
                if evento.key == K_q:
                    setEstado(estatesDic["SALIR"])
                    return True

                if evento.key == K_j:
                    setEstado(estatesDic["JUGANDO"])
                    return True
        # Actualizar pantalla
        pygame.display.flip()

# Función para actualizar la superficie de la pantalla con el fondo y los botones
def actualizar_superficie(pantalla, fondo, boton_juego, boton_salir, icono, boton_juego_rect, boton_salir_rect, sonido_rect):
    pantalla.blit(fondo, (0, 0))

    pygame.draw.rect(pantalla, BLANCO, RECTANGULO_JUEGO)
    pygame.draw.rect(pantalla, AZUL, RECTANGULO_JUEGO, 5)

    pantalla.blit(boton_juego, boton_juego_rect)

    pygame.draw.rect(pantalla, BLANCO, RECTANGULO_SALIR)
    pygame.draw.rect(pantalla, AZUL, RECTANGULO_SALIR, 5)

    pantalla.blit(boton_salir, boton_salir_rect)
    pantalla.blit(icono, sonido_rect)
