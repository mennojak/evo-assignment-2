import random

from models.graph import Graph
from models.solution import Solution
from models.vertex import Vertex
from vertex_descent_algohrithm import local_search_vertex_descent
from utils import copy_graph_vertices_grouped_by_color, create_copy_of_vertices

def genetic_local_search(graph: Graph, colors: int, population_size: int, descent_cycles: int = 100, max_generations: int = 10) -> Solution:
    
    best_solution = None

    population = []
    for _ in range(population_size):
        solution = Solution(graph, colors)
        population.append(solution)


    for _ in range(max_generations):

        if optimal_solution_found(best_solution):
            break

        # Greedy Partitioning Crossover
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        child = greedy_partitioning_crossover(parent1, parent2)


        # Vertex descent
        for _ in range(descent_cycles):
            child = local_search_vertex_descent(child)
            child.graph.update_vertices_grouped_by_color()


        worst_solution: Solution = max(population, key=lambda s: s.conflicts_amount)
        if child.conflicts_amount <= worst_solution.conflicts_amount:
            population.remove(worst_solution)
            population.append(child)

    return best_solution

def greedy_partitioning_crossover(parent1: Solution, parent2: Solution) -> Solution:
    parent1_grouped_vertices_by_color: dict[int, list[int]] = copy_graph_vertices_grouped_by_color(parent1.graph)
    parent2_grouped_vertices_by_color: dict[int, list[int]] = copy_graph_vertices_grouped_by_color(parent2.graph)

    child_structure: list[Vertex] = create_copy_of_vertices(parent1.graph.vertices)
    child_grouped_vertices_by_color: dict[int, list[int]] = partition_parents(parent1_grouped_vertices_by_color,parent2_grouped_vertices_by_color)

    child = Solution(child_structure,child_grouped_vertices_by_color)


    return child
                                                                     
    
def partition_parents(parent1: dict[int, list[int]], parent2: dict[int, list[int]]) -> dict[int, list[int]]:
    
    child_grouped_vertices_by_color: dict[int, list[int]] = {}
    
    # TODO

    return child_grouped_vertices_by_color
    


def optimal_solution_found(solution: Solution) -> bool:
    return solution.conflicts_amount == 0

