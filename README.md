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
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el programa principal:
    ```bash
    python main.py
    ```
2. Ingresa el estado inicial del puzzle cuando se solicite.
3. Selecciona el algoritmo y la heurística deseada.

## Estructura del Proyecto

- `main.py`: Archivo principal de ejecución.
- `puzzle.py`: Lógica del juego y movimientos.
- `algorithms/`: Implementaciones de los algoritmos de búsqueda.
- `heuristics/`: Funciones de heurísticas.
- `README.md`: Documentación del proyecto.
