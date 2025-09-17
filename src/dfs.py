from servicios import obtener_vecinos, obtener_camino_salto

def DFS(inicio, meta, grilla):
    # pila para guardar caminos a explorar
    pila = [(inicio, [inicio])] # (una_posición, camino_para_llegar_a_ella)
    visitados = set()
    
    while pila:
        actual, camino = pila.pop()
        if actual == meta:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        
        # Buscar nuevos caminos
        for vecino in obtener_vecinos(actual, grilla):
            if vecino not in visitados:
                casillas_salto = obtener_camino_salto(actual, vecino)

                if meta in casillas_salto:
                    idx = casillas_salto.index(meta)
                    return camino + casillas_salto[:idx+1]
                nuevo_camino = camino + casillas_salto
                pila.append((vecino, nuevo_camino))
                #visitados.add(vecino)
    
    return None
