from models.solution import Solution
from models.vertex import Vertex
import random


def local_search_vertex_descent(solution: Solution) -> Solution:
    vertices = [v for v in solution.graph.vertices if v.amount_of_conflicts > 0]

    random.shuffle(vertices)

    total_conflicts = 0

    for vertex in vertices:
        current_conflicts = count_conflicts(vertex, vertex.color)
        best_color, best_conflicts = get_best_color(vertex, solution.colors)

        if best_conflicts < current_conflicts or (
            best_conflicts == current_conflicts and random.random() < 0.5
        ):
            vertex.color = best_color
            vertex.amount_of_conflicts = best_conflicts
        else:
            vertex.amount_of_conflicts = current_conflicts

        total_conflicts += vertex.amount_of_conflicts

    solution.conflicts_amount = total_conflicts

    return solution


def get_best_color(vertex: Vertex, num_colors: int) -> tuple[int, int]:
    color_conflicts = [0] * num_colors

    for neighbor in vertex.neighbors:
        if neighbor.color != -1:
            color_conflicts[neighbor.color] += 1

    min_conflicts = min(color_conflicts)

    best_colors = [
        color for color, conflicts in enumerate(color_conflicts)
        if conflicts == min_conflicts
    ]

    return random.choice(best_colors), min_conflicts


def count_conflicts(vertex: Vertex, color: int) -> int:
    return sum(1 for neighbor in vertex.neighbors if neighbor.color == color)