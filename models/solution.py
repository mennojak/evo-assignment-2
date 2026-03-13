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
    
    def update_conflicts_amount(self):
        self.conflicts_amount = 0
        for vertex in self.graph.vertices:
            vertex.amount_of_conflicts = 0
            for neighbor in vertex.neighbors:
                if vertex.color != -1 and neighbor.color == vertex.color:
                    vertex.amount_of_conflicts += 1
            self.conflicts_amount += vertex.amount_of_conflicts
        self.conflicts_amount = self.conflicts_amount