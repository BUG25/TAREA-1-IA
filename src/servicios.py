def imprimir_grilla(grilla, inicio, meta, salidas, casillas_visitadas=None, pos_agente=None):
    for i, fila in enumerate(grilla):
        linea = ""
        for j, celda in enumerate(fila):
            pos = (i, j)
            if pos == inicio:
                linea += "\033[94mI\033[0m "   # Azul = Inicio
            elif pos == meta:
                linea += "\033[92mM\033[0m "   # Verde = Meta verdadera
            elif pos_agente and pos == pos_agente:
                linea += "\033[93mA\033[0m "   # Amarillo = Agente
            elif pos in salidas and pos:
                linea += "\033[91mS\033[0m "   # Rojo = salida falsa
            #elif pos in salidas and pos:
                #linea += "\033[48mS\033[0m "   # Naranjo = salida falsa visitada
            elif celda == 0:
                linea += "\033[90m█\033[0m "  # Gris = muro
            #elif pos in casillas_visitadas:
                #linea += "\033[48.\33[0m" # Naranjo = casilla visitada
            else:
                linea += "\033[97m.\033[0m "  # Blanco = camino libre
        print(linea)
    print()  # Salto de línea extra entre grillas