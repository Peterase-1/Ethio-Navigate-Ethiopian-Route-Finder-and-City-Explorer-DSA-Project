import copy
from utils.file_io import save_edges, save_visitors, load_visitors

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
                for u in self.graph.edges:
                    for v, d in self.graph.edges[u]:
                        if (u == city and v == to_city) or (u == to_city and v == city):
                            self.graph.delete_edge(u, v)
                            self.graph.add_edge(city, to_city, distance)
                            edges.append((city, to_city, distance))
                            break
        elif mode == "intermediate" and from_city and distance is not None:
            if any(v == to_city for v, _ in self.graph.get_neighbors(from_city)):
                self.graph.delete_edge(from_city, to_city)
            if not any(v == city for v, _ in self.graph.get_neighbors(from_city)):
                self.graph.add_edge(from_city, city, distance)
                edges.append((from_city, city, distance))
            if not any(v == to_city for v, _ in self.graph.get_neighbors(city)):
                self.graph.add_edge(city, to_city, distance)
                edges.append((city, to_city, distance))

        if edges:
            save_edges(edges)
            self.history.append(("add", copy.deepcopy(self.graph.edges)))

    def delete_edge(self, from_city, to_city):
        if from_city in self.graph.edges:
            self.graph.edges[from_city] = [(n, d) for n, d in self.graph.edges[from_city] if n != to_city]
        if to_city in self.graph.edges:
            self.graph.edges[to_city] = [(n, d) for n, d in self.graph.edges[to_city] if n != from_city]
        save_edges([(u, v, d) for u in self.graph.edges for v, d in self.graph.edges[u]])
        self.history.append(("delete", copy.deepcopy(self.graph.edges)))

    def delete_city(self, city):
        if city in self.graph.edges:
            # Remove all edges connected to the city
            neighbors = self.graph.get_neighbors(city)
            for neighbor, _ in neighbors:
                self.delete_edge(city, neighbor)
            del self.graph.edges[city]
            # Update visitors
            visitors = load_visitors()
            if city in visitors:
                del visitors[city]
                save_visitors(visitors)
            save_edges([(u, v, d) for u in self.graph.edges for v, d in self.graph.edges[u]])
            self.history.append(("delete_city", copy.deepcopy(self.graph.edges)))

    def undo(self):
        if self.history:
            action, prev_state = self.history.pop()
            self.graph.edges = copy.deepcopy(prev_state)
            save_edges([(u, v, d) for u in self.graph.edges for v, d in self.graph.edges[u]])