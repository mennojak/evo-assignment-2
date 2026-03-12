

from models.graph import Graph
from models.vertex import Vertex

def copy_graph_vertices_grouped_by_color(graph: Graph) -> dict[int, list[int]]:
    
    vertices_grouped_by_color: dict[int, list[int]] = {}
    for color, vertex_ids in graph.vertices_grouped_by_color.items():
        for vertex_id in vertex_ids:
            if color not in vertices_grouped_by_color:
                vertices_grouped_by_color[color] = []
            vertices_grouped_by_color[color].append(vertex_id)

    return vertices_grouped_by_color

def create_copy_of_vertices(vertices: list[Vertex]) -> list[Vertex]:
    vertices_copy_dict = {v.id: Vertex(v.id, v.color) for v in vertices}

    for vertice in vertices:
        copy_vertice = vertices_copy_dict[vertice.id]
        for vertex_neighbor in vertice.neighbors:
            copy_neighbor = vertices_copy_dict[vertex_neighbor.id]
            copy_vertice.neighbors.add(copy_neighbor)

    return list(vertices_copy_dict.values())