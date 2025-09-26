import pygame
import copy
from a_search import a_star_agent
from servicios import generar_grilla, dibujar_grilla, cambiar_murallas, imprimir_grilla
from laberinto_generator import LaberintoGenerator


def main():

    # Parámetros de generación de laberintos
    n = 50   # Tamaño de la grilla (NxN)
    k = 3   # Número de salidas
    num_laberintos = 100 # Número total de laberintos
    seed_global =50 #Seed para que los laberintos evolucionen de igual manera para ambos algoritmos
    
    # Genera laberintos aleatorios
    laberintoGenerator = LaberintoGenerator(seed_global) #Clase para generar laberintos que evolucionan de igual manera
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
        generador_a_star = LaberintoGenerator(seed_global)
        grilla_copia = copy.deepcopy(grilla) #Se crea una copia para evitar modificar la original


        a_star = a_star_agent(grilla_copia, inicio, salidas) #Se crea el agente que implementa A*
        grilla_cambio = False #Variable para saber si la grilla ha cambiado después de modificar_murallas
        pos_agente = inicio #Posición actual del agente
        casillas_visitadas = []
        imprimir_grilla(grilla_copia, inicio, meta, salidas, casillas_visitadas, pos_agente)
        victoria = False 

        while victoria == False:
            if pos_agente == meta:
                print("Agente ha llegado a la meta")
                victoria = True
                break
            if pos_agente in salidas and pos_agente != meta:
                print(f"Llegó a salida falsa en {pos_agente}, recalculando meta...")
                a_star.actualizar_meta()

            siguiente_pos = a_star.actuar(grilla_cambio)
            if siguiente_pos is None:
                print("No hay más movimientos posibles.")
                break
            
            pos_agente = siguiente_pos
            casillas_visitadas.append(pos_agente)
            print("Agente se mueve a:", pos_agente)
            imprimir_grilla(grilla_copia, inicio, meta, salidas, casillas_visitadas, pos_agente)

            grilla_copia, grilla_cambio = generador_a_star.cambiar_murallas(grilla_copia, inicio, meta, salidas, pos_agente)
            if grilla_cambio:
                print("El laberinto cambió")
                imprimir_grilla(grilla_copia, inicio, meta, salidas, casillas_visitadas, pos_agente)

            


if __name__ == "__main__":
    main()