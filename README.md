# Escape del Laberinto Mutante
### Integrantes: 
- Diego Alday
- Gabriel Castillo
- Marcos Martínez

### Instrucciones de uso: 
Una vez clonado el repositorio se debe crear un entorno virtual y activarlo para su ejecución: 
```bash
python -m venv venv
```
- Windows:
```bash
venv\Scripts\activate.bat
```
- Linux/macOS:
```bash
source venv/bin/activate
```

Luego instalar las dependencias necesarias: 
```bash
pip install -r requeriments.txt
```
Una vez hecho los pasos anteriores, se puede ejecutar los tests (desde la carpeta raiz): 
```python
python3 src/main.py
```
Con ello verá por terminal una visualización de cómo se mueve el agente en el laberinto y si este llegó a la meta o no. 

Los datos, como el tiempo en que se tardan en buscar la salida, se van guardando en un archivo csv ('resultados_experimentos.csv').
