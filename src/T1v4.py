import pygame

from dfs import DFS
from servicios import generar_grilla, dibujar_grilla

TAMAÑO_FUENTE = 20
TAMAÑO_CELDA = 60
MARGEN = 2
PADDING_VENTANA = 60
RETARDO_PASO = 1000  # milisegundos entre pasos

def main():
    pygame.init()
    fuente = pygame.font.SysFont("Arial", TAMAÑO_FUENTE)
    reloj = pygame.time.Clock()
    
    # Parámetros de generación de laberintos
    n = 6   # Tamaño de la grilla (NxN)
    k = 3   # Número de salidas
    num_laberintos = 5  # Número total de laberintos
    
    # Genera laberintos aleatorios
    laberintos = []
    for _ in range(num_laberintos):
        inicio, meta, grilla, salidas = generar_grilla(n, k)
        laberintos.append((inicio, meta, grilla, salidas))
    
    # Imprime resultados al iniciar
    print("\n=#= Soluciones encontradas =#=")
    for idx, (inicio, meta, grilla, salidas) in enumerate(laberintos):
        print(f"Laberinto #{idx + 1}")
        resultado_dfs = DFS(inicio, meta, grilla)
        print("DFS:", len(resultado_dfs)-1 if resultado_dfs else "No hay solución\n")

    indice = 0
    modo = 'dfs'
    animando = False
    victoria = False

    inicio, meta, grilla, salidas = laberintos[indice]
    camino = DFS(inicio, meta, grilla)
    camino_visible = camino.copy() if camino else []

    def actualizar_geometria_grilla(grilla):
        ancho = len(grilla[0]) * (TAMAÑO_CELDA + MARGEN) + 2 * PADDING_VENTANA
        alto = len(grilla) * (TAMAÑO_CELDA + MARGEN) + 2 * PADDING_VENTANA
        return pygame.display.set_mode((ancho, alto))

    pantalla = actualizar_geometria_grilla(grilla)
    indice_paso = 0
    ejecutando = True

    while ejecutando:
        dibujar_grilla(pantalla, grilla, inicio, meta, salidas, camino_visible, fuente, modo, indice, len(laberintos), victoria)
        pygame.display.flip()
        reloj.tick(60)

        if animando and camino:                                # Muestra la animación de la solución de cada agente
            if indice_paso < len(camino):
                camino_visible = camino[:indice_paso + 1]
                indice_paso += 1
                pygame.time.delay(RETARDO_PASO)
            else:
                animando = False
                victoria = True

        # Cerramos la ventana si se dal click a la X
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:                # Evento: presionar tecla 'n'
                if evento.key == pygame.K_n and indice < len(laberintos) - 1:
                    # Siguiente laberinto
                    indice += 1
                    inicio, meta, grilla, salidas = laberintos[indice]
                    pantalla = actualizar_geometria_grilla(grilla)
                    camino = DFS(inicio, meta, grilla)
                    indice_paso = 0
                    camino_visible = []  # limpia el camino dibujado
                    animando = False
                    victoria = False
                    
                elif evento.key == pygame.K_b and indice > 0:  # Evento: presionar la tecla 'b'
                    # Laberinto anterior
                    indice -= 1
                    inicio, meta, grilla, salidas = laberintos[indice]
                    pantalla = actualizar_geometria_grilla(grilla)
                    camino = DFS(inicio, meta, grilla)
                    indice_paso = 0
                    camino_visible = []
                    animando = False
                    victoria = False
                    
                elif evento.key == pygame.K_a and camino:      # Evento: presionar la tecla 'a'
                    # Anima solución
                    indice_paso = 0
                    camino_visible = []
                    animando = True
                    victoria = False
                    
                elif evento.key == pygame.K_r:                 # Evento: presionar la tecla 'r'
                    # Regenerar laberinto actual
                    inicio, meta, grilla, salidas = generar_grilla(n, k)
                    laberintos[indice] = (inicio, meta, grilla, salidas)
                    pantalla = actualizar_geometria_grilla(grilla)
                    camino = DFS(inicio, meta, grilla)
                    indice_paso = 0
                    camino_visible = []
                    animando = False
                    victoria = False

    pygame.quit()

if __name__ == "__main__":
    main()