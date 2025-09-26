import random

DIRECCIONES = ['U', 'D', 'L', 'R']                                         # up, down, left, right
MAPA_DIRECCIONES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}  # diccionario que asocia cada direccióm con un cambio de coordenadas

class AgenteGenetico:
    def __init__(self, cuadricula, inicio, meta, tamaño_poblacion=20, longitud_cromosoma=30, tasa_mutacion=0.1, generaciones=30):
        self.cuadricula = cuadricula
        self.inicio = inicio
        self.meta = meta
        self.tamaño_poblacion = tamaño_poblacion
        self.longitud_cromosoma = longitud_cromosoma                                    # el número de movimientos en cada cromosoma
        self.tasa_mutacion = tasa_mutacion
        self.generaciones = generaciones                                                # número de iteraciones para evolucionar la lista de "cromosomas" (cada cromosoma es una lista de movimientos)
        self.poblacion = [self.cromosoma_aleatorio() for _ in range(tamaño_poblacion)]  # lista de cromosomas 
        self.mejor_cromo = None
        self.mejor_camino = []
        self.indice_turno = 0
        self.evolucionar()

    def cromosoma_aleatorio(self):
        return [random.choice(DIRECCIONES) for _ in range(self.longitud_cromosoma)]  # elegimos cualquier dirección al azar

    def aptitud(self, cromosoma):
        posicion = self.inicio
        visitados = set()                                                                                                    # inicializamos una colección para no repetir posiciones visitadas
        puntaje = 0
        for movimiento in cromosoma:
            nueva_posicion = (posicion[0] + MAPA_DIRECCIONES[movimiento][0], posicion[1] + MAPA_DIRECCIONES[movimiento][1])  # "posicinon[0]" es la fila, "posicion[1]" es la columna
            if not (0 <= nueva_posicion[0] < len(self.cuadricula) and 0 <= nueva_posicion[1] < len(self.cuadricula[0])):     # "si no se cumple que la nueva posicion este dentro de la cuadricula"
                break 
            if self.cuadricula[nueva_posicion[0]][nueva_posicion[1]] == 0:                                                   # "si la nueva posicion es una muralla"
                break
            posicion = nueva_posicion
            puntaje -= 1                                                                                                     # aumenta costo por cada movimiento
            if posicion == self.meta:
                puntaje += 1000                                                                                              # le da muchos puntos si llega
                break
            visitados.add(posicion)

        puntaje -= abs(posicion[0] - self.meta[0]) + abs(posicion[1] - self.meta[1])                                         # le quita la distancia en filas y columnas a la meta
        return puntaje

    def seleccion(self):
        c1, c2 = random.sample(self.poblacion, 2)                 # elegimos muestras al azar (dos cromosomas)
        return c1 if self.aptitud(c1) > self.aptitud(c2) else c2  # retorna el cromosoma con mejor aptitud (mayor puntaje)

    def cruce(self, p1, p2):
        # Mezcla los "genes" de los padres. Elige al azar un punto y combina sus segmentos.
        punto = random.randint(1, self.longitud_cromosoma - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]  # combina ambas mitades

    def mutar(self, cromosoma):
        # genera un cambio aleatorio en el camino de un cromosoma
        return [bit if random.random() > self.tasa_mutacion else random.choice(DIRECCIONES) for bit in cromosoma]

    def evolucionar(self):
        # Crea una nueva población a partir de la actual
        for _ in range(self.generaciones):
            puntajes = [self.aptitud(c) for c in self.poblacion]          # Lista de puntajes
            mejor_indice = puntajes.index(max(puntajes))                  # Extrae el índice del máximo puntaje
            self.mejor_cromo = self.poblacion[mejor_indice]       
            nueva_poblacion = []                                          # A partir de la mejor población crea una nueva

            # Selección, cruce y mutación
            while len(nueva_poblacion) < self.tamaño_poblacion:
                p1, p2 = self.seleccion(), self.seleccion()
                c1, c2 = self.cruce(p1, p2)
                nueva_poblacion.extend([self.mutar(c1), self.mutar(c2)])  # Incluye a la lista de nueva población los cromosomas mutados
            self.poblacion = nueva_poblacion[:self.tamaño_poblacion]      # Aseguramos que la población no debe exceder el tamaño definido

        # Almacena el mejor camino encontrado
        self.mejor_camino = self.decodificar_camino(self.mejor_cromo)
        self.indice_turno = 0

    def decodificar_camino(self, cromosoma):
        # devuelve el camino que hizo el cromosoma
        posicion = self.inicio
        camino = [posicion]
        for movimiento in cromosoma:
            nueva_posicion = (posicion[0] + MAPA_DIRECCIONES[movimiento][0], posicion[1] + MAPA_DIRECCIONES[movimiento][1])
            if not (0 <= nueva_posicion[0] < len(self.cuadricula) and 0 <= nueva_posicion[1] < len(self.cuadricula[0])):
                break
            if self.cuadricula[nueva_posicion[0]][nueva_posicion[1]] == 0:
                break
            posicion = nueva_posicion
            camino.append(posicion)
            if posicion == self.meta:
                break
        return camino

    def actuar(self, cuadricula_cambiada=False):
        # Hace que evolucione si la cuadricula ha cambiado y devuelve la siguiente posición en el mejor camino
        if cuadricula_cambiada:
            self.evolucionar()
        if self.indice_turno < len(self.mejor_camino) - 1: 
            self.indice_turno += 1
            return self.mejor_camino[self.indice_turno]
        return None