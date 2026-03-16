import random

from models.graph import Graph
from models.solution import Solution
from models.vertex import Vertex
from vertex_descent_algohrithm import local_search_vertex_descent
from utils import copy_graph_vertices_grouped_by_color, create_copy_of_vertices
from evaluation import GenerationResult
import random

def genetic_local_search(graph_name: str, colors: int, population_size: int, descent_cycles: int = 100, max_generations: int = 1000) -> tuple[Solution, list[GenerationResult]]:
    
    best_solution = None
    generation_results: list[GenerationResult] = []

    population = []
    for _ in range(population_size):
        graph = Graph()
        graph.create_from_file(graph_name)
        solution = Solution(graph, colors, create_random=True)
        population.append(solution)

    print("----------------------------------")
    print(f"Initial population created with {population_size} solutions - Vertices: {len(population[0].graph.vertices)} - Edges: {len(population[0].graph.edges)}")
    print("Starting genetic local search, displaying progress every 100 generations...")
    print("----------------------------------")

    for generation in range(max_generations):
        if best_solution and optimal_solution_found(best_solution):
            break

        # Greedy Partitioning Crossover
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        child = greedy_partitioning_crossover(parent1, parent2)

        # Vertex descent
        # descent_cycles_ran = 0
        for i in range(descent_cycles):
            # descent_cycles_ran += 1
            conflicts_before = child.conflicts_amount

            child = local_search_vertex_descent(child)
            # child.graph.update_vertices_grouped_by_color()

            conflicts_after = child.conflicts_amount

            if conflicts_after >= conflicts_before:
                break

        # print(f"Generation {generation}: Ran {descent_cycles_ran} descent cycles.")

        worst_solution: Solution = max(population, key=lambda s: s.conflicts_amount)
        if child.conflicts_amount <= worst_solution.conflicts_amount:
            population.remove(worst_solution)
            population.append(child)

        generation_result = create_generation_result(population, generation)
        generation_results.append(generation_result)

        best_solution = min(population, key=lambda s: s.conflicts_amount)

        if generation % 100 == 0:
            print(f"Generation: {generation} - Best solution: {best_solution.conflicts_amount} - Average solution: {generation_result.average_penalty}")

    return best_solution, generation_results

def greedy_partitioning_crossover(parent1: Solution, parent2: Solution) -> Solution:
    parent1_grouped_vertices_by_color: dict[int, list[int]] = copy_graph_vertices_grouped_by_color(parent1.graph)
    parent2_grouped_vertices_by_color: dict[int, list[int]] = copy_graph_vertices_grouped_by_color(parent2.graph)

    child_structure: list[Vertex] = create_copy_of_vertices(parent1.graph.vertices)
    child_grouped_vertices_by_color: dict[int, list[int]] = partition_parents(parent1_grouped_vertices_by_color,parent2_grouped_vertices_by_color, parent1.colors)

    child_graph = Graph()
    child_graph.create_from_vertices(child_structure, child_grouped_vertices_by_color)
    child_solution = Solution(child_graph, parent1.colors)
    child_solution.update_conflicts_amount()

    return child_solution

def partition_parents(parent1: dict[int, list[int]], parent2: dict[int, list[int]], colors: int) -> dict[int, list[int]]:
    
    all_vertices = {v for group in parent1.values() for v in group}
    
    child: dict[int, list[int]] = {}
    assigned_vertices = set()

    for color_index in range(colors):
        active = parent1 if color_index % 2 == 0 else parent2
        fallback = parent2 if color_index % 2 == 0 else parent1

        parent_source = active if active else fallback
        if not parent_source:
            break

        largest_color = max(parent_source, key=lambda c: len(parent_source[c]))
        largest_group = set(parent_source[largest_color])

        child[color_index] = list(largest_group)
        assigned_vertices.update(largest_group)

        for parent in (parent1, parent2):
            for color in list(parent.keys()):
                parent[color] = [v for v in parent[color] if v not in largest_group]
                if not parent[color]:
                    del parent[color]

    orphans = all_vertices - assigned_vertices
    for v in orphans:
        target = random.randint(0, colors - 1)
        child[target].append(v)

    return child
    
def optimal_solution_found(solution: Solution) -> bool:
    return solution.conflicts_amount == 0

def create_generation_result(population: list[Solution], generation: int) -> GenerationResult:
    best_solution = min(population, key=lambda s: s.conflicts_amount)
    average_conflicts = sum(s.conflicts_amount for s in population) / len(population)

    return GenerationResult(
        generation_number=generation,
        best_penalty= float(best_solution.conflicts_amount),
        average_penalty=average_conflicts
    )