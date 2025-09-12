from typing import Dict, List, Optional, Tuple
from puzzle import State, Solution, neighbors, manhattan_distance


def astar(start: State, goal: State) -> Optional[Solution]:
    """
    Algoritmo A* con heurística de Manhattan (h), donde el costo de cada movimiento es 1.
    Utiliza listas ABIERTO y CERRADO, acumula el costo g+h, mantiene la mejor trayectoria a cada estado
    y ordena ABIERTO de forma ascendente por f.
    """
    if start == goal:
        return Solution([start], [], nodes_generated=0, nodes_expanded=0)

    # g: costo desde el estado inicial, f = g + h
    g_score: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[Optional[State], Optional[str]]] = {start: (None, None)}

    # ABIERTO: lista de tuplas (f, g, state)
    def f_of(state: State) -> int:
        # Calcula el valor f para un estado
        return g_score[state] + manhattan_distance(state, goal)

    abierto: List[Tuple[int, int, State]] = [(f_of(start), 0, start)]
    cerrado: Dict[State, bool] = {}  # Estados ya explorados

    nodes_generated = 0
    nodes_expanded = 0

    while abierto:
        # Ordena ABIERTO ascendentemente por f y luego por g (estable)
        abierto.sort(key=lambda x: (x[0], x[1]))
        f_current, g_current, current = abierto.pop(0)

        if current in cerrado:
            continue
        cerrado[current] = True  # Marca el estado como explorado

        # Expande el estado actual
        nodes_expanded += 1

        if current == goal:
            # Reconstruye la trayectoria desde el diccionario parent
            path: List[State] = []
            moves: List[str] = []
            st = current
            while st is not None:
                p, mv = parent[st]
                path.append(st)
                if mv is not None:
                    moves.append(mv)
                st = p
            path.reverse()
            moves.reverse()
            return Solution(path, moves, nodes_generated, nodes_expanded)

        for mv, nb in neighbors(current):
            tentative_g = g_current + 1
            nodes_generated += 1

            if nb in cerrado:
                continue

            # Si esta trayectoria es mejor (menor g), actualiza los valores
            if (nb not in g_score) or (tentative_g < g_score[nb]):
                g_score[nb] = tentative_g
                parent[nb] = (current, mv)
                abierto.append((tentative_g + manhattan_distance(nb, goal), tentative_g, nb))

    # Si no se encuentra solución, retorna None
    return None