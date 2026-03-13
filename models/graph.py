from random import random

from models.vertex import Vertex

# dictionary keeps track of color order with key, list does only with its own index, so dictionary is safer to use.
class Graph:

    def __init__(self):
        self.file_path: str = ""
        self.edges: list[tuple[int, int]] = []
        self.vertices: list[Vertex] = []
        self.vertices_grouped_by_color: dict[int, list[int]] = {}
    
    def create_from_file(self, file_path: str):
        self.file_path = file_path
        self.edges = []
        self.vertices: list[Vertex] = []
        self.vertices_grouped_by_color: dict[int, list[int]] = {}
        self.load_graph()

    def create_from_vertices(self, vertices: list[Vertex], vertices_grouped_by_color: dict[int, list[int]]):
        self.file_path = ""
        self.edges = []
        self.vertices: list[Vertex] = vertices
        self.vertices_grouped_by_color: dict[int, list[int]] = vertices_grouped_by_color

        for color, vertex_ids in vertices_grouped_by_color.items():
            for vertex_id in vertex_ids:
                vertex = next(v for v in vertices if v.id == vertex_id)
                vertex.color = color

    def load_graph(self):
        vertex_dict: dict[int, Vertex] = {}
        with open(self.file_path, 'r') as f:
            for line in f:
                if line.startswith('c'):
                    continue
                elif line.startswith('e'):
                    parts = line.split()
                    v1_id = int(parts[1])
                    v2_id = int(parts[2].strip('\\'))

                    if v1_id not in vertex_dict:
                        vertex_dict[v1_id] = Vertex(v1_id)
                    if v2_id not in vertex_dict:
                        vertex_dict[v2_id] = Vertex(v2_id)

                    v1 = vertex_dict[v1_id]
                    v2 = vertex_dict[v2_id]

                    vertex_dict[v1_id].neighbors.add(v2)
                    vertex_dict[v2_id].neighbors.add(v1)

                    self.edges.append((v1_id, v2_id))

        self.vertices = list(vertex_dict.values())
        print(f"Loaded graph from {self.file_path} with {len(self.vertices)} vertices and {len(self.edges)} edges")


    def update_vertices_grouped_by_color(self):
        self.vertices_grouped_by_color = {}
        for vertex in self.vertices:
            if vertex.color not in self.vertices_grouped_by_color:
                self.vertices_grouped_by_color[vertex.color] = []
            self.vertices_grouped_by_color[vertex.color].append(vertex.id)