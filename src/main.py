import pygame
from dfs import DFS
from servicios import generar_grilla, dibujar_grilla, cambiar_murallas

TAMAÑO_FUENTE = 20
TAMAÑO_CELDA = 60
MARGEN = 2
PADDING_VENTANA = 60
RETARDO_PASO = 200  # milisegundos entre pasos

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
    ultimo_tiempo_cambio = pygame.time.get_ticks()

    inicio, meta, grilla, salidas = laberintos[indice]
    camino = DFS(inicio, meta, grilla)
    camino_visible = []

    def actualizar_geometria_grilla(grilla):
        ancho = len(grilla[0]) * (TAMAÑO_CELDA + MARGEN) + 2 * PADDING_VENTANA
        alto = len(grilla) * (TAMAÑO_CELDA + MARGEN) + 2 * PADDING_VENTANA
        return pygame.display.set_mode((ancho, alto))

    pantalla = actualizar_geometria_grilla(grilla)
    indice_paso = 0
    ejecutando = True

    while ejecutando:
        tiempo_actual = pygame.time.get_ticks()

        # Cambiar las murallas de forma periodica
        if tiempo_actual - ultimo_tiempo_cambio > 100:  # "si hay 100 ticks de diferencia"
            grilla = cambiar_murallas(grilla, inicio, meta, salidas)
            ultimo_tiempo_cambio = tiempo_actual

            # Recalcular camino cuando cambian las murallas
            nuevo_camino = DFS(inicio, meta, grilla)

            if nuevo_camino != camino: 
                camino = nuevo_camino
                if animando:
                    # Si se estaba animando y cambio el camino, reiniciar el camino
                    indice_paso = 0
                    camino_visible = []
                else: 
                    # si no se esta animando, mostrar el camino completo
                    camino_visible = camino.copy() if camino else []
        
        if animando and camino: 
            if indice_paso < len(camino):
                camino_visible = camino[:indice_paso + 1]
                
                # Para avanzar al siguiente paso solo si ha pasado suficiente tiempo 
                if tiempo_actual % RETARDO_PASO < 16: # casi cada RETARDO_PASO ms
                    indice_paso += 1
            else: 
                animando = False
                victoria = True if camino else False
        elif not animando: 
            # si no se esta animando, mostrar el camino completo si es que hay uno
            camino_visible = camino.copy() if camino else []
            victoria = True if camino else False
        

        dibujar_grilla(pantalla, grilla, inicio, meta, salidas, camino_visible, fuente, modo, indice, len(laberintos), victoria)
        pygame.display.flip()
        reloj.tick(60)


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
                    ultimo_tiempo_cambio = pygame.time.get_ticks()
                    
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
                    ultimo_tiempo_cambio = pygame.time.get_ticks()

                    
                elif evento.key == pygame.K_a and camino:      # Evento: presionar la tecla 'a'
                    # Activar/desactivar animación
                    if not animando:
                        indice_paso = 0
                        camino_visible = []
                        animando = True
                        victoria = False
                    else:
                        animando = False
                        camino_visible = camino.copy() if camino else []
                        victoria = True if camino else False
                    
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
                    ultimo_tiempo_cambio = pygame.time.get_ticks()

    pygame.quit()

if __name__ == "__main__":
    main()