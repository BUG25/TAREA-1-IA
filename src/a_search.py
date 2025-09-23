import math
import heapq
from queue import PriorityQueue
#Implementación inspirada en https://www.geeksforgeeks.org/dsa/a-search-algorithm/

# Se define la clase celda
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Costo desde el inicio hasta esta celda
        self.h = 0  # Coste heurístico de llegar desde esta celda hasta el destino

class a_star_agent:
    def __init__(self, grid, inicio, metas):
        self.grid = grid
        self.inicio = inicio
        self.pos = inicio #Posición del agente
        self.camino = []
        self.cola_metas = PriorityQueue()
        for meta in metas:
            self.cola_metas.put((self.calculate_h_value(inicio[0], inicio[1], meta), meta))
        _, self.meta = self.cola_metas.get()

    #Se calcula el valor h usando una heurística manhattan
    def calculate_h_value(self, row, col, dest):
        return abs(row - dest[0]) + abs(col - dest[1])

    #Se verifica si la celda está bloqueada
    def is_unblocked(self, grid, estado):
        if grid[estado[0]][estado[1]] > 0:
            return True
        else: 
            return False
    #Se verifica si la celda es válida
    def is_valid(self, grid, estado):
        return 0 <= estado[0] < len(grid) and 0 <= estado[1] < len(grid[0])
    
    #Se verifica si la celda es el destino
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    # Se traza camino desde el inicio hasta el destino
    def trace_path(self, cell_details, dest):
        #print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]

        # Se traza el camino utilizando los padres de las celdas, comenzando desde el destino
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Se añade la celda de inicio al camini
        path.append((row, col))
        # Se invierte el camino para que tenga un orden desde el inicio hasta el destino
        path.reverse()

        # Print the path
        #for i in path:
            #print("->", i, end=" ")
        #print()
        return path

    def a_star_search(self, grid, inicio, destino):
        cantidad_filas = len(grid)
        cantidad_columnas = len(grid[0])
        # Se inicializa la lista cerrada en donde se almacenarán las celdas visitadas
        closed_list = [[False for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]
        # Se inicializa un objeto celda por cada celda en la grilla
        celdas = [[Cell() for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]

        #Se establecen los valores de la celda de inicio
        celdas[inicio[0]][inicio[1]].parent_i = inicio[0]
        celdas[inicio[0]][inicio[1]].parent_j = inicio[1]
        celdas[inicio[0]][inicio[1]].g = 0
        celdas[inicio[0]][inicio[1]].f = 0

        # Inicializa la lista abierta (celdas a ser visitadas) con la celda de inicio   
        open_list = []
        heapq.heappush(open_list, (0.0, inicio[0], inicio[1]))

         # Marcador para determinar si ha encontrado la celda de destino
        found_dest = False

        # Ciclo principal del algoritmo
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Marca la celda como visitada
            i = p[1]
            j = p[2]
            closed_list[i][j] = True
            # Revisar los sucesores en todas las direcciones
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]
                nuevo_estado = (new_i, new_j)
                # Si el sucesor es válido, no está bloqueado y no se ha visitado
                if self.is_valid(grid, nuevo_estado) and self.is_unblocked(grid, nuevo_estado) and not closed_list[new_i][new_j]:
                    if self.is_destination(new_i, new_j, destino):
                        # Se establecen las posiciones de la celda padre
                        celdas[new_i][new_j].parent_i = i
                        celdas[new_i][new_j].parent_j = j
                        #print("The destination cell is found")
                        # Se llama trace_path para obtener el camino a seguir
                        camino = self.trace_path(celdas, destino)
                        found_dest = True
                        return camino
                    else:
                        #  Se calculan los nuevos valores para g, h y f
                        g_new = celdas[i][j].g + grid[new_i][new_j]
                        h_new = self.calculate_h_value(new_i, new_j, destino)
                        f_new = g_new + h_new

                        # Si la celda no está en la lista abierta o el nuevo valor f es menor
                        if celdas[new_i][new_j].f == float('inf') or celdas[new_i][new_j].f > f_new:
                            # Se añade la celda a la lista abierta
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Se actualizan los atributos de la celda
                            celdas[new_i][new_j].f = f_new
                            celdas[new_i][new_j].g = g_new
                            celdas[new_i][new_j].h = h_new
                            celdas[new_i][new_j].parent_i = i
                            celdas[new_i][new_j].parent_j = j


        #Imprime si no se ha encontrado la celda de destino
        if not found_dest:
            #print("Failed to find the destination cell")
            return

    def actuar(self, cambio=False):
        #Su no hay camino se intenta calcular uno nuevo
        if not self.camino:
            nuevo_camino = self.a_star_search(self.grid, self.pos, self.meta)
            if not nuevo_camino:
                #print("No hay camino hacia la meta actual")
                return None
            # quitar la posición actual para devolver solo los pasos futuros
            self.camino = nuevo_camino[1:]
        
        if cambio:
            casilla_bloqueada = False #Varíable para detectar si alguna casilla del camino ha sido bloqueada
            for celda in self.camino:
                if not self.is_unblocked(self.grid, celda): #Se detecta si alguna de las casillas está bloqueada
                    casilla_bloqueada = True 
                    break
            if casilla_bloqueada: #Si hay alguna casilla bloqueada se recalcula el camino
                nuevo_camino = self.a_star_search(self.grid, self.pos, self.meta)
                if not nuevo_camino:
                    print("No hay camino hacia la meta después del cambio")
                    return None
                # quitar la posición actual para devolver solo los pasos futuros
                self.camino = nuevo_camino[1:]
                print("Una celda del camino ha sido bloqueada, se recalcula nuevo camino con éxito")
            else:
                print("Ninguna celda ha sido bloqueada, se continua con el camino ya calculado")
        # tomar el siguiente paso
        if self.camino:
            siguiente = self.camino.pop(0)
            self.pos = siguiente
            return siguiente
        return None
    
    def actualizar_meta(self):
        if self.cola_metas.empty():
            print("Ya no quedan metas")
            self.meta = None

        
        metas_restantes = []
        while not self.cola_metas.empty():
            _, meta = self.cola_metas.get()
            metas_restantes.append(meta)
        
        self.cola_metas = PriorityQueue()
        for meta in metas_restantes:
            h = self.calculate_h_value(self.pos[0], self.pos[1], meta)
            self.cola_metas.put((h, meta))

        # La nueva meta será la salida más cercana a la posición actual
        _, self.meta = self.cola_metas.get()
        self.camino = []  # limpiar el camino para que se recalcule en actuar()

