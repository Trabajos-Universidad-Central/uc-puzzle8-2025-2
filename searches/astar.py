from typing import Dict, List, Optional, Tuple
from puzzle import State, Solution, neighbors, manhattan_distance


def astar(start: State, goal: State) -> Optional[Solution]:
    """
    A* con heurística de Manhattan (h), costo de arista = 1 por movimiento.
    Sigue el pseudo: ABIERTO/CERRADO, acumula costo g+h, mantiene la mejor
    trayectoria a cada estado y ordena ABIERTO ascendente por f.
    """
    if start == goal:
        return Solution([start], [], nodes_generated=0, nodes_expanded=0)

    # g: costo desde el inicio, f = g + h
    g_score: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[Optional[State], Optional[str]]] = {start: (None, None)}

    # ABIERTO: lista de tuplas (f, g, state)
    def f_of(state: State) -> int:
        return g_score[state] + manhattan_distance(state, goal)

    abierto: List[Tuple[int, int, State]] = [(f_of(start), 0, start)]
    cerrado: Dict[State, bool] = {}

    nodes_generated = 0
    nodes_expanded = 0

    while abierto:
        # Ordenar ABIERTO ascendentemente por f, luego g (estable)
        abierto.sort(key=lambda x: (x[0], x[1]))
        f_current, g_current, current = abierto.pop(0)

        if current in cerrado:
            continue
        cerrado[current] = True

        # expandir
        nodes_expanded += 1

        if current == goal:
            # reconstruir trayectoria desde parent
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

            # Si esta trayectoria es mejor (menor g), actualizar
            if (nb not in g_score) or (tentative_g < g_score[nb]):
                g_score[nb] = tentative_g
                parent[nb] = (current, mv)
                abierto.append((tentative_g + manhattan_distance(nb, goal), tentative_g, nb))

    return None

