import math
import heapq

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Costo desde el inicio hasta esta celda
        self.h = 0  # Coste heurístico de llegar desde esta celda hasta el destino

class a_star_agent:
    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    def is_unblocked(self, grid, estado):
        if grid[estado[0]][estado[1]] > 0:
            return True
        else: 
            return False
    def is_valid(self, grid, estado):
        return 0 <= estado[0] < len(grid) and 0 <= estado[1] < len(grid[0])
    
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    # Trace the path from source to destination
    def trace_path(self, cell_details, dest):
        print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
        print()
        return path

    def a_star_search(self, grid, inicio, destino):
        cantidad_filas = len(grid)
        cantidad_columnas = len(grid[0])
        # Se inicializa la lista cerrada en donde se almacenarán las celdas visitadas
        closed_list = [[False for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]
        # Initialize the details of each cell
        celdas = [[Cell() for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]

        #Se establecen los valores de la celda de inicio
        celdas[inicio[0]][inicio[1]].parent_i = inicio[0]
        celdas[inicio[0]][inicio[1]].parent_j = inicio[1]
        celdas[inicio[0]][inicio[1]].g = 0
        celdas[inicio[0]][inicio[1]].f = 0

        # Inicializa la lista abierta (celdas a ser visitadas) con la celda de inicio   
        open_list = []
        heapq.heappush(open_list, (0.0, inicio[0], inicio[1]))

         # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True
            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]
                nuevo_estado = (new_i, new_j)
                # If the successor is valid, unblocked, and not visited
                if self.is_valid(grid, nuevo_estado) and self.is_unblocked(grid, nuevo_estado) and not closed_list[new_i][new_j]:
                    if self.is_destination(new_i, new_j, destino):
                        # Set the parent of the destination cell
                        celdas[new_i][new_j].parent_i = i
                        celdas[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and print the path from source to destination
                        camino = self.trace_path(celdas, destino)
                        found_dest = True
                        return camino
                    else:
                        # Calculate the new f, g, and h values
                        g_new = celdas[i][j].g + grid[new_i][new_j]
                        h_new = self.calculate_h_value(new_i, new_j, destino)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if celdas[new_i][new_j].f == float('inf') or celdas[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            celdas[new_i][new_j].f = f_new
                            celdas[new_i][new_j].g = g_new
                            celdas[new_i][new_j].h = h_new
                            celdas[new_i][new_j].parent_i = i
                            celdas[new_i][new_j].parent_j = j


        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")
