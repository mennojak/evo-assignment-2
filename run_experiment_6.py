import time
import pandas as pd
from evaluation import EvaluationResult
from gls_algorithm import genetic_local_search
import matplotlib.pyplot as plt
from collections import defaultdict
import random
from evaluation import EvaluationResult, GenerationResult

def run_specific_tournament_size(graph: str, colors: int, tournament_size: int, population_size: int, descent_cycles: int, max_generations: int):
    start_time = time.time()
    best_solution, generation_results = genetic_local_search(
        graph, 
        colors, 
        population_size, 
        descent_cycles, 
        max_generations, 
        tournament_selection_on=True, 
        tournament_size=tournament_size
    )
    print("Best solution conflicts:", best_solution.conflicts_amount)
    print("Average solution conflicts:", generation_results[-1].average_penalty)
    print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
    print(f"Amount of generations: {len(generation_results)}")
    evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
    evaluation.plot()

def run_all_tournament_sizes(graph: str, colors: int, population_size: int, descent_cycles: int, max_generations: int, tournament_sizes: list[int]):
    evaluations = []

    for size in tournament_sizes:
        print(f"Running with tournament size: {size}")

        start_time = time.time()
        best_solution, generation_results = genetic_local_search(
            graph, 
            colors, 
            population_size, 
            descent_cycles, 
            max_generations, 
            tournament_selection_on=True, 
            tournament_size=size
        )

        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 6, colors, population_size, descent_cycles)
        evaluations.append(evaluation)

    rows = []

    for evaluation in evaluations:
        last_gen = evaluation.generation_results[-1]

        rows.append({
            "tournament_size": tournament_sizes[evaluations.index(evaluation)],
            "population_size": evaluation.population_size,
            "descent_cycles": evaluation.descent_cycles,
            "generations": len(evaluation.generation_results),
            "final_best_solution": last_gen.best_penalty,
            "final_average_solution": last_gen.average_penalty,
            "runtime_seconds": evaluation.time
        })

    df = pd.DataFrame(rows)
    df = df.set_index(["population_size", "descent_cycles"])

    df.to_csv("results/" + str(colors) + "_experiment_6_results.csv", sep=';')

def run_some_tournament_sizes_average(graph: str, colors: int, population_size: int, descent_cycles: int, max_generations: int, tournament_sizes: list[int], runs_amount: int):

    grouped = defaultdict(list)

    # Run all experiments
    for run_num in range(runs_amount):
        print(f"Run {run_num + 1} out of {runs_amount} for all tournament sizes...")
        for tournament_size in tournament_sizes:
            start_time = time.time()
            best_solution, generation_results = genetic_local_search(
                graph, colors, population_size, descent_cycles, max_generations, tournament_selection_on=True, tournament_size=tournament_size
            )
            duration = time.time() - start_time

            evaluation = EvaluationResult(
                generation_results, 6, colors,
                population_size, descent_cycles, duration
            )

            grouped[tournament_size].append(evaluation)

    evaluations_average = []

    # Compute average penalty per generation for each hyperparameter combination
    for tournament_size, evaluations in grouped.items():
        average_generation_results = []

        max_generations_count = max(len(evaluation.generation_results) for evaluation in evaluations)

        for i in range(max_generations_count):
            penalties = [
                evaluation.generation_results[i].average_penalty
                for evaluation in evaluations if i < len(evaluation.generation_results)
            ]
            avg_penalty = sum(penalties) / len(penalties) if penalties else 0
            average_generation_results.append(
                GenerationResult(i, best_penalty=0, average_penalty=avg_penalty)
            )

        evaluations_average.append(
            EvaluationResult(
                average_generation_results, 6, colors,
                population_size, descent_cycles
            )
        )

    plt.figure()
    color_palette = ['blue', 'green', 'red', 'purple', 'orange']

    for idx, (tournament_size, evaluation) in enumerate(zip(grouped.keys(), evaluations_average)):
        generations = [r.generation_number for r in evaluation.generation_results]
        avg_penalties = [r.average_penalty for r in evaluation.generation_results]
        color = color_palette[idx % len(color_palette)]

        plt.plot(
            generations,
            avg_penalties,
            linestyle='-',
            color=color,
            label=f'Exp {evaluation.experiment} (colors={evaluation.colors}, N={evaluation.population_size}, L={evaluation.descent_cycles}, T={tournament_size})'
        )

        for run in grouped[tournament_size]:
            last_gen = run.generation_results[-1]
            plt.scatter(
                last_gen.generation_number,
                last_gen.average_penalty,
                color=color,
                marker='o',
                s=40,
                alpha=0.7
            )

    plt.xlabel('Generation')
    plt.ylabel('Average penalty')
    plt.title('Experiment 6 - Colors: ' + str(colors) + ' - Tournament sizes comparison (average score over multiple runs)')
    plt.legend()
    plt.savefig("results/" + str(colors) + "_best_three_tournament_sizes_comparison_average_with_dots.png")
    plt.show()