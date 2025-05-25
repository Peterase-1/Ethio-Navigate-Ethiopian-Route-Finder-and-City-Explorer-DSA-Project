class Graph:
    def __init__(self):
        self.edges = {}  # Dictionary: {city: [(neighbor, distance), ...]}

    def add_edge(self, from_city, to_city, distance):
        if from_city not in self.edges:
            self.edges[from_city] = []
        if to_city not in self.edges:
            self.edges[to_city] = []
        self.edges[from_city].append((to_city, distance))
        self.edges[to_city].append((from_city, distance))

    def get_neighbors(self, city):
        return self.edges.get(city, [])

    def delete_edge(self, from_city, to_city):
        if from_city in self.edges:
            self.edges[from_city] = [(n, d) for n, d in self.edges[from_city] if n != to_city]
        if to_city in self.edges:
            self.edges[to_city] = [(n, d) for n, d in self.edges[to_city] if n != from_city]

    def get_shortest_distance(self, start, end):
        if start not in self.edges or end not in self.edges:
            return None
        from collections import deque
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            city, dist = queue.popleft()
            if city == end:
                return dist
            for neighbor, distance in self.edges.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + distance))
        return None