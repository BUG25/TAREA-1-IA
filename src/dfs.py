from servicios import obtener_vecinos

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
                pila.append((vecino, camino + [vecino]))
    
    return None