from collections import defaultdict
import time
import pandas as pd
from evaluation import EvaluationResult, GenerationResult
from gls_algorithm import genetic_local_search
from matplotlib import pyplot as plt

def run_all_hyperparameter_combinations(population_sizes: list[int], descent_cycles_list: list[int], colors: int, graph: str, max_generations: int):
    evaluation_results = []

    for population_size in population_sizes:
        for descent_cycles in descent_cycles_list:
            start_time = time.time()
            best_solution, generation_results = genetic_local_search(graph, colors, population_size, descent_cycles, max_generations)
            print("Best solution conflicts:", best_solution.conflicts_amount)
            print("Average solution conflicts:", generation_results[-1].average_penalty)
            print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
            print(f"Amount of generations: {len(generation_results)}")
            end_time = time.time()
            duration = end_time - start_time
            evaluation = EvaluationResult(generation_results, 3, colors, population_size, descent_cycles, duration)
            evaluation_results.append(evaluation)

    rows = []

    for evaluation in evaluation_results:
        last_gen = evaluation.generation_results[-1]

        rows.append({
            "population_size": evaluation.population_size,
            "descent_cycles": evaluation.descent_cycles,
            "generations": len(evaluation.generation_results),
            "final_best_solution": last_gen.best_penalty,
            "final_average_solution": last_gen.average_penalty,
            "runtime_seconds": evaluation.time
        })

    df = pd.DataFrame(rows)
    df = df.set_index(["population_size", "descent_cycles"])

    df.to_csv("results/" + str(colors) + "_experiment_3_results.csv", sep=',')

    best_three_evaluations = sorted(
        evaluation_results,
        key=lambda e: e.generation_results[-1].generation_number
    )[:3]

    plt.figure()

    styles = [
        ('--', 'blue'),
        ('-', 'green'),
        (':', 'red')
    ]

    for evaluation, (linestyle, color) in zip(best_three_evaluations, styles):
        generations = [r.generation_number for r in evaluation.generation_results]
        best_penalties = [r.best_penalty for r in evaluation.generation_results]

        plt.plot(
            generations,
            best_penalties,
            linestyle=linestyle,
            color=color,
            label=f'Exp {evaluation.experiment} (colors={evaluation.colors}, n={evaluation.population_size}, L={evaluation.descent_cycles})'
        )

    plt.xlabel('Generation')
    plt.ylabel('Penalty')
    plt.title('Experiment 3 - Colors: ' + str(colors) + ' - Best three hyperparameter combinations (population size and descent cycles)')
    plt.legend()

    plt.savefig("results/" + str(colors) + "_best_three_comparison.png")
    plt.show()
 
def run_specific_hyperparameter_combinations(graph: str, colors: int, population_size: int, descent_cycles: int, max_generations: int):
        start_time = time.time()
        best_solution, generation_results = genetic_local_search(graph, colors, population_size, descent_cycles, max_generations)
        print("Best solution conflicts:", best_solution.conflicts_amount)
        print("Average solution conflicts:", generation_results[-1].average_penalty)
        print(f"Evaluation time: {time.time() - start_time:.2f} seconds")
        print(f"Amount of generations: {len(generation_results)}")
        evaluation = EvaluationResult(generation_results, 1, colors, population_size, descent_cycles)
        evaluation.plot()

# hyperparameters = [
#     (population_size, descent_cycles),
#     etc...
# ]
def run_some_hyperparameter_combinations_average(graph: str, colors: int, hyperparameters: list[tuple[int, int]], max_generations: int, runs_amount: int):

    grouped = defaultdict(list)

    # Run all experiments
    for run_num in range(runs_amount):
        print(f"Run {run_num + 1} out of {runs_amount} for all hyperparameter combinations...")
        for population_size, descent_cycles in hyperparameters:
            start_time = time.time()
            best_solution, generation_results = genetic_local_search(
                graph, colors, population_size, descent_cycles, max_generations
            )
            duration = time.time() - start_time

            evaluation = EvaluationResult(
                generation_results, 3, colors,
                population_size, descent_cycles, duration
            )

            key = (population_size, descent_cycles)
            grouped[key].append(evaluation)

    evaluations_average = []

    # Compute average penalty per generation for each hyperparameter combination
    for (population_size, descent_cycles), evaluations in grouped.items():
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
                average_generation_results, 3, colors,
                population_size, descent_cycles
            )
        )

    plt.figure()
    color_palette = ['blue', 'green', 'red', 'purple', 'orange']

    for idx, ((population_size, descent_cycles), evaluation) in enumerate(zip(grouped.keys(), evaluations_average)):
        generations = [r.generation_number for r in evaluation.generation_results]
        avg_penalties = [r.average_penalty for r in evaluation.generation_results]
        color = color_palette[idx % len(color_palette)]

        plt.plot(
            generations,
            avg_penalties,
            linestyle='-',
            color=color,
            label=f'Exp {evaluation.experiment} (colors={evaluation.colors}, n={evaluation.population_size}, L={evaluation.descent_cycles})'
        )

        for run in grouped[(population_size, descent_cycles)]:
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
    plt.title('Experiment 3 - Colors: ' + str(colors) + ' - Best three hyperparameter combinations (population size and descent cycles) average score (over multiple runs)')
    plt.legend()
    plt.savefig("results/" + str(colors) + "_best_three_comparison_average_with_dots.png")
    plt.show()