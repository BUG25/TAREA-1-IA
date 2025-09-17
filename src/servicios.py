import pygame
import random

TAMAÑO_CELDA = 60
MARGEN = 2
PADDING_VENTANA = 60

# Colores para la grilla
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
BROWN = (139, 69, 19)  


# === FUNCIONES DE GRILLA Y VECINOS ===

def generar_grilla(n, k, probabilidad_muralla=0.3):
    # Genera una grilla NxN aleatoria con murallas y k salidas
    # Con el valor "1" todas las casillas son transitables (inicialmente)
    grilla = [[random.randint(1, n//2) for _ in range(n)] for _ in range(n)]
    
    # Genera murallas
    for i in range(n):
        for j in range(n):
            if random.random() < probabilidad_muralla:
                grilla[i][j] = 0 # (valor 0 representa muralla)
    
    # Se asegura de que el inicio y al menos k celdas sean usables (valor >= 1)
    inicio = (0, 0)
    grilla[inicio[0]][inicio[1]] = 1
    
    # Genera k salidas potenciales
    salidas = []
    intentos = 0
    while len(salidas) < k and intentos < 100:
        i = j = random.randint(0, n-1)
        # Si la casilla NO ha sido designada como "estado de inicio" o "muralla"
        if (i, j) != inicio and grilla[i][j] != 0:
            salidas.append((i, j))
            #grilla[i][j] = random.randint(1, n//2) # Asigna un valor de salto aleatorio a la salida
        intentos += 1
    
    # Garantiza que la función cumpla con generar las k salidas después de los 100 intentos
    while len(salidas) < k:
        for i in range(n):
            for j in range(n):
                if (i, j) != inicio and grilla[i][j] != 0 and (i, j) not in salidas:
                    salidas.append((i, j))
                    grilla[i][j] = random.randint(1, n//2)
                    if len(salidas) == k:
                        break
            if len(salidas) == k:
                break
    
    # Elije una salida válida aleatoriamente
    meta_valida = random.choice(salidas)
    
    return inicio, meta_valida, grilla, salidas

def obtener_vecinos(posicion, grilla):
    m, n = len(grilla), len(grilla[0]) # filas y columnas
    i, j = posicion
    
    # Si es una muralla no tiene vecinos
    if grilla[i][j] == 0:
        return []
    
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # arriba, abajo, izq, der
    
    vecinos = []
    for di, dj in direcciones:
        ni, nj = i + di, j + dj

        # Verificar que la posición esté dentro de los límites
        if 0 <= ni < m and 0 <= nj < n:
            if grilla[ni][nj] != 0: # Verificar que no sea una muralla
                vecinos.append((ni, nj))
    return vecinos

def obtener_camino_salto(desde, hasta):
    i1, j1 = desde
    i2, j2 = hasta
    
    # Calcular la dirección y distancia del salto
    di = i2 - i1
    dj = j2 - j1
    pasos = max(abs(di), abs(dj))
    
    # Si es un movimiento de 1 casilla, solo incluir el destino
    if abs(di) <= 1 and abs(dj) <= 1:
        return [hasta]

    # Determinar la dirección y número de pasos
    camino_salto = []
    
    if di == 0:  # Movimiento horizontal
        pasos = abs(dj)
        direccion_j = 1 if dj > 0 else -1
        for paso in range(1, pasos + 1):
            pos_i = i1
            pos_j = j1 + (paso * direccion_j)
            camino_salto.append((pos_i, pos_j))
    elif dj == 0:  # Movimiento vertical
        pasos = abs(di)
        direccion_i = 1 if di > 0 else -1
        for paso in range(1, pasos + 1):
            pos_i = i1 + (paso * direccion_i)
            pos_j = j1
            camino_salto.append((pos_i, pos_j))
    else:
        # No debería ocurrir en este tipo de laberinto (solo movimientos cardinales)
        return [hasta]
    
    return camino_salto


def dibujar_grilla(pantalla, grilla, inicio, meta, salidas, camino, fuente, modo, indice, total, victoria):
    filas = columnas = len(grilla) # NxN -> le damos el mismo valor a fila y columna
    pantalla.fill(WHITE)

    for i in range(filas):
        for j in range(columnas):
            x = j * (TAMAÑO_CELDA + MARGEN) + PADDING_VENTANA
            y = i * (TAMAÑO_CELDA + MARGEN) + PADDING_VENTANA
            rect = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)

            # Asignación de colores según el tipo de celda
            if grilla[i][j] == 0:  # Muralla
                color = BROWN
            elif (i, j) == inicio:
                color = BLUE
            elif (i, j) == meta:
                color = GREEN
            elif camino and (i, j) in camino:
                color = YELLOW
            elif (i, j) in salidas and (i, j) != meta:
                color = RED  # Salidas no válidas
            else:
                color = GRAY  # Celdas normales

            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, BLACK, rect, 1)  # Dibuja el borde del rectángulo

            # Dibuja el número (valor de salto) solo si no es muralla
            if grilla[i][j] != 0:
                texto = fuente.render(str(grilla[i][j]), True, BLACK)
                texto_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, texto_rect)

    # Muestra información
    texto_modo = fuente.render(f"Modo: {modo.upper()}", True, RED)
    pantalla.blit(texto_modo, (20, 20))

    texto_nivel = fuente.render(f"Laberinto {indice + 1} de {total}", True, BLACK)
    ancho_ventana = pantalla.get_width()
    texto_nivel_rect = texto_nivel.get_rect(topright=(ancho_ventana - 20, 20))
    pantalla.blit(texto_nivel, texto_nivel_rect)

    if victoria:
        texto_victoria = fuente.render("¡Victoria!", True, (0, 180, 0))
        texto_victoria_rect = texto_victoria.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() - 50))
        pantalla.blit(texto_victoria, texto_victoria_rect)
