from models.solution import Solution
from models.vertex import Vertex
import random
import sys


def local_search_vertex_descent(solution: Solution) -> Solution:

    vertices = [v for v in solution.graph.vertices if v.amount_of_conflicts > 0]

    while True:
        color_snapshot: dict[int, int] = {v.id: v.color for v in vertices}

        random.shuffle(vertices)
        old_total_conflicts = 0
        new_total_conflicts = 0

        for vertex in vertices:
            current_conflicts = check_amount_conflicts(vertex, vertex.color)
            best_color, best_conflicts = get_color_with_minimal_conflicts(vertex, solution.colors)

            if best_conflicts < current_conflicts or (
                best_conflicts == current_conflicts and random.random() < 0.5
            ):
                vertex.color = best_color
                vertex.amount_of_conflicts = best_conflicts
            else:
                vertex.amount_of_conflicts = current_conflicts

            old_total_conflicts += current_conflicts
            new_total_conflicts += vertex.amount_of_conflicts

        if new_total_conflicts < old_total_conflicts:
            solution.conflicts_amount = new_total_conflicts
            break
        elif new_total_conflicts == old_total_conflicts and random.random() < 0.5:
            solution.conflicts_amount = new_total_conflicts
            break
        else:
            for v in vertices:
                v.color = color_snapshot[v.id]

    return solution


def get_color_with_minimal_conflicts(vertex: Vertex, num_colors: int) -> tuple[int, int]:
    min_conflicts = sys.maxsize
    best_colors: list[int] = []

    for color in range(num_colors):
        conflict_amount = check_amount_conflicts(vertex, color)
        if conflict_amount < min_conflicts:
            min_conflicts = conflict_amount
            best_colors = [color]
        elif conflict_amount == min_conflicts:
            best_colors.append(color)

    return random.choice(best_colors), min_conflicts


def check_amount_conflicts(vertex: Vertex, color: int) -> int:
    return sum(0.5 for neighbor in vertex.neighbors if neighbor.color == color)