import copy
from utils.file_io import save_edges

class Admin:
    def __init__(self, graph):
        self.graph = graph
        self.history = []  # For undo functionality

    def add_city(self, mode, city, to_city, from_city=None, distance=None):
        edges = []
        if mode == "new":
            if (city, to_city) not in self.graph.edges and (to_city, city) not in self.graph.edges:
                self.graph.add_edge(city, to_city, distance)
                edges.append((city, to_city, distance))
            else:
                # Update existing edge if it exists
                for (f, t), d in list(self.graph.edges.items()):
                    if (f == city and t == to_city) or (f == to_city and t == city):
                        self.graph.edges[(f, t)] = distance
                        edges.append((f, t, distance))
                        break
        elif mode == "intermediate" and from_city and distance is not None:
            if (from_city, to_city) in self.graph.edges or (to_city, from_city) in self.graph.edges:
                # Remove direct edge
                self.delete_edge(from_city, to_city)
            if (from_city, city) not in self.graph.edges and (city, from_city) not in self.graph.edges:
                self.graph.add_edge(from_city, city, distance)
                edges.append((from_city, city, distance))
            if (city, to_city) not in self.graph.edges and (to_city, city) not in self.graph.edges:
                self.graph.add_edge(city, to_city, distance)  # Placeholder for remaining distance logic
                edges.append((city, to_city, distance))

        if edges:
            save_edges(edges)
            self.history.append(("add", copy.deepcopy(self.graph.edges)))

    def delete_edge(self, from_city, to_city):
        if (from_city, to_city) in self.graph.edges:
            del self.graph.edges[(from_city, to_city)]
            save_edges(self.graph.edges_data())
            self.history.append(("delete", copy.deepcopy(self.graph.edges)))
        elif (to_city, from_city) in self.graph.edges:
            del self.graph.edges[(to_city, from_city)]
            save_edges(self.graph.edges_data())
            self.history.append(("delete", copy.deepcopy(self.graph.edges)))

    def delete_city(self, city):
        if city in self.graph.edges:
            neighbors = list(self.graph.get_neighbors(city))
            for neighbor, _ in neighbors:
                self.delete_edge(city, neighbor)
            save_edges(self.graph.edges_data())
            self.history.append(("delete_city", copy.deepcopy(self.graph.edges)))

    def undo(self):
        if self.history:
            action, prev_state = self.history.pop()
            self.graph.edges = copy.deepcopy(prev_state)
            save_edges(self.graph.edges_data())