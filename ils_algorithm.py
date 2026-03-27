# ILS
# - Start with a solution using the generic algorithm.
# - Apply a local search (vertex descent) to the solution until a local minimum is reached.
# - Escape the local optimum.
# - Apply local search again.
# - Accept the solution or reject it.


from evaluation import GenerationResult
from gls_algorithm import genetic_local_search
from models.graph import Graph
from models.solution import Solution
from vertex_descent_algohrithm import local_search_vertex_descent
import random
from utils import create_copy_of_vertices, copy_graph_vertices_grouped_by_color
from models.graph import Graph
from models.solution import Solution


def iterated_local_search(graph_name: str, colors: int, descent_cycles: int, max_iterations: int, perturbation_strength: int) -> tuple[Solution, list[GenerationResult]]:
    generation_results: list[GenerationResult] = []
    graph = Graph()
    graph.create_from_file(graph_name)

    current = Solution(graph, colors, create_random=True)
    current = run_vertex_descent(current, descent_cycles)

    best = copy_solution(current)

    no_improvement_counter = 0

    min_strength = 3
    max_strength = 50

    for iteration in range(max_iterations):

        candidate = copy_solution(current)

        escape_local_optimum(candidate, perturbation_strength)

        candidate = run_vertex_descent(candidate, descent_cycles)


        if candidate.conflicts_amount < best.conflicts_amount:
            best = copy_solution(candidate)
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1


        if no_improvement_counter >= 50:
            new_strength = min(perturbation_strength + 5, max_strength)

            if new_strength > perturbation_strength:
                perturbation_strength = new_strength
                print(f"Increasing perturbation to {perturbation_strength}")

            no_improvement_counter = 0

        # Accept the better candidate
        if candidate.conflicts_amount <= current.conflicts_amount:
            current = candidate

        # To help escape plateaus, also accept worse solutions with a small probability
        elif random.random() < 0.1:
            current = candidate

        generation_results.append(
        GenerationResult(
            generation_number=iteration,
            best_penalty=float(best.conflicts_amount),
            average_penalty=float(current.conflicts_amount) 
        )
)

        if iteration % 100 == 0:
            print(f"Iteration {iteration} - Best: {best.conflicts_amount} - Perturbation: {perturbation_strength}")

        if best.conflicts_amount == 0:
            break

    return best, generation_results

def run_vertex_descent(solution: Solution, descent_cycles: int) -> Solution:
    for _ in range(descent_cycles):
        before = solution.conflicts_amount

        solution = local_search_vertex_descent(solution)
        solution.graph.update_vertices_grouped_by_color()

        if solution.conflicts_amount >= before:
            break

    return solution


def escape_local_optimum(solution: Solution, strength: int):
    conflict_vertices = [v for v in solution.graph.vertices if v.amount_of_conflicts > 0]

    if not conflict_vertices:
        conflict_vertices = solution.graph.vertices

    for _ in range(strength):
        v = random.choice(conflict_vertices)
        v.color = random.randint(0, solution.colors - 1)

    solution.update_conflicts_amount()



def copy_solution(solution: Solution) -> Solution:
    vertices_copy = create_copy_of_vertices(solution.graph.vertices)
    grouped = copy_graph_vertices_grouped_by_color(solution.graph)

    graph_copy = Graph()
    graph_copy.create_from_vertices(vertices_copy, grouped)

    new_solution = Solution(graph_copy, solution.colors)
    new_solution.conflicts_amount = solution.conflicts_amount

    return new_solution


# Notes on ILS and it's behaviour:
# - Many large plateaus. The algorithm can easily get stuck on them and make no progress. 
# I tried implementing the adaptive Iterative local search, where the pertubation (Pertubation is the offical term for escaping the local optimum) strength increases when no improvement is found for a while, 
# and it does help to escape plateaus, but it also makes the search more random and less focused. 
# I find it unclear if it's actually better than a normal Vertex descent algorithm. It seems to be quite equal, both having their own downsides and upsides. 
# 


import csv
import time


def compare_gls_ils(
    graph_name: str,
    colors: int,
    runs: int,
    population_size: int,
    descent_cycles: int,
    max_generations: int,
    ils_iterations: int,
    perturbation_strength: int,
    experiment_name: str
):
    results = []

    for run in range(runs):
        print(f"\n=== Run {run + 1}/{runs} ===")

        # -------------------
        # GLS
        # -------------------
        start = time.time()

        gls_best, gls_history = genetic_local_search(
            graph_name,
            colors,
            population_size,
            descent_cycles,
            max_generations
        )

        gls_time = time.time() - start

        results.append([
            run,
            "GLS",
            gls_best.conflicts_amount,
            gls_history[-1].average_penalty,
            len(gls_history),
            gls_time
        ])

        print(f"GLS -> best: {gls_best.conflicts_amount}, time: {gls_time:.2f}s")

        # -------------------
        # ILS
        # -------------------
        start = time.time()

        ils_best, ils_history = iterated_local_search(
            graph_name,
            colors,
            descent_cycles,
            ils_iterations,
            perturbation_strength
        )

        ils_time = time.time() - start

        results.append([
            run,
            "ILS",
            ils_best.conflicts_amount,
            ils_history[-1].average_penalty,
            len(ils_history),
            ils_time
        ])

        print(f"ILS -> best: {ils_best.conflicts_amount}, time: {ils_time:.2f}s")

    # -------------------
    # Save CSV
    # -------------------
    file_location = f"results/compare_{experiment_name}_colors={colors}.csv"

    with open(file_location, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "run",
            "algorithm",
            "best_conflicts",
            "final_conflicts",
            "iterations",
            "time_seconds"
        ])

        writer.writerows(results)

    print(f"\nSaved comparison to {file_location}")