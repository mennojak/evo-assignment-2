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
        start_time = time.time()
        best_solution, generation_results = genetic_local_search("data/flat300_26_0.col", colors, population_size, descent_cycles)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
        evaluation.plot()

    if choice == "2":
        colors = int(input("Enter number of colors (minimum 83): "))
        population_size = 50
        descent_cycles = 100
        start_time = time.time()
        best_solution, generation_results = genetic_local_search("data/flat1000_76_0.col", colors, population_size, descent_cycles)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
        evaluation.plot()

if __name__ == "__main__":    
    main()