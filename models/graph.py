class Graph:
    def __init__(self, file_path):
        self.file_path = file_path
        self.edges = []
        self.load_graph()


    def load_graph(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                if line.startswith('c'):
                    continue

                elif line.startswith('e'):
                    parts = line.split()
                    v1 = int(parts[1])
                    v2 = int(parts[2].strip('\\'))
                    self.edges.append((v1, v2))

        print(f"Loaded graph with from {self.file_path}")
        