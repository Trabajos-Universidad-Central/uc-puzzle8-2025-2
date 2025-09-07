# Puzzle8 Métodos de búsqueda

Proyecto de resolución del clásico **Puzzle 8** utilizando algoritmos de búsqueda y heurísticas.

## Descripción

Este proyecto implementa el juego Puzzle 8, donde el objetivo es ordenar una cuadrícula de 3x3 moviendo fichas numeradas del 1 al 8 y un espacio vacío. Se incluyen algoritmos para resolver el puzzle automáticamente.

## Características

- Interfaz para ingresar el estado inicial del puzzle.
- Resolución automática usando algoritmos de búsqueda (BFS, DFS, A*, Ascenso en Colina y algortimo genético).
- Visualización paso a paso de la solución.
- Selección de heurísticas para A* (distancia de Manhattan, número de fichas fuera de lugar).

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/Trabajos-Universidad-Central/uc-puzzle8-2025-2.git
    ```
2. Instala las dependencias si es necesario:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el programa principal:
    ```bash
    python main.py
    ```
2. Ingresa el estado inicial y final del puzzle cuando se solicite.
3. Selecciona el algoritmo y la heurística deseada.

## Estructura del Proyecto

- `main.py`: Archivo principal de ejecución - versión de Python utilizada: 3.12.4
- `puzzle.py`: Lógica del juego y movimientos.
- `searches/`: Implementaciones de los algoritmos de búsqueda.
- `estados_de_prueba/`: Carpeta con ejemplos de estados inicial y final del puzzle en formato `.txt`.
- `README.md`: Documentación del proyecto.

## Ejemplo de archivos de estado

En la carpeta `estados_de_prueba` se incluyen dos archivos de ejemplo:

- `inicial.txt`:
    ```
    1 2 3
    0 5 6
    4 7 8
    ```
- `final.txt`:
    ```
    1 2 3
    4 5 6
    7 8 0
    ```

Cada archivo representa el estado del puzzle como una matriz de 3x3, donde los números están separados por espacios y cada fila en una línea distinta. El número `0` representa el espacio vacío.

Puedes utilizar estos archivos para cargar estados de prueba en el programa principal.
