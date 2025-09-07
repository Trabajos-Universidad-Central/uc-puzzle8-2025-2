import random
from typing import List, Optional, Tuple
from puzzle import State, Solution, manhattan_distance, apply_moves


MOVES = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']


def _random_chromosome(length: int) -> List[str]:
    return [random.choice(MOVES) for _ in range(length)]


def _crossover(a: List[str], b: List[str]) -> Tuple[List[str], List[str]]:
    if len(a) != len(b) or len(a) == 0:
        return a[:], b[:]
    point = random.randint(1, len(a) - 1)
    return a[:point] + b[point:], b[:point] + a[point:]


def _mutate(ch: List[str], rate: float) -> None:
    for i in range(len(ch)):
        if random.random() < rate:
            ch[i] = random.choice(MOVES)


def _tournament(pop: List[List[str]], fitness: List[int], k: int) -> List[str]:
    idxs = random.sample(range(len(pop)), k=min(k, len(pop)))
    best = min(idxs, key=lambda i: fitness[i])
    return pop[best][:]


def genetic_simple(
    start: State,
    goal: State,
    pop_size: int = 100,
    chrom_len: int = 30,
    generations: int = 200,
    mutate_every: int = 1,
    mutation_rate: float = 0.1,
    tournament_k: int = 3,
    elitism: int = 2,
) -> Optional[Solution]:
    """
    Algoritmo genético simple para puzzle-8, cromosoma = secuencia de movimientos fija.
    Fitness = distancia Manhattan del estado alcanzado tras aplicar la secuencia al estado inicial.
    Éxito cuando fitness = 0 (se alcanza la meta).
    Nodos generados = total de descendientes producidos.
    Nodos expandidos = evaluaciones de fitness (individuos) realizadas.
    """
    # Población inicial
    population: List[List[str]] = [_random_chromosome(chrom_len) for _ in range(pop_size)]
    nodes_generated = 0
    nodes_expanded = 0

    # Evaluar población inicial
    fitness: List[int] = []
    for ch in population:
        end_state, _ = apply_moves(start, ch)
        f = manhattan_distance(end_state, goal)
        fitness.append(f)
        nodes_expanded += 1

    for gen in range(1, generations + 1):
        # ¿Solución encontrada?
        best_idx = min(range(len(population)), key=lambda i: fitness[i])
        if fitness[best_idx] == 0:
            # reconstruir trayectoria con el mejor
            _, path_states = apply_moves(start, population[best_idx])
            # derivar lista de movimientos hasta llegar a meta (puede ser <= chrom_len si llega antes)
            # recortar movimientos hasta el punto donde el estado sea la meta
            moves: List[str] = []
            for i in range(1, len(path_states)):
                moves.append(population[best_idx][i - 1])
                if path_states[i] == goal:
                    path_states = path_states[: i + 1]
                    break
            return Solution(path_states, moves[: len(path_states) - 1], nodes_generated, nodes_expanded)

        # Nueva generación con elitismo
        new_pop: List[List[str]] = []
        new_fit: List[int] = []

        # Elitismo: copiar los mejores 'elitism' individuos
        if elitism > 0:
            order = sorted(range(len(population)), key=lambda i: fitness[i])
            for i in order[: min(elitism, pop_size)]:
                new_pop.append(population[i][:])
                new_fit.append(fitness[i])

        while len(new_pop) < pop_size:
            # Selección por torneo
            p1 = _tournament(population, fitness, tournament_k)
            p2 = _tournament(population, fitness, tournament_k)

            # Cruce de un punto
            c1, c2 = _crossover(p1, p2)

            # Mutación cada m generaciones
            if mutate_every > 0 and (gen % mutate_every == 0):
                _mutate(c1, mutation_rate)
                _mutate(c2, mutation_rate)

            # Evaluar descendientes y añadir
            end1, _ = apply_moves(start, c1)
            f1 = manhattan_distance(end1, goal)
            nodes_generated += 1
            nodes_expanded += 1
            new_pop.append(c1)
            new_fit.append(f1)

            if len(new_pop) < pop_size:
                end2, _ = apply_moves(start, c2)
                f2 = manhattan_distance(end2, goal)
                nodes_generated += 1
                nodes_expanded += 1
                new_pop.append(c2)
                new_fit.append(f2)

        # Reemplazo generacional completo
        population = new_pop
        fitness = new_fit

    # No convergió a solución
    return None
