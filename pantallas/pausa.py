import pygame
from pygame.locals import KEYDOWN, K_c, K_q, MOUSEBUTTONDOWN

from recursos import *
from estados import *
#from ajustes import *

# Función para mostrar la pantalla de pausa
def pant_pausa(pantalla, reloj, fuente):
    print("pantalla de pausa")
     # Obtener el fondo de la función getFondo en el módulo recursos
    fondo = getFondo("pausa")

    if sonidoActivo():
         icn_sonido = getIcono("sonido_on")
    else:
         icn_sonido = getIcono("sonido_off")

    # Crear texto para el botón "Cerrar"
    boton = fuente.render("Cerrar", None, AZUL)
    boton_rect = boton.get_rect(center=RECTANGULO_CERRAR.center)

    sonido_rect = icn_sonido.get_rect(center=(TAMANIO_PANTALLA[0] // 3, TAMANIO_PANTALLA[1] // 2.7))

    # Actualizar la superficie de la pantalla con el fondo y el botón
    actualizar_superficie(pantalla, fondo, boton, icn_sonido, boton_rect, sonido_rect)

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
                if evento.key == K_c:
                    setEstado(estatesDic["JUGANDO"])
                    return True

            if (evento.type == MOUSEBUTTONDOWN):
                if (boton_rect.collidepoint(pygame.mouse.get_pos())):
                    setEstado(estatesDic["JUGANDO"])
                    return True
                if (sonido_rect.collidepoint(pygame.mouse.get_pos())):
                    if sonidoActivo():
                         pygame.mixer.music.play()
                         icn_sonido = getIcono("sonido_on")
                    else:
                         pygame.mixer.music.pause()
                         icn_sonido = getIcono("sonido_off")
                    return True

        pygame.display.flip()

# Función para actualizar la superficie de la pantalla con el fondo y el botón
def actualizar_superficie(pantalla, fondo, boton, icono, boton_rect, sonido_rect):
    pantalla.blit(fondo, (0, 0))

    pygame.draw.rect(pantalla, BLANCO, RECTANGULO_CERRAR)
    pygame.draw.rect(pantalla, AZUL, RECTANGULO_CERRAR, 5)

    pantalla.blit(boton, boton_rect)
    pantalla.blit(icono, sonido_rect)