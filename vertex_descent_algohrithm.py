from models.solution import Solution
from models.vertex import Vertex
import random

def local_search_vertex_descent(solution: Solution, descent_cycles: int = 100) -> Solution:
    vertices = solution.graph.vertices
    num_colors = solution.colors

    # Assign random colors only if needed
    for v in vertices:
        if v.color == -1:
            v.color = random.randrange(num_colors)

    color_costs_matrix = initialize_color_costs_matrix(vertices, num_colors)

    for cycle in range(descent_cycles):
        improvement_made = False

        for vertex in vertices:
            current_color = vertex.color
            current_cost = color_costs_matrix[vertex.id][current_color]

            best_color, best_cost = find_best_color(color_costs_matrix[vertex.id])

            if should_recolor(current_cost, best_cost):
                recolor_vertex(vertex, best_color, color_costs_matrix)

                if best_cost < current_cost:
                    improvement_made = True  # mark that we improved

        # Early stop if no improvement in this cycle
        if not improvement_made:
            break

    # Update global conflicts at the end
    solution.conflicts_amount = count_total_conflicts(vertices)
    return solution


def initialize_color_costs_matrix(vertices: list[Vertex], num_colors: int) -> dict[int, list[int]]:
    color_costs_matrix = {v.id: [0] * num_colors for v in vertices}

    for v in vertices:
        for neighbor in v.neighbors:
            if neighbor.color != -1:
                color_costs_matrix[v.id][neighbor.color] += 1

    return color_costs_matrix


def find_best_color(cost_row: list[int]) -> tuple[int, int]:
    min_cost = min(cost_row)

    best_colors = [
        color for color, cost in enumerate(cost_row)
        if cost == min_cost
    ]

    return random.choice(best_colors), min_cost


def should_recolor(current_cost: int, best_cost: int) -> bool:
    if best_cost < current_cost:
        return True

    if best_cost == current_cost:
        return random.random() < 0.1  # small randomness

    return False


def recolor_vertex(vertex: Vertex, new_color: int, color_costs: dict[int, list[int]]) -> None:
    old_color = vertex.color

    if old_color == new_color:
        return

    vertex.color = new_color

    for neighbor in vertex.neighbors:
        neighbor_costs = color_costs[neighbor.id]

        # Neighbor no longer conflicts with old color
        neighbor_costs[old_color] -= 1

        # Neighbor now conflicts with new color
        neighbor_costs[new_color] += 1


def count_total_conflicts(vertices: list[Vertex]) -> int:
    total = 0

    for v in vertices:
        for neighbor in v.neighbors:
            if v.color == neighbor.color:
                total += 1

    return total // 2  # each edge counted twice