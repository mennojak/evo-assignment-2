from models.graph import Graph
from models.solution import Solution
from vertex_descent_algohrithm import local_search_vertex_descent

def genetic_local_search(graph: Graph, colors: int, population_size: int, descent_cycles: int, ils: bool = False):
    
    best_solution = None

    # Create population of random solutions (colorings)
    population = []
    for _ in range(population_size):
        solution = Solution(graph, colors)
        population.append(solution)

    # For each generation: (set a max number of generations or stop when optimal solution found)
        # Select 2 parents

        # Create 1 child via Crossover (GPX)

        # Local search on that child (vertex descent)

        new_solution = local_search_vertex_descent(solution)
        new_solution.graph.update_vertices_grouped_by_color()

        # Update population (replace worst if offspring is better or equal)

    # Check termination condition (e.g. optimal solution found or max generations reached)

    return best_solution