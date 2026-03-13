import matplotlib.pyplot as plt

class GenerationResult:
    def __init__(self, generation_number : int, best_penalty: float, average_penalty: float):
        self.generation_number = generation_number
        self.best_penalty = best_penalty
        self.average_penalty = average_penalty

class EvaluationResult:
    def __init__(self, generation_results: list[GenerationResult]):
        self.generation_results = generation_results

    def plot(self):
        generations = [result.generation_number for result in self.generation_results]
        best_penalties = [result.best_penalty for result in self.generation_results]
        average_penalties = [result.average_penalty for result in self.generation_results]

        plt.plot(generations, best_penalties, label='Best Penalty')
        plt.plot(generations, average_penalties, label='Average Penalty')
        plt.xlabel('Generation')
        plt.ylabel('Penalty')
        plt.title('Genetic Algorithm Performance')
        plt.legend()
        plt.show()
