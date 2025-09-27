import time
import copy
import pandas as pd

from a_search import a_star_agent
from agente_genetico import AgenteGenetico
from laberinto_generator import LaberintoGenerator

def main():
    # Parámetros de generación de laberintos
    n = 10                                                # Tamaño de la grilla (NxN)
    k = 3                                                 # Número de salidas
    num_laberintos = 3                                  # Número total de laberintos
    seed_global = 50                                       #Seed para que los laberintos evolucionen de igual manera para ambos algoritmos
    prob_cambio = 0.1
    # Genera laberintos aleatorios
    laberintoGenerator = LaberintoGenerator(seed_global)  # Clase para generar laberintos que evolucionan de igual manera
    laberintos = []
    for _ in range(num_laberintos):
        inicio, meta, grilla, salidas = laberintoGenerator.generar_grilla(n, k)
        laberintos.append((inicio, meta, grilla, salidas))
    
    resultados = []

    print("\n\n--- INICIANDO PRUEBA PARA A* ---")

    # Medir el tiempo de inicio de A*
    start_time_a_star = time.time()
    #Test para A*
    for num_laberinto,(inicio, meta, grilla, salidas) in enumerate(laberintos):
        print(f"\n=== Laberinto #{num_laberinto+1} ===")
        print("Meta verdadera:", meta)
        print("Salidas:", salidas)
        print("Inicio:", inicio)

        # Reiniciar el generador de cambios para asegurar condiciones idénticas
        generador_cambios = LaberintoGenerator(seed_global)
        grilla_a = copy.deepcopy(grilla) #Se crea una copia para evitar modificar la original

        # Inicializar
        agente_a = a_star_agent(grilla_a, inicio, salidas)
        pos_a = inicio
        victoria_a = False
        #casillas_a = []

        while not victoria_a:
            if pos_a == meta:
                print("A*: llegó a la meta")
                victoria_a = True
                continue # Salta al siguiente ciclo del while (y termina)

            if pos_a in salidas and pos_a != meta:
                agente_a.actualizar_meta()

            # El laberinto cambia ANTES de que el agente decida
            grilla_a, cambio = generador_cambios.cambiar_murallas(grilla_a, inicio, meta, salidas, pos_a, prob_cambio)
            
            siguiente_a = agente_a.actuar(cambio)
            if siguiente_a is None:
                #print("A*: sin más movimientos")
                victoria_a = True
            else:
                pos_a = siguiente_a
                # casillas_a.append(pos_a)
                # print("A* se mueve a:", pos_a)
                # imprimir_grilla(grilla_a, inicio, meta, salidas, casillas_a, pos_a)

    # Medir el tiempo total de A*
    end_time_a_star = time.time()
    tiempo_a_star = end_time_a_star - start_time_a_star
    print(f"\n--- TIEMPO TOTAL PARA A*: {tiempo_a_star:.4f} segundos ---")

    resultados.append({
        'algoritmo': 'A*',
        'num_laberintos': num_laberintos,
        'tamaño_laberinto': n, 
        'prob_cambio': prob_cambio, 
        'tiempo_total_segundos': tiempo_a_star
    })

    print("\n\n--- INICIANDO PRUEBA PARA ALGORITMO GENÉTICO ---")
    # Medir el tiempo de inicio para el Genético
    start_time_genetico = time.time()

    # Bucle exclusivo para el Algoritmo Genético
    for num_laberinto, (inicio, meta, grilla, salidas) in enumerate(laberintos):
        print(f"\n=== Genético | Laberinto #{num_laberinto+1} ===")
        print("Meta verdadera:", meta)
        print("Salidas:", salidas)
        print("Inicio:", inicio)
        
        # Reiniciar el generador de cambios para asegurar condiciones idénticas
        generador_cambios = LaberintoGenerator(seed_global)
        grilla_g = copy.deepcopy(grilla)

        # Inicializar
        agente_g = AgenteGenetico(grilla_g, inicio, meta)
        pos_g = inicio
        victoria_g = False
        #casillas_g = []

        while not victoria_g:
            if pos_g == meta:
                print("Genético: llegó a la meta")
                victoria_g = True
                continue

            grilla_g, cambio = generador_cambios.cambiar_murallas(grilla_g, inicio, meta, salidas, pos_g, prob_cambio)
            
            siguiente_g = agente_g.actuar(pos_g, cambio)
            if siguiente_g is None:
                #print("Genético: sin más movimientos")
                victoria_g = True
            else:
                pos_g = siguiente_g
                # casillas_g.append(pos_g)
                # print("Genético se mueve a:", pos_g)
                # imprimir_grilla(grilla_g, inicio, meta, salidas, casillas_g, pos_g)

    # Medir y mostrar el tiempo total del Genético
    end_time_genetico = time.time()
    tiempo_genetico = end_time_genetico - start_time_genetico
    print(f"\n--- TIEMPO TOTAL PARA GENÉTICO: {tiempo_genetico:.4f} segundos ---")

    resultados.append({
        'algoritmo': 'Genético',
        'num_laberintos': num_laberintos,
        'tamaño_laberinto': n, 
        'prob_cambio': prob_cambio, 
        'tiempo_total_segundos': tiempo_genetico
    })

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv('resultados.csv', index=False, sep=';')
    print(f"\nResultados guardados exitosamente en resultados.csv")

    print("\nResumen de resultados:")
    print(df_resultados)

if __name__ == "__main__":
    main()