import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)  # {city: [(neighbor, distance), ...]}

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
        distances = {start: 0}
        pq = [(0, start)]
        visited = set()
        while pq:
            current_distance, current_city = heapq.heappop(pq)
            if current_city in visited:
                continue
            visited.add(current_city)
            if current_city == end:
                return current_distance
            for neighbor, distance in self.edges[current_city]:
                if neighbor not in visited:
                    distance_to_neighbor = current_distance + distance
                    if neighbor not in distances or distance_to_neighbor < distances[neighbor]:
                        distances[neighbor] = distance_to_neighbor
                        heapq.heappush(pq, (distance_to_neighbor, neighbor))
        return None