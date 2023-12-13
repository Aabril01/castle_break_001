import random
from recursos import *

lista_dragones = []
ultimAltura = [67, 73, 80]
dragonSprites = []
countCayendo = 0

#creo un nuevo dragon y lo agrego a la lista con sus caracteristicas
def newDragon(init=False): # Si init es False (el valor predeterminado), la función  agrega un nuevo dragón sin reiniciar la lista existente de dragones.
    #la variable init se utiliza para determinar si se debe iniciar una nueva lista de dragones al agregar un dragon nuevo
    global lista_dragones
    global dragonSprites
    global ultimAltura

    if init == True: # si init es true se limpia la lista antes de agregar uno
        lista_dragones = [] # limpio la lista antes de agregar un nuevo dragon 
    altura = int(random.random() * 1.99) # calculo aleatoriamente la altura del nuevo dragon
    dragones = getSprites("dragon") # obtengo los sprites asociados con la entidad "dragon".
    dragonSprites = toMatrix(dragones["dragon"], 3, 4,False,0.3) # obtiene los sprits del dragon y los combierte en una matriz
    
    lista_dragones.append([3, 0, ultimAltura[altura], TAMANIO_PANTALLA[0], False])


def moverDragones():
    global lista_dragones
    global dragonSprites
    global countCayendo
    # asegura que la animación del dragón avance continuamente a través de los frames disponibles, y si llega al final, se reinicie para crear un bucle de animación. 
    # Cada vez que este bloque se ejecuta, se pasa al siguiente frame en la secuencia de animación del dragón.
    for _, dragon in enumerate(lista_dragones): #  La función enumerate se utiliza para obtener tanto el índice como el valor de cada elemento en la lista.
        #  uso  _ como representacion del índice, porque no se utiliza dentro del bucle
        # dragon[1] representa el índice actual del frame (la imagen individual) de animación del dragón.
        if dragon[1] < 2: # verifica si el índice actual es menor que 2, lo que significa que hay más frames disponibles en la secuencia de animación. 
            dragon[1] += 1# Si el índice actual es menor que 2, dragon[1] += 1 incrementa el índice en 1 para cambiar al siguiente frame en la secuencia de animación.
        else:
            dragon[1] = 0 # Si el índice actual ya es 2 o más, significa que hemos llegado al último frame de la secuencia, 
                           #por lo que else: dragon[1] = 0 reinicia el índice a 0, comenzando la animación desde el primer frame.

        surface = dragonSprites[dragon[0]][dragon[1]] # Obtiene la superficie correspondiente al frame de animación actual del dragón y lo asigna a surface
        rect = surface.get_rect() # obtengo el rect de la sup

        if dragon[4]: # dragon 4 = cayendo                                                                                      ()   Esto simula el movimiento hacia 
            dragon[2] += 0.9 # incrementa la posición en el eje y (dragon[2]) en 0.9 unidades. Esto simula la caída del dragón. ()   abajo del dragón durante su caída.

        if dragon[2] > TAMANIO_PANTALLA[1]: # Verifica si la posición en el eje y del dragón es mas alta que la altura de la pantalla
            lista_dragones.remove(dragon)#Si es así, se elimina el dragón de la lista lista_dragones y 
            countCayendo -= 1 # #se decrementa countCayendo, una variable que lleva el seguimiento de la cantidad de dragones que están cayendo.

        dragon[3] -= 1 # el tiempo se decrementa en 1 en cada itera, de este for.
        if dragon[3] == 0 - rect.width: # Verifica si el contador de tiempo ha alcanzado cero menos el ancho del rectángulo asociado al frame actual del dragón
            lista_dragones.remove(dragon) # Si es así, se elimina el dragón de la lista 

#  obtener el frame de animación actual de un dragón específico según su índice en la lista de dragones 
def getCurrentFrame(index): # Es el índice del dragón en la lista de dragones del cual se quiere obtener el frame actual.
    global dragonSprites
    lista = getListaDragones() # Llama a una función que retorna la lista de dragones 
    element = lista[index] # Obtiene el dragón específico de la lista usando su índice.
    surface = dragonSprites[element[0]][element[1]] # Accede a la matriz de sprites (dragonSprites) para obtener el 
    #frame de animación actual del dragón. element[0] se refiere al índice de la lista que representa al dragón en sí, y element[1] es el índice del frame de animación actual del dragón.
    return surface


def getFrameRect(index):
    lista = getListaDragones() # Utiliza información de la lista de dragones 
    element = lista[index] # la posición index para seleccionar un dragón específico
    surface = getCurrentFrame(index) # para obtener la superficie del frame actual
    rect = surface.get_rect() # usa esa info para construir un rect que represnta elem. 3 y 2
    rect.x = element[3] # posicion del frame en pantalla
    rect.y = element[2] # dimenciones del frame en pantalla
    return rect

# la función parece estar destinada a gestionar la eliminación de dragones de la lista, con una consideración especial para aquellos que están "cayendo", actualizando la variable countCayendo
def remove_de_la_lista(item):
    global lista_dragones
    global countCayendo
    if item[4]: # si el quito elemneto de la lista es true
        #countCayendo -= 1 # se decrementa en 1 la variable global
        lista_dragones.remove(item) # la eliminacion del elemento de la lista se realiza mas alla del valor del quinto elemento 

# acceso a la lista de dragones
def getListaDragones():
    global lista_dragones
    return lista_dragones

# cambiar el estado de "cayendo" de un dragón específico en la lista de dragones. 
def setFalling(index):
    global lista_dragones
    global countCayendo
    if index < len(lista_dragones): # and countCayendo < 2: #  Si el índice es válido (menor que la longitud de la lista de dragones) y la cantidad total de dragones que están cayendo es menor que 2
        lista_dragones[index][4] = True # se establece el quinto elemento del dragón en "cayendo" (True) 
        countCayendo += 1 # se incrementa la cuenta total de dragones cayendo.

# La función proporciona una interfaz para obtener la imagen (superficie) asociada al frame de animación actual de un dragón específico.
def getDragonImg(dragon):
    global dragonSprites
    surface = dragonSprites[dragon[0]][dragon[1]] # Se accede a la matriz de sprites dragonSprites para obtener la superficie correspondiente al frame de animación actual del dragón.
    # 0 =  se refiere al índice que representa al dragón en sí en la lista. 1 = se refiere al índice del frame de animación actual del dragón.
    return surface