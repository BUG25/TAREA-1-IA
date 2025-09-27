import random

DIRECCIONES = ['U', 'D', 'L', 'R']                                         # up, down, left, right
MAPA_DIRECCIONES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}  # diccionario que asocia cada direccióm con un cambio de coordenadas

class AgenteGenetico:
    def __init__(self, cuadricula, inicio, meta, tamaño_poblacion=500, longitud_cromosoma=300, tasa_mutacion=0.15, generaciones=500):
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
        self.mejor_puntaje_historico = float('-inf')
        self.generaciones_sin_mejora = 0
        self.max_generaciones_sin_mejora = 50
        self.evolucionar(self.inicio)

    def cromosoma_aleatorio(self):
        return [random.choice(DIRECCIONES) for _ in range(self.longitud_cromosoma)]  # elegimos cualquier dirección al azar

    def aptitud(self, cromosoma, inicio_simulacion):
        posicion = inicio_simulacion
        visitados = set([inicio_simulacion])                                                                                                    # inicializamos una colección para no repetir posiciones visitadas
        puntaje = 0
        pasos_validos = 0

        for i, movimiento in enumerate(cromosoma):
            nueva_posicion = (posicion[0] + MAPA_DIRECCIONES[movimiento][0], posicion[1] + MAPA_DIRECCIONES[movimiento][1])  # "posicinon[0]" es la fila, "posicion[1]" es la columna

            if not (0 <= nueva_posicion[0] < len(self.cuadricula) and 0 <= nueva_posicion[1] < len(self.cuadricula[0])):     # "si no se cumple que la nueva posicion este dentro de la cuadricula"
                puntaje -= 50
                break 
            if self.cuadricula[nueva_posicion[0]][nueva_posicion[1]] == 0:                                                   # "si la nueva posicion es una muralla"
                puntaje -= 50
                break

            posicion = nueva_posicion
            pasos_validos += 1                                                                                                     # aumenta costo por cada movimiento

            if posicion == self.meta:
                puntaje += 2000                                                                                              # le da muchos puntos si llega
                puntaje += (self.longitud_cromosoma - i) * 5
                break

            puntaje -= 0.5

            if posicion in visitados:
                puntaje -= 3
            else:
                visitados.add(posicion)
                puntaje += 0.5

        distancia_meta = abs(posicion[0] - self.meta[0]) + abs(posicion[1] - self.meta[1])     # le quita la distancia en filas y columnas a la meta
        
        if distancia_meta > 0: 
            puntaje -= distancia_meta * 2
            puntaje += max(0, 20 - distancia_meta)
        
        puntaje += pasos_validos * 0.1
        
        return puntaje

    def seleccion(self, inicio_simulacion):
        c1, c2 = random.sample(self.poblacion, 2)                 # elegimos muestras al azar (dos cromosomas)
        return c1 if self.aptitud(c1, inicio_simulacion) > self.aptitud(c2, inicio_simulacion) else c2  # retorna el cromosoma con mejor aptitud (mayor puntaje)

    def cruce(self, p1, p2):
        # Mezcla los "genes" de los padres. Elige al azar un punto y combina sus segmentos.
        punto = random.randint(1, self.longitud_cromosoma - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]  # combina ambas mitades

    def mutar(self, cromosoma):
        # genera un cambio aleatorio en el camino de un cromosoma
        cromosoma_mutado = []
        for gen in cromosoma:
            if random.random() < self.tasa_mutacion:
                # 30% de probabilidad de mutación dirigida hacia la meta
                if random.random() < 0.3:
                    # Calcular dirección preferida hacia la meta desde posición actual
                    direcciones_preferenciales = DIRECCIONES
                    cromosoma_mutado.append(random.choice(direcciones_preferenciales))
                else:
                    # Mutación aleatoria normal
                    cromosoma_mutado.append(random.choice(DIRECCIONES))
            else:
                cromosoma_mutado.append(gen)
        return cromosoma_mutado


    def evolucionar(self, inicio_camino):
        mejor_puntaje_actual = float('-inf')
        self.generaciones_sin_mejora = 0
        
        for generacion in range(self.generaciones):
            # Calcular aptitudes
            puntajes = [self.aptitud(c, inicio_camino) for c in self.poblacion]
            mejor_indice = puntajes.index(max(puntajes))
            mejor_puntaje_gen = max(puntajes)
            
            # Actualizar mejor cromosoma
            if mejor_puntaje_gen > mejor_puntaje_actual:
                mejor_puntaje_actual = mejor_puntaje_gen
                self.mejor_cromo = self.poblacion[mejor_indice].copy()
                self.generaciones_sin_mejora = 0
                
                # Verificar si encontramos la meta
                camino_actual = self.decodificar_camino(self.mejor_cromo, inicio_camino)
                if len(camino_actual) > 0 and camino_actual[-1] == self.meta:
                    break
            else:
                self.generaciones_sin_mejora += 1
            
            # Criterio de parada por estancamiento
            if self.generaciones_sin_mejora > self.max_generaciones_sin_mejora:
                print(f"Genético: Parada temprana en generación {generacion} por estancamiento")
                break
            
            # Crear nueva población
            nueva_poblacion = []
            
            # Elitismo: mantener los mejores 10%
            puntajes_indices = [(puntajes[i], i) for i in range(len(puntajes))]
            puntajes_indices.sort(reverse=True)
            elite_size = max(1, self.tamaño_poblacion // 10)
            
            for _, idx in puntajes_indices[:elite_size]:
                nueva_poblacion.append(self.poblacion[idx].copy())
            
            # Generar resto de la población
            while len(nueva_poblacion) < self.tamaño_poblacion:
                p1 = self.seleccion(inicio_camino)
                p2 = self.seleccion(inicio_camino)
                c1, c2 = self.cruce(p1, p2)
                nueva_poblacion.extend([
                    self.mutar(c1), 
                    self.mutar(c2)
                ])
            
            self.poblacion = nueva_poblacion[:self.tamaño_poblacion]
        
        # Almacenar el mejor camino encontrado
        self.mejor_camino = self.decodificar_camino(self.mejor_cromo, inicio_camino)
        self.indice_turno = 0

    def decodificar_camino(self, cromosoma, inicio_camino):
        posicion = inicio_camino
        camino = [posicion]
        
        for movimiento in cromosoma:
            nueva_posicion = (posicion[0] + MAPA_DIRECCIONES[movimiento][0], 
                             posicion[1] + MAPA_DIRECCIONES[movimiento][1])
            
            # Verificar límites
            if not (0 <= nueva_posicion[0] < len(self.cuadricula) and 
                   0 <= nueva_posicion[1] < len(self.cuadricula[0])):
                break
                
            # Verificar muralla
            if self.cuadricula[nueva_posicion[0]][nueva_posicion[1]] == 0:
                break
                
            posicion = nueva_posicion
            camino.append(posicion)
            
            # Si llegamos a la meta, terminar
            if posicion == self.meta:
                break
                
        return camino

    def actuar(self, pos_actual, cuadricula_cambiada=False):
        # 1. Si el laberinto cambió, es obligatorio re-planificar desde donde estamos.
        if cuadricula_cambiada:
            self.evolucionar(pos_actual)

        # 2. Si después de todo, no tenemos un plan viable, nos rendimos.
        #    Un plan no es viable si no existe, o si solo contiene la posición inicial.
        if not self.mejor_camino or len(self.mejor_camino) <= 1:
            print("Genético: No se encontró un camino válido. Atascado.")
            return None

        # 3. Si nos hemos quedado sin pasos en nuestro plan actual, nos rendimos.
        #    Esto evita el bucle de re-planificación infinita.
        if self.indice_turno >= len(self.mejor_camino) - 1:
            print("Genético: Se acabó el plan y no se llegó a la meta. Atascado.")
            return None

        # 4. Si todo está en orden, avanza al siguiente paso del plan.
        self.indice_turno += 1
        siguiente_pos = self.mejor_camino[self.indice_turno]

        # 5. Verificación de seguridad: si el siguiente paso ahora es una pared, re-planifica.
        if self.cuadricula[siguiente_pos[0]][siguiente_pos[1]] == 0:
            print(f"Genético: Siguiente posición {siguiente_pos} bloqueada por una nueva pared. Re-planificando...")
            self.evolucionar(pos_actual)
            # Después de re-planificar, intenta moverse de nuevo en el siguiente turno.
            # Devuelve la posición actual para no perder un turno.
            return pos_actual

        return siguiente_pos