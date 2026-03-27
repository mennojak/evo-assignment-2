from evaluation import GenerationResult
from models.graph import Graph
from models.solution import Solution
from vertex_descent_algohrithm import local_search_vertex_descent
from utils import create_copy_of_vertices, copy_graph_vertices_grouped_by_color

import random
import time
import csv


def iterated_local_search(
    graph_name: str,
    colors: int,
    descent_cycles: int,
    max_iterations: int,
    perturbation_strength: int
) -> tuple[Solution, list[GenerationResult]]:

    graph = Graph()
    graph.create_from_file(graph_name)

    generation_results: list[GenerationResult] = []

    current = multi_start_initialization(graph, colors, descent_cycles, tries=10)
    best = copy_solution(current)

    no_improvement_counter = 0
    max_strength = 50

    for iteration in range(max_iterations):

        candidate = copy_solution(current)

        # Perturbation
        escape_local_optimum(candidate, perturbation_strength)

        # Local search
        candidate = run_vertex_descent(candidate, descent_cycles)


        # Update best
        if candidate.conflicts_amount < best.conflicts_amount:
            best = copy_solution(candidate)
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        # Adaptivly try to escape the local optimum by increasing the steps out of the local optimum if we are stuck for too long
        if no_improvement_counter >= 50:
            perturbation_strength = min(perturbation_strength + 5, max_strength)
            no_improvement_counter = 0
            print(f"Increasing perturbation to {perturbation_strength}")


        current = candidate

        generation_results.append(
            GenerationResult(
                generation_number=iteration,
                best_penalty=float(best.conflicts_amount),
                average_penalty=float(current.conflicts_amount)
            )
        )

        if iteration % 100 == 0:
            print(
                f"Iteration {iteration} - Best: {best.conflicts_amount} - Current: {current.conflicts_amount} - Perturbation: {perturbation_strength}"
            )

        if best.conflicts_amount == 0:
            break

    return best, generation_results



def multi_start_initialization(graph: Graph, colors: int, descent_cycles: int, tries: int) -> Solution:
    best = None

    for _ in range(tries):
        g_copy = Graph()
        g_copy.create_from_vertices(
            create_copy_of_vertices(graph.vertices),
            {}
        )

        s = Solution(g_copy, colors, create_random=True)
        s = run_vertex_descent(s, descent_cycles)

        if best is None or s.conflicts_amount < best.conflicts_amount:
            best = s

    return best


def run_vertex_descent(solution: Solution, descent_cycles: int) -> Solution:
    for _ in range(descent_cycles):
        before = solution.conflicts_amount

        solution = local_search_vertex_descent(solution)
        solution.graph.update_vertices_grouped_by_color()

        # Stop when no strict improvement
        if solution.conflicts_amount >= before:
            break

    return solution


def escape_local_optimum(solution: Solution, strength: int):
    vertices = solution.graph.vertices
    conflict_vertices = [v for v in vertices if v.amount_of_conflicts > 0]

    for _ in range(strength):

        # Mix strategy: sometimes global, sometimes conflict-based
        if conflict_vertices and random.random() < 0.5:
            v = random.choice(conflict_vertices)
        else:
            v = random.choice(vertices)

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


# Comparison function gls and ils.
from gls_algorithm import genetic_local_search
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

        # GLS
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

        # ILS
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