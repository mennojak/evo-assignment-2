from models.solution import Solution
from models.vertex import Vertex
import random
import sys


def local_search_vertex_descent(solution: Solution) -> Solution:
    
    vertices = solution.graph.vertices

    random.shuffle(vertices)

    for vertex in vertices:

        if vertex.color == -1:
            vertex.color = random.randint(0, solution.colors - 1)
            continue

        if vertex.amount_of_conflicts == 0:
            continue

        current_conflicts = vertex.amount_of_conflicts

        best_color, best_conflicts = get_color_with_minimal_conflicts(vertex, solution.colors)

        if best_conflicts < current_conflicts or (best_conflicts == current_conflicts and random.random() < 0.5):
            vertex.color = best_color
            vertex.amount_of_conflicts = best_conflicts
        else:
            pass

    solution.update_conflicts_amount()
    solution.graph.update_vertices_grouped_by_color()
    return solution


def get_color_with_minimal_conflicts(vertex: Vertex, num_colors: int) -> tuple[int, int]:
    neighbor_color_counts = [0 for _ in range(num_colors)]
    
    for neighbor in vertex.neighbors:
        if neighbor.color != -1:
            neighbor_color_counts[neighbor.color] += 1

    min_conflicts = min(neighbor_color_counts)

    best_colors = [color for color in range(num_colors) if neighbor_color_counts[color] == min_conflicts]

    chosen_color = random.choice(best_colors)

    return chosen_color, min_conflicts
