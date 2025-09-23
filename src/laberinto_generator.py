import random

class LaberintoGenerator:
    
    def __init__(self, seed=None) :
        self.seed = seed
        self.random = random.Random(seed)  # generador independiente

    def generar_grilla(self, n, k, probabilidad_muralla=0.3):
        # Genera una grilla NxN aleatoria con murallas y k salidas
        # Con el valor "1" todas las casillas son transitables (inicialmente)
        grilla = [[self.random.randint(1, n//2) for _ in range(n)] for _ in range(n)]
        
        # Genera murallas
        for i in range(n):
            for j in range(n):
                if self.random.random() < probabilidad_muralla:
                    grilla[i][j] = 0 # (valor 0 representa muralla)
        
        # Se asegura de que el inicio y al menos k celdas sean usables (valor >= 1)
        inicio = (0, 0)
        grilla[inicio[0]][inicio[1]] = 1
        
        # Genera k salidas potenciales
        salidas = []
        intentos = 0
        while len(salidas) < k and intentos < 100:
            i = self.random.randint(0, n-1)
            j = self.random.randint(0, n-1)
            # Si la casilla NO ha sido designada como "estado de inicio" o "muralla"
            if (i, j) != inicio and grilla[i][j] != 0 and (i, j) not in salidas:
                salidas.append((i, j))
                #grilla[i][j] = random.randint(1, n//2) # Asigna un valor de salto aleatorio a la salida
            intentos += 1
        
        # Garantiza que la función cumpla con generar las k salidas después de los 100 intentos
        while len(salidas) < k:
            for i in range(n):
                for j in range(n):
                    if (i, j) != inicio and grilla[i][j] != 0 and (i, j) not in salidas:
                        salidas.append((i, j))
                        grilla[i][j] = self.random.randint(1, n//2)
                        if len(salidas) == k:
                            break
                if len(salidas) == k:
                    break
        
        # Elije una salida válida aleatoriamente
        meta_valida = self.random.choice(salidas)
        
        return inicio, meta_valida, grilla, salidas
    
    def cambiar_murallas(self, grilla, inicio, meta, salidas, pos_agente, prob=0.1):
        n = len(grilla)
        i = self.random.randint(0, n-1)
        j = self.random.randint(0, n-1) 
        cambio = False #Variable que devuelve si el laberinto cambió o no
        # No mutar inicio ni meta ni las salidas ficticias
        if (i, j) == inicio or (i, j) == meta or (i, j) == pos_agente or (i, j) in salidas:
            return grilla, cambio
        if grilla[i][j] == 0:
            # Muralla puede abrirse
            if self.random.random() < prob:
                grilla[i][j] = self.random.randint(1, n//2)
                cambio = True
        else:
            # Celda libre puede volverse muralla
            if self.random.random() < prob:
                grilla[i][j] = 0
                cambio = True
        return grilla, cambio
