import random

from models.graph import Graph
import sys

class Solution:
    def __init__(self, graph: Graph, colors: int, create_random: bool = False):
        self.graph: Graph = graph
        self.colors: int = colors
        self.conflicts_amount: int = sys.maxsize
        if create_random:
            self.create_random_solution()


    def create_random_solution(self):
        for vertex in self.graph.vertices:
            vertex.color = random.randint(0, self.colors - 1)

        self.update_conflicts_amount()
        self.graph.update_vertices_grouped_by_color()


    def calculate_penalty(self)  -> int:
        total = 0
        for vertex in self.graph.vertices:
            total += vertex.amount_of_conflicts
        self.conflicts_amount = total
        return self.conflicts_amount
    

    def update_conflicts_amount(self) -> None:
        total = 0
        for vertex in self.graph.vertices:
            vertex.amount_of_conflicts = 0
        for vertex in self.graph.vertices:
            for neighbor in vertex.neighbors:
                if vertex.id < neighbor.id and vertex.color != -1 and vertex.color == neighbor.color:
                    vertex.amount_of_conflicts += 1
                    neighbor.amount_of_conflicts += 1
                    total += 1
        self.conflicts_amount = total