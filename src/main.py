import time
import copy
import pandas as pd
from a_search import a_star_agent
from laberinto_generator import LaberintoGenerator
from agente_genetico import AgenteGenetico
from servicios import imprimir_grilla

def simulacion(algoritmo_nombre, laberintos, seed, prob_cambio, n):
    """
    Ejecuta la simulación para un algoritmo dado y devuelve el tiempo de ejecución.
    """
    print(f"\n--- EJECUTANDO: {algoritmo_nombre} | Tamaño={n}x{n} | Prob. Cambio={prob_cambio} ---")
    
    start_time = time.time()

    for num_lab, (inicio, meta, grilla, salidas) in enumerate(laberintos):
        print(f"    Laberinto #{num_lab+1}/{len(laberintos)}") 
        generador_cambios = LaberintoGenerator(seed)
        grilla_copia = copy.deepcopy(grilla)

        if algoritmo_nombre == 'A*':
            agente = a_star_agent(grilla_copia, inicio, salidas)
        elif algoritmo_nombre == 'Genetico':
            agente = AgenteGenetico(grilla_copia, inicio, meta)
        else:
            raise ValueError("Nombre de algoritmo no reconocido")

        posicion = inicio
        victoria = False
        casillas_agente = []

        while not victoria:
            if posicion == meta:
                victoria = True
                print(f"{algoritmo_nombre} llegó a la meta")
                continue

            grilla_copia, cambio = generador_cambios.cambiar_murallas(grilla_copia, inicio, meta, salidas, posicion, prob=prob_cambio)

            if algoritmo_nombre == 'A*':
                if posicion in salidas and posicion != meta:
                    agente.actualizar_meta()
                siguiente_paso = agente.actuar(cambio)
            else: # Genetico
                siguiente_paso = agente.actuar(posicion, cambio)
            
            if siguiente_paso is None:
                victoria = True
                print(f"{algoritmo_nombre} no encontró un camino y se detuvo.")
                
            else:
                posicion = siguiente_paso
                casillas_agente.append(posicion)
                imprimir_grilla(grilla_copia, inicio, meta, salidas, casillas_agente, posicion)
    
    end_time = time.time()
    return end_time - start_time


def main():
    # Listas de parámetros a probar
    tamaños_laberinto = [5, 10, 15, 20, 25] # Probar con laberintos de hasta 25x25
    cantidades_laberintos = [10, 20]    # Probar con 10 y 20 laberintos
    probabilidades_cambio = [0.1, 0.3, 0.5]  # Probar con 10%, 30%, 50% de probabilidad de cambiar las murallas

    seed_global = 50

    # Recopilar todos los resultados
    todos_los_resultados = []

    # Bucle principal para los experimentos
    for n in tamaños_laberinto:
        k = n//2 # número de salidas. 
        for num_labs in cantidades_laberintos:
            for prob in probabilidades_cambio:
                # Generar el conjunto de laberintos para esta configuración
                print(f"\nGenerando {num_labs} laberintos de tamaño {n}x{n}...")
                laberinto_gen = LaberintoGenerator(seed_global)
                laberintos = [laberinto_gen.generar_grilla(n, k) for _ in range(num_labs)]

                # Probar A* con la configuración actual
                tiempo_a_star = simulacion('A*', laberintos, seed_global, prob, n)
                todos_los_resultados.append({
                    'algoritmo': 'A*',
                    'num_laberintos': num_labs,
                    'tamaño_laberinto': n,
                    'prob_cambio': prob,
                    'tiempo_total_segundos': tiempo_a_star
                })

                # Probar Genético con la misma configuración
                tiempo_genetico = simulacion('Genetico', laberintos, seed_global, prob, n)
                todos_los_resultados.append({
                    'algoritmo': 'Genetico',
                    'num_laberintos': num_labs,
                    'tamaño_laberinto': n,
                    'prob_cambio': prob,
                    'tiempo_total_segundos': tiempo_genetico
                })

    # Guardar los resultados en un archivo CSV 
    df_resultados = pd.DataFrame(todos_los_resultados)
    nombre_archivo_csv = 'resultados_experimentos.csv'
    df_resultados.to_csv(nombre_archivo_csv, index=False, sep=';')
    
    print(f"\n\nExperimentos completados. Todos los resultados han sido guardados en {nombre_archivo_csv}")
    print("\nResumen de resultados:")
    print(df_resultados)


if __name__ == "__main__":
    main()