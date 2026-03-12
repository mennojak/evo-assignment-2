from models.solution import Solution
from models.graph import Vertex
import random
import sys
from utils import create_copy_of_vertices

def local_search_vertex_descent(solution: Solution) -> Solution:
    improved = True

    while improved:
        improved = False
        vertices_list_copy = create_copy_of_vertices(solution.graph.vertices) # Is het nodig om een kopie te maken van de vertices? We kunnen toch gewoon de kleuren aanpassen en daarna weer terug zetten als het niet beter is?
        random.shuffle(vertices_list_copy)
        total_conflicts = 0

        for vertex in vertices_list_copy:
            if(vertex.color == -1):
                vertex.color = random.randint(1, solution.colors)
                continue

            current_color_conflict_amount = check_amount_conflicts(vertex, vertex.color)

            best_color, best_color_conflict_amount = get_color_with_minimal_conflicts(vertex, solution.colors)

            if best_color_conflict_amount < current_color_conflict_amount:
                vertex.color = best_color
                vertex.amount_of_conflicts = best_color_conflict_amount
            elif best_color_conflict_amount == current_color_conflict_amount and random.random() < 0.5:
                vertex.color = best_color
                vertex.amount_of_conflicts = best_color_conflict_amount

            total_conflicts += vertex.amount_of_conflicts

        # Volgensmij kan het simpeler naar een =< check, want we willen ook bij gelijke de nieuwe oplossing kiezen, dacht dat het zo in de opdracht stond.
        if total_conflicts < solution.conflicts_amount:
            solution.conflicts_amount = total_conflicts
            solution.graph.vertices = vertices_list_copy
            improved = True
        elif total_conflicts == solution.conflicts_amount and random.random() < 0.5:
            solution.conflicts_amount = total_conflicts
            solution.graph.vertices = vertices_list_copy
            improved = True

    return solution


def get_color_with_minimal_conflicts(vertex: Vertex, num_colors: int) -> tuple[int, int]:
    min_conflicts: int = sys.maxsize # Moet dit niet een initiele waarde hebben?
    best_colors = []

    for color in range(1, num_colors + 1):
        conflict_amount = check_amount_conflicts(vertex, color)
        if conflict_amount < min_conflicts:
            min_conflicts = conflict_amount
            best_colors = [color]
        elif conflict_amount == min_conflicts:
            best_colors.append(color)

    chosen_color = random.choice(best_colors)

    return chosen_color, min_conflicts


def check_amount_conflicts(vertex: Vertex, color: int) -> int:
    conflict_amount = 0
    for neighbor in vertex.neighbors:
        if color != -1 and neighbor.color == color:
            conflict_amount += 1
    return conflict_amount