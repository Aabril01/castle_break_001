import math
import time

from jugador import *
from math import *

flechas = [] # lista que contiene la img de la flecha
alpha = 30 # un angulo que representa la inclinacion inicial de la flecha
x = 0 # coord cartesiana ancho.
y = 0 # coord cartesiana alto.     
x0 = 0 # coord de la posic inicial // se usan para calcular el mov de la flecha en el tiempo
y0 = 0  # coord de la posic inicial // se usan para calcular el mov de la flecha en el tiempo
vx = 0 # variacion de x (podria ser delta x ) x seria el valor  para calcular la posi de la flecha
vx0 = 0 # Variables para almacenar las velocidades iniciales en las direcciones x e y.
vy = 0 # variacion de y para calcular la posi de la flecha
vy0 = 0 # Variables para almacenar las velocidades iniciales en las direcciones x e y.
t0 = time.time() # tiempo = t . tiempo inicial
g = 0.98 # gravedad. el valor real es 9,81 m/s pero lo dividi por 100 para q entre en la pantalla


# funcion para inicializar, cargar el sprite y escalar
def loadFlecha(px, py): # los param son los puntos donde la voy a ubicar, en la ballista q es el jugador
    global flechas, alpha
    set_x_flecha(px)
    set_y_flecha(py)
    flechas = getSprites("flecha") # la img la carga desde recursos con la funcion getSprites
    flecha_img = flechas["flecha"] # aca la usa como global ( flechas) para obtener la imagen
    flecha_rect = flecha_img.get_rect()
    N_ancho = flecha_rect.width * 0.1
    N_alto = flecha_rect.height * 0.1
    flecha_img = pygame.transform.scale(flecha_img, (N_ancho, N_alto))
    flecha_rect.x = get_x_flecha()
    flecha_rect.y = get_y_flecha()
    return flecha_img

# esta función proporciona acceso a la imagen de la flecha almacenada en la variable global flechas.
def get_flecha_img():
    global flechas
    return flechas["flecha"]

# esta función permite ajustar el ángulo de la flecha hacia arriba o hacia abajo según la dirección especificada y el tamaño del paso (step).
def changeAlpha(direction="up", step=3): # para opcio. definidos por defecto 
    global alpha
    if direction == "up": # si es true se incrementa de a 3
        alpha += step
    else:
        alpha -= step

# si en algún lugar necesito conocer el ángulo actual de la flecha
def getAlpha():
    global alpha
    return alpha

# modifico el valor de la var global . osea llamo a setAlpha(45) y alpha se establece en 45
def setAlpha(angulo):
    global alpha
    alpha = angulo

# ----- simulacion de lanzamiento de flecha desde posi inicial --------
# func para calcular valores iniciales de fisica  con trigonometria
def disparar(xi, yi, potencia, angulo, t): # xinicial  yinical t = tiempo de get_ticks
    global x, y, x0, y0, vx, vy, vx0, vy0, t0
    # kinematics
    setAlpha(angulo) #  Establece el ángulo de la flecha usando la funcion, que a su vez modifica la variable glogal
    x0 = xi * cos(angulo * pi / 180) * 1.1 # Calcula la componente x de la posición inicial teniendo en cuenta el ángulo y un factor de escala.
    y0 = yi * sin(angulo * pi / 180) * 1.1 
    vx0 = potencia * cos(angulo * pi / 180)#  Calcula la componente x de la velocidad inicial utilizando la potencia y el ángulo.
    vy0 = potencia * sin(angulo * pi / 180)
    t0 = t # tiempo. Actualiza el tiempo inicial (t0) con el tiempo proporcionado como argumento.
    set_x_flecha(origen_x(x0)) # Establecer la posición inicial de la flecha
    set_y_flecha(origen_y(y0))
    vx = vx0# Establecer las componentes iniciales de la velocidad (vx y vy) con las velocidades calculadas.
    vy = vy0

# va recalculando los valores para x e y para redibujar la flecha en la nueva posi
def moverFlecha(t):  # animar el vuelo de la flecha en el juego si no se va al chori
    # la fun calcula y actualiza las posi y veloci de la flecha en funcion del tiempo, simulando el movimiento con la gravedad
    global g, x, y, x0, y0, vx0, vy0, vx, vy, t0
    x = (x0 + vx0 * (t - t0)) # Calcula la nueva posición horizontal (x) de la flecha
    # utilizando la fórmula de posición en el movimiento rectilíneo uniforme (MRU), 
    # donde x0 es la posición inicial, vx0 es la velocidad inicial en la dirección x, y (t - t0) representa el intervalo de tiempo.
    y = (y0 + vy0 * (t - t0) - g / 2 * (t - t0) ** 2) #  Calcula la nueva posición vertical 
    # utilizando la fórmula de posición en el movimiento uniformemente acelerado (MUA), donde y0 es la posición inicial, vy0 es la velocidad inicial en la dirección y, g es la aceleración debida a la gravedad, y (t - t0) es el intervalo de tiempo. La parte g / 2 * (t - t0) ** 2 representa la contribución de la aceleración gravitatoria a la posición vertical.
    vx = vx0 # Actualiza la velocidad en la dirección x. En este caso, la velocidad en la dirección x se mantiene constante. 
    vy = vy0 - g * (t - t0) #  Actualiza la velocidad en la dirección y considerando la aceleración debida a la gravedad. La velocidad en la dirección y disminuye con el tiempo debido a la influencia de la gravedad.


# actualizar la posi horiz de la flecha, asignandole un nuevo valor pasado como argum
def set_x_flecha(new_x):
    global x # se utiliza globalmente para almacenar y mantener la posición horizontal actual de la flecha.
    x = new_x

# lo mismo per vertical
def set_y_flecha(new_y):
    global y
    y = new_y

# esta función devuelve la posición horizontal actual de la flecha, redondeada al entero más cercano.
def get_x_flecha():
    global x
    return round(x)

# lo mismo pero vertical
def get_y_flecha():
    global y
    return round(y)

# esta función proporciona acceso al valor actual de la componente horizontal de la velocidad de la flecha
def get_vx_flecha():
    global vx
    return vx

# lo mismo verti
def get_vy_flecha():
    global vy
    return vy

def origen_x(x): # convierte el valor de la variable x a un entero utilizando la función int() y luego devuelve ese valor entero.
    return int(x) # Si x ya es un entero, la función simplemente devuelve el mismo valor entero.


#  ajuste de las coordenadas y en función del tamaño de la pantalla
def origen_y(y): # toma un valor "y" (una coord) lo resta del tam de la pantalla en la dimencion y
    return int(TAMANIO_PANTALLA[1] - y) # convierte el resul a entero y lo devuelve


#  # (angulo * pi / 180) convierte el angulo de grados a radianes, porque cos de la biblio math tiene q estar en radianes
 #   cos(angulo * pi / 180) Calcula el coseno del ángulo convertido a radianes.
#xi * cos(angulo * pi / 180)  # # Esto proporciona la componente x o y de la posición inicial ajustada por el ángulo.
# yi * sin(angulo * pi / 180) * 1.1 # al multiplicar por el escalar ajusta aun mas la posi inicial en direccion x o y 

# el MRU se refiere al movimiento de un objeto que se desplaza en línea recta (rectilíneo) y a una velocidad constante (uniforme) en el tiempo. 
# el MUA se refiere al movimiento de un objeto que se desplaza en línea recta y experimenta una aceleración constante. 