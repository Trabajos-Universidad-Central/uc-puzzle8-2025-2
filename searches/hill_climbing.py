from typing import List, Tuple, Optional, Dict
from puzzle import State, Solution, neighbors, manhattan_distance


def hill_climbing(start: State, goal: State, max_nodes: Optional[int] = None) -> Optional[Solution]:
    """
    Ascenso de colina (Hill Climbing) según el pseudocódigo:
    - ABIERTO y CERRADO
    - Quitar primero de ABIERTO
    - Si no en CERRADO: poner en CERRADO, expandir, calcular heurísticas, ordenar asc, mover sucesores al inicio
    Nota: Usamos distancia de Manhattan como heurística.
    """
    if start == goal:
        return Solution([start], [], nodes_generated=0, nodes_expanded=0)

    abierto: List[Tuple[State, Optional[int], Optional[str], int]] = [(start, None, None, 0)]
    cerrado: Dict[State, int] = {}  # guardamos la profundidad alcanzada solo como referencia
    explored: List[Tuple[State, Optional[int], Optional[str], int]] = []
    nodes_generated = 0
    nodes_expanded = 0

    while abierto:
        current, parent_idx, move, depth = abierto.pop(0)

        if current in cerrado:
            continue

        idx_current = len(explored)
        explored.append((current, parent_idx, move, depth))
        cerrado[current] = depth

        if current == goal:
            path_states: List[State] = []
            path_moves: List[str] = []
            i = idx_current
            while i is not None:
                st, p_idx, mv, _ = explored[i]
                path_states.append(st)
                if mv is not None:
                    path_moves.append(mv)
                i = p_idx
            path_states.reverse()
            path_moves.reverse()
            return Solution(path_states, path_moves, nodes_generated, nodes_expanded)

        nodes_expanded += 1
        succs = neighbors(current)
        # calcular heurística para cada sucesor
        scored: List[Tuple[int, Tuple[str, State]]] = []
        for mv, st in succs:
            nodes_generated += 1
            if max_nodes is not None and nodes_generated > max_nodes:
                return None
            h = manhattan_distance(st, goal)
            scored.append((h, (mv, st)))

        if scored:
            # ordenar por heurística ascendente
            scored.sort(key=lambda x: x[0])
            # convertir a lista de entradas y poner al inicio de ABIERTO
            nuevos: List[Tuple[State, Optional[int], Optional[str], int]] = []
            for _, (mv, st) in scored:
                if st in cerrado:
                    continue
                nuevos.append((st, idx_current, mv, depth + 1))
            abierto = nuevos + abierto

    return None

