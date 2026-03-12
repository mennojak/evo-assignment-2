from models.graph import Graph
import sys

class Solution:
    def __init__(self, graph: Graph, colors: int):
        # TODO
        self.graph: Graph = graph
        self.colors: int = colors
        self.conflicts_amount: int = sys.maxsize
        self.create_random_solution()

    def create_random_solution(self):
        pass

    def calculate_penalty(self)  -> int:
        total = 0
        for vertex in self.graph.vertices:
            total += vertex.amount_of_conflicts
        return total