import random
from typing import List, Optional, Tuple
from puzzle import State, Solution, manhattan_distance, apply_moves


MOVES = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']


def _random_chromosome(length: int) -> List[str]:
    # Genera un cromosoma aleatorio de movimientos
    return [random.choice(MOVES) for _ in range(length)]


def _crossover(a: List[str], b: List[str]) -> Tuple[List[str], List[str]]:
    # Realiza cruce de un punto entre dos cromosomas
    if len(a) != len(b) or len(a) == 0:
        return a[:], b[:]
    point = random.randint(1, len(a) - 1)
    return a[:point] + b[point:], b[:point] + a[point:]


def _mutate(ch: List[str], rate: float) -> None:
    # Aplica mutación aleatoria a un cromosoma
    for i in range(len(ch)):
        if random.random() < rate:
            ch[i] = random.choice(MOVES)


def _tournament(pop: List[List[str]], fitness: List[int], k: int) -> List[str]:
    # Selección por torneo: elige el mejor de k individuos aleatorios
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
    Algoritmo genético simple para el puzzle-8, donde cada cromosoma es una secuencia fija de movimientos.
    La aptitud (fitness) es la distancia Manhattan entre el estado alcanzado y el estado meta tras aplicar la secuencia.
    El algoritmo tiene éxito cuando la aptitud es 0 (se alcanza la meta).
    Nodos generados: total de descendientes producidos.
    Nodos expandidos: total de evaluaciones de aptitud realizadas (individuos evaluados).
    """
    # Generar la población inicial de cromosomas aleatorios
    population: List[List[str]] = [_random_chromosome(chrom_len) for _ in range(pop_size)]
    nodes_generated = 0
    nodes_expanded = 0

    # Evaluar la aptitud de la población inicial
    fitness: List[int] = []
    for ch in population:
        end_state, _ = apply_moves(start, ch)
        f = manhattan_distance(end_state, goal)
        fitness.append(f)
        nodes_expanded += 1

    for gen in range(1, generations + 1):
    # ¿Se encontró una solución?
        best_idx = min(range(len(population)), key=lambda i: fitness[i])
        if fitness[best_idx] == 0:
            # Reconstruir la trayectoria con el mejor cromosoma
            _, path_states = apply_moves(start, population[best_idx])
            # Derivar la lista de movimientos hasta llegar a la meta (puede ser menor o igual a chrom_len si llega antes)
            # Recortar los movimientos hasta el punto donde se alcanza el estado meta
            moves: List[str] = []
            for i in range(1, len(path_states)):
                moves.append(population[best_idx][i - 1])
                if path_states[i] == goal:
                    path_states = path_states[: i + 1]
                    break
            return Solution(path_states, moves[: len(path_states) - 1], nodes_generated, nodes_expanded)

    # Crear nueva generación aplicando elitismo
        new_pop: List[List[str]] = []
        new_fit: List[int] = []

    # Elitismo: copiar los mejores individuos según el parámetro 'elitism'
        if elitism > 0:
            order = sorted(range(len(population)), key=lambda i: fitness[i])
            for i in order[: min(elitism, pop_size)]:
                new_pop.append(population[i][:])
                new_fit.append(fitness[i])

        while len(new_pop) < pop_size:
            # Selección por torneo para padres
            p1 = _tournament(population, fitness, tournament_k)
            p2 = _tournament(population, fitness, tournament_k)

            # Cruce de un punto entre los padres
            c1, c2 = _crossover(p1, p2)

            # Aplicar mutación cada m generaciones
            if mutate_every > 0 and (gen % mutate_every == 0):
                _mutate(c1, mutation_rate)
                _mutate(c2, mutation_rate)

            # Evaluar los descendientes y agregarlos a la nueva población
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

    # Reemplazo generacional completo: la nueva población sustituye a la anterior
    population = new_pop
    fitness = new_fit

    # Si no se encontró solución tras todas las generaciones, retorna None
    return None