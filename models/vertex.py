import sys

class Vertex:
    def __init__(self, id: int, color: int = -1):
        self.id: int = id
        self.color = color
        self.neighbors: set[Vertex] = set()
        self.amount_of_conflicts: int = sys.maxsize
    