from servicios import obtener_vecinos

def DFS(inicio, meta, grilla):
    pila = [(inicio, [inicio])]
    visitados = set()
    
    while pila:
        actual, camino = pila.pop()
        if actual == meta:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        
        for vecino in obtener_vecinos(actual, grilla):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
    
    return None