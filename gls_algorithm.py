from models.solution import Solution

def genetic_local_search(graph, colors, population_size, descent_cycles, ils=False):
    
    # Create population of random solutions (colorings)
    population = []
    for _ in range(population_size):
        solution = Solution(graph, colors)
        population.append(solution)

    # For each generation: (set a max number of generations or stop when optimal solution found)
        # Select 2 parents

        # Create 1 child via Crossover (GPX)

        # Local search on that child (vertex descent)

        # Update population (replace worst if offspring is better or equal)

    # Check termination condition (e.g. optimal solution found or max generations reached)

    return best_solution