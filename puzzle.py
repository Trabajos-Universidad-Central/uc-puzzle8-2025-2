from typing import List, Tuple, Optional, Dict

State = Tuple[int, ...]  # 9-length flat tuple representing the board, 0 is blank


def read_puzzle_file(path: str) -> State:
    numbers: List[int] = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            for p in parts:
                if p.strip():
                    numbers.append(int(p))
            if len(numbers) >= 9:
                break
    if len(numbers) != 9:
        raise ValueError("El archivo debe contener exactamente 9 números (0..8).")
    if set(numbers) != set(range(9)):
        raise ValueError("El archivo debe contener los dígitos 0..8 sin repetir.")
    return tuple(numbers)


def manhattan_distance(state: State, goal: State) -> int:
    pos_goal: Dict[int, Tuple[int, int]] = {v: (i // 3, i % 3) for i, v in enumerate(goal)}
    dist = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        r, c = i // 3, i % 3
        gr, gc = pos_goal[v]
        dist += abs(r - gr) + abs(c - gc)
    return dist


def is_solvable(start: State, goal: State) -> bool:
    def inversions(arr: List[int]) -> int:
        a = [x for x in arr if x != 0]
        inv = 0
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                if a[i] > a[j]:
                    inv += 1
        return inv

    return inversions(list(start)) % 2 == inversions(list(goal)) % 2


def neighbors(state: State) -> List[Tuple[str, State]]:
    idx = state.index(0)
    r, c = divmod(idx, 3)
    nbrs: List[Tuple[str, State]] = []

    def swap(pos_r: int, pos_c: int, move: str):
        j = pos_r * 3 + pos_c
        lst = list(state)
        lst[idx], lst[j] = lst[j], lst[idx]
        nbrs.append((move, tuple(lst)))

    # Order: Arriba, Abajo, Derecha, Izquierda
    if r > 0:
        swap(r - 1, c, 'Arriba')
    if r < 2:
        swap(r + 1, c, 'Abajo')
    if c < 2:
        swap(r, c + 1, 'Derecha')
    if c > 0:
        swap(r, c - 1, 'Izquierda')

    return nbrs


def state_to_str(state: State) -> str:
    rows = []
    for r in range(3):
        row = state[r*3:(r+1)*3]
        rows.append(' '.join('_' if x == 0 else str(x) for x in row))
    return '\n'.join(rows)


class Solution:
    def __init__(self, path: List[State], moves: List[str], nodes_generated: int, nodes_expanded: int):
        self.path = path
        self.moves = moves
        self.nodes_generated = nodes_generated
        self.nodes_expanded = nodes_expanded


def apply_move(state: State, move: str) -> State:
    """Apply a move label to a state if valid; otherwise return the same state."""
    for mv, st in neighbors(state):
        if mv == move:
            return st
    return state


def apply_moves(state: State, moves: List[str]) -> Tuple[State, List[State]]:
    """Apply a sequence of moves, returning final state and the path of states including the start."""
    path = [state]
    cur = state
    for mv in moves:
        cur = apply_move(cur, mv)
        path.append(cur)
    return cur, path
