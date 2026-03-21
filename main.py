import time
from models.graph import Graph 
from gls_algorithm import genetic_local_search
from evaluation import EvaluationResult
import pandas as pd
import matplotlib.pyplot as plt
from run_experiment_3 import run_all_hyperparameter_combinations, run_some_hyperparameter_combinations_average, run_specific_hyperparameter_combinations
from run_experiment_6 import run_specific_tournament_size, run_all_tournament_sizes, run_some_tournament_sizes_average

def main():
    print("Select experiment:")
    print("1 - flat300 with 26+ colors- section 2")
    print("2 - flat1000 with 83+ colors - section 3")
    print("3 - flat300 with 26+ and flat1000 with 83+ colors varying population size and descent cycles - section 4.1")
    print("4 - flat300 with 26+ colors test ILS using Vertex descent - section 4.3")
    print("5 - flat1000 with 83+ colors test ILS using Vertex descent (only if experiment 5 successful) - section 4.3")
    print("6 - Custom experiment: TBD - section 4.4")


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
        max_generations = 5000
        graph = input("Choose graph: 'small' for flat300, 'large' for flat1000: ")
        if graph == "small":
            graph = "data/flat300_26_0.col"
        elif graph == "large":
            graph = "data/flat1000_76_0.col"

        run_types = int(input("Choose run type (1 for specific, 2 for average, 3 for all): "))

        if run_types == 1:
            population_size = int(input("Enter population size (e.g. 20, 50, 100): "))
            descent_cycles = int(input("Enter descent cycles (e.g. 20, 50, 100): "))
            run_specific_hyperparameter_combinations(graph, colors, population_size, descent_cycles, max_generations)
        elif run_types == 2:
            hyperparameters_string = input("Enter hyperparameter combinations as population_size,descent_cycles; e.g. 20,20;50,50;100,100: ")
            hyperparameters = []
            for combination in hyperparameters_string.split(";"):
                population_size, descent_cycles = map(int, combination.split(","))
                hyperparameters.append((population_size, descent_cycles)) 
            run_some_hyperparameter_combinations_average(graph, colors, hyperparameters, max_generations, runs_amount=5)
        elif run_types == 3:
            population_sizes = [25, 50, 100, 200]
            descent_cycles_list = [25, 50, 100, 200]
            run_all_hyperparameter_combinations(population_sizes, descent_cycles_list, colors, graph, max_generations)

    if choice == "6":
        colors = int(input("Enter number of colors (minimum 26 or 83): "))
        max_generations = 5000
        graph = input("Choose graph: 'small' for flat300, 'large' for flat1000: ")
        if graph == "small":
            graph = "data/flat300_26_0.col"
        elif graph == "large":
            graph = "data/flat1000_76_0.col"

        run_types = int(input("Choose run type (1 for specific, 2 for average, 3 for all): "))

        
        population_size = 50
        descent_cycles = 50

        if run_types == 1:
            tournament_size = int(input("Enter tournament size (e.g. 2, 4, 8, 16): "))
            run_specific_tournament_size(graph, colors, tournament_size, population_size, descent_cycles, max_generations)
        elif run_types == 2:
            tournament_sizes_string = input("Enter tournament sizes as comma separated values (e.g. 2,4,8,16): ")
            tournament_sizes = list(map(int, tournament_sizes_string.split(",")))
            run_some_tournament_sizes_average(graph, colors, population_size, descent_cycles, max_generations, tournament_sizes, runs_amount=5)
        elif run_types == 3:
            tournament_sizes_string = input("Enter tournament sizes as comma separated values (e.g. 2,4,8,16): ")
            tournament_sizes = list(map(int, tournament_sizes_string.split(",")))
            run_all_tournament_sizes(graph, colors, population_size, descent_cycles, max_generations, tournament_sizes)

if __name__ == "__main__":    
    main()