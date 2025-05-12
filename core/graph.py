class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_city, to_city, distance):
        self.edges.setdefault(from_city, []).append((to_city, distance))
        self.edges.setdefault(to_city, []).append((from_city, distance))

    def remove_city(self, city):
        if city in self.edges:
            for conn in list(self.edges[city]):
                self.edges[conn[0]] = [(c, d) for c, d in self.edges[conn[0]] if c != city]
            del self.edges[city]

    def get_neighbors(self, city):
        return self.edges.get(city, [])