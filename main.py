import time
from models.graph import Graph 
from gls_algorithm import genetic_local_search
from evaluation import EvaluationResult

def main():
    print("Select experiment:")
    print("1 - flat300 with 26+ colors- section 2")
    print("2 - flat1000 with 83+ colors - section 3")
    print("3 - flat300 with 26+ colors varying population size and descent cycles - section 4.1")
    print("4 - flat1000 with 83+ colors, population size and descent cycles based on experiment 3 - section 4.2")
    print("5 - flat300 with 26+ colors test ILS using Vertex descent - section 4.3")
    print("6 - flat1000 with 83+ colors test ILS using Vertex descent (only if experiment 5 successful) - section 4.3")
    print("7 - Custom experiment: TBD - section 4.4")


    choice = input("Enter 1-9: ")

    if choice == "1":
        colors = int(input("Enter number of colors (minimum 26): "))
        population_size = 50
        descent_cycles = 100
        max_generations = 100000
        start_time = time.time()
        best_solution, generation_results = genetic_local_search("data/flat300_26_0.col", colors, population_size, descent_cycles, max_generations)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
        evaluation.plot()

    if choice == "2":
        colors = int(input("Enter number of colors (minimum 83): "))
        population_size = 100
        descent_cycles = 200
        max_generations = 25000
        start_time = time.time()
        best_solution, generation_results = genetic_local_search("data/flat1000_76_0.col", colors, population_size, descent_cycles, max_generations)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 2, colors, population_size, descent_cycles)
        evaluation.plot()

    if choice == "3":
        colors = int(input("Enter number of colors (minimum 26 or 83): "))
        population_size = int(input("Enter population size (e.g. 20, 50, 100): "))
        descent_cycles = int(input("Enter descent cycles (e.g. 20, 50, 100): "))
        max_generations = 100000
        graph = input("Choose graph: 'small' for flat300, 'large' for flat1000: ")
        if graph == "small":
            graph = "data/flat300_26_0.col"
        elif graph == "large":
            graph = "data/flat1000_76_0.col"

        start_time = time.time()
        best_solution, generation_results = genetic_local_search(graph, colors, population_size, descent_cycles, max_generations)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
        evaluation.plot()

if __name__ == "__main__":    
    main()