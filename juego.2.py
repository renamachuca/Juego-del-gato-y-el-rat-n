import random

# Definición de las dimensiones del tablero
Filas = 5
Columnas = 5
VACIO = "."
Gato = "G"
Raton = "R"
Salida = "S"

# Creación del tablero
tablero = [[VACIO for _ in range(Columnas)] for _ in range(Filas)]

# Posiciones iniciales del gato y el ratón
Posicion_gato = (0, 0)
Posicion_raton = (4, 4)
Posicion_salida = (random.randint(1, Filas-1), random.randint(1, Columnas-1))

# Colocar el gato y el ratón en el tablero
tablero[Posicion_gato[0]][Posicion_gato[1]] = Gato
tablero[Posicion_raton[0]][Posicion_raton[1]] = Raton
tablero[Posicion_salida[0]][Posicion_salida[1]] = Salida

# Función para verificar si el juego ha terminado
def juego_terminado(tablero):
    for i in range(len(tablero)):
        for k in range(len(tablero[i])):
            if tablero[i][k] == Raton:
                # Verifica si hay un Gato en la posición de arriba, abajo, izquierda y derecha
                if (i > 0 and tablero[i-1][k] == Gato) or \
                    (i < len(tablero) - 1 and tablero[i+1][k] == Gato) or \
                    (k > 0 and tablero[i][k-1] == Gato) or \
                    (k < len(tablero[i]) - 1 and tablero[i][k+1] == Gato):
                    return True
    return False

# Función para imprimir el tablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

# Función específica para obtener los movimientos disponibles del gato (una casilla)
def movimientos_disponibles_gato(tablero, pos_gato):
    movimientos = []
    i, k = pos_gato
    posibles_movimientos = [(i-1, k), (i+1, k), (i, k-1), (i, k+1)]
    for ni, nk in posibles_movimientos:
        if 0 <= ni < len(tablero) and 0 <= nk < len(tablero[0]) and tablero[ni][nk] == VACIO:
            movimientos.append((ni, nk))
    return movimientos

# Función específica para obtener los movimientos disponibles del ratón (una casilla)
def movimientos_disponibles_raton(tablero, pos_raton):
    movimientos = []
    i, k = pos_raton
    posibles_movimientos = [(i-1, k), (i+1, k), (i, k-1), (i, k+1)]
    for ni, nk in posibles_movimientos:
        if 0 <= ni < len(tablero) and 0 <= nk < len(tablero[0]) and tablero[ni][nk] == VACIO:
            movimientos.append((ni, nk))
    return movimientos

# Función para aplicar un movimiento en el tablero
def aplicar_movimiento(tablero, movimiento, jugador, pos_anterior):
    nuevo_tablero = [fila[:] for fila in tablero]
    # Borrar la posición anterior
    if pos_anterior:
        nuevo_tablero[pos_anterior[0]][pos_anterior[1]] = VACIO
    # Aplicar el nuevo movimiento
    i, k = movimiento
    nuevo_tablero[i][k] = jugador
    return nuevo_tablero

# Función para evaluar el tablero para el gato
def evaluar_gato(tablero, pos_gato, pos_raton):
    distancia = abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1])
    return -distancia  # El gato quiere minimizar esta distancia

# Función para evaluar el tablero para el ratón
def evaluar_raton(tablero, pos_raton, pos_salida):
    distancia = abs(pos_raton[0] - pos_salida[0]) + abs(pos_raton[1] - pos_salida[1])
    return -distancia  # El ratón quiere minimizar esta distancia

# Función para encontrar la mejor jugada del gato
def mejor_jugada_gato(tablero, pos_gato, pos_raton):
    mejor_valor = float("-inf")
    mejor_movimiento = None
    for movimiento in movimientos_disponibles_gato(tablero, pos_gato):
        nuevo_tablero = aplicar_movimiento(tablero, movimiento, Gato, pos_gato)
        valor = evaluar_gato(nuevo_tablero, movimiento, pos_raton)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento

# Función para encontrar la mejor jugada del ratón
def mejor_jugada_raton(tablero, pos_raton, pos_salida):
    mejor_valor = float("-inf")
    mejor_movimiento = None
    for movimiento in movimientos_disponibles_raton(tablero, pos_raton):
        nuevo_tablero = aplicar_movimiento(tablero, movimiento, Raton, pos_raton)
        valor = evaluar_raton(nuevo_tablero, movimiento, pos_salida)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento

# Definición de la profundidad
profundidad = 2

# Bucle principal del juego
pos_gato = Posicion_gato
pos_raton = Posicion_raton
pos_salida = Posicion_salida

turnos = 0
while not juego_terminado(tablero) and turnos < 5:
    imprimir_tablero(tablero)

    # Movimiento del gato
    movimiento_gato = mejor_jugada_gato(tablero, pos_gato, pos_raton)
    if movimiento_gato:
        tablero = aplicar_movimiento(tablero, movimiento_gato, Gato, pos_gato)
        pos_gato = movimiento_gato

    if juego_terminado(tablero):
        break

    # Movimiento del ratón
    movimiento_raton = mejor_jugada_raton(tablero, pos_raton, pos_salida)
    if movimiento_raton:
        tablero = aplicar_movimiento(tablero, movimiento_raton, Raton, pos_raton)
        pos_raton = movimiento_raton

    # Verificar si el ratón está al lado de la salida
    if abs(pos_raton[0] - pos_salida[0]) <= 1 and abs(pos_raton[1] - pos_salida[1]) <= 1:
        print("¡El ratón ha escapado!")
        break

    turnos += 1

# Imprimir tablero final y mensaje de fin del juego
imprimir_tablero(tablero)
if juego_terminado(tablero):
    print("¡El gato ha ganado el juego!")
elif turnos >= 5:
    print("¡El ratón ha ganado el juego!")