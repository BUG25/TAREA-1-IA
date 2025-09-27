import pygame
import copy
from a_search import a_star_agent
from servicios import cambiar_murallas, imprimir_grilla
from laberinto_generator import LaberintoGenerator
from agente_genetico import AgenteGenetico

def main():
    # Parámetros de generación de laberintos
    n = 10                                                # Tamaño de la grilla (NxN)
    k = 3                                                 # Número de salidas
    num_laberintos = 10                                  # Número total de laberintos
    seed_global = 50                                       #Seed para que los laberintos evolucionen de igual manera para ambos algoritmos
    
    # Genera laberintos aleatorios
    laberintoGenerator = LaberintoGenerator(seed_global)  # Clase para generar laberintos que evolucionan de igual manera
    laberintoGenerator = LaberintoGenerator(seed_global)  # Clase para generar laberintos que evolucionan de igual manera
    laberintos = []
    for _ in range(num_laberintos):
        inicio, meta, grilla, salidas = laberintoGenerator.generar_grilla(n, k)
        laberintos.append((inicio, meta, grilla, salidas))
    
    #Test para A*
    for num_laberinto,(inicio, meta, grilla, salidas) in enumerate(laberintos):
        print(f"\n=== Laberinto #{num_laberinto+1} ===")
        print("Meta verdadera:", meta)
        print("Salidas:", salidas)
        print("Inicio:", inicio)

        grilla_compartida = copy.deepcopy(grilla) #Se crea una copia para evitar modificar la original

        # Inicializar
        agente_a = a_star_agent(grilla_compartida, inicio, salidas)
        agente_g = AgenteGenetico(grilla_compartida, inicio, meta)

        pos_a = inicio
        pos_g = inicio
        victoria_a = False
        victoria_g = False
        casillas_a = []
        casillas_g = [] 
        grilla_cambio = False

        while not (victoria_a and victoria_g):
            # -- A* --
            if not victoria_a:
                if pos_a == meta:
                    print("A*: llegó a la meta")
                    victoria_a = True
                else:
                    if pos_a in salidas and pos_a != meta:
                        print(f"A* llegó a la salida falsa en {pos_a}, recalculando meta...")
                        agente_a.actualizar_meta()

                    siguiente_a = agente_a.actuar(grilla_cambio)
                    if siguiente_a is None:
                        print("A*: sin más movimientos")
                        victoria_a = True
                    else:
                        pos_a = siguiente_a
                        casillas_a.append(pos_a)
                        print("A* se mueve a:", pos_a)
                        imprimir_grilla(grilla_compartida, inicio, meta, salidas, casillas_a, pos_a)
            
            # -- Genético --
            if not victoria_g:
                if pos_g == meta:
                    print("Genético: llegó a la meta")
                    victoria_g = True
                else:
                    siguiente_g = agente_g.actuar(pos_g, grilla_cambio)
                    if siguiente_g is None:
                        print("Genético: sin más movimientos")
                        victoria_g = True
                    else:
                        pos_g = siguiente_g
                        casillas_g.append(pos_g)
                        print("Genético se mueve a:", pos_g)
                        imprimir_grilla(grilla_compartida, inicio, meta, salidas, casillas_a, pos_a)
            

            # -- Cambiar murallas solo si ambos agentes siguen jugando --
            if not victoria_a and not victoria_g:
                grilla_compartida = cambiar_murallas(grilla_compartida, inicio, meta, salidas, prob=0.1)
                grilla_cambio = True
                # Opcional: imprimir la grilla solo cuando cambia
                print("--- El laberinto cambió ---")
                imprimir_grilla(grilla_compartida, inicio, meta, salidas, casillas_a, pos_a)
            else:
                # Si un agente ya ganó, el laberinto no cambia más.
                grilla_cambio = False

if __name__ == "__main__":
    main()