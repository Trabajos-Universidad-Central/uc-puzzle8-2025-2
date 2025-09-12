from typing import List, Tuple, Optional, Dict
from puzzle import State, Solution, neighbors


def dfs(start: State, goal: State, max_depth: Optional[int] = None, max_nodes: Optional[int] = None) -> Optional[Solution]:
    # Búsqueda en profundidad (DFS)
    if start == goal:
        return Solution([start], [], nodes_generated=0, nodes_expanded=0)

    abierto: List[Tuple[State, Optional[int], Optional[str], int]] = [(start, None, None, 0)]
    visited_depth: Dict[State, int] = {}
    nodes_generated = 0
    nodes_expanded = 0
    explored: List[Tuple[State, Optional[int], Optional[str], int]] = []

    while abierto:
        current, parent_idx, move, depth = abierto.pop()

        # Si el estado ya fue visitado con menor profundidad, lo omitimos
        if current in visited_depth and depth >= visited_depth[current]:
            continue

        idx_current = len(explored)
        explored.append((current, parent_idx, move, depth))
        visited_depth[current] = depth

        if current == goal:
            # Reconstruir la trayectoria y movimientos
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

        if max_depth is not None and depth >= max_depth:
            continue

        nodes_expanded += 1
        succs = neighbors(current)

        # Expandir sucesores
        for mv, st in succs:
            nodes_generated += 1
            if max_nodes is not None and nodes_generated > max_nodes:
                return None
            new_depth = depth + 1
            if (st not in visited_depth) or (new_depth < visited_depth[st]):
                abierto.append((st, idx_current, mv, new_depth))

    # Si no se encuentra solución, retorna None
    return None