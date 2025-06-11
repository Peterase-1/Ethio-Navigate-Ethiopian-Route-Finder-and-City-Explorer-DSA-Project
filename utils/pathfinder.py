from EthioNavigator.core.graph import Graph  # Absolute import
import heapq

def find_shortest_paths(graph, start, end):
    if start not in graph.edges or end not in graph.edges:
        return "City not registered."
    distances = {start: 0}
    previous = {start: None}
    pq = [(0, start)]
    paths = []
    while pq:
        current_distance, current_city = heapq.heappop(pq)
        if current_city == end:
            path = []
            while current_city is not None:
                path.append(current_city)
                current_city = previous[current_city]
            paths.append((current_distance, path[::-1]))
            continue
        for neighbor, distance in graph.get_neighbors(current_city):
            distance_to_neighbor = current_distance + distance
            if neighbor not in distances or distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                previous[neighbor] = current_city
                heapq.heappush(pq, (distance_to_neighbor, neighbor))
    return sorted(paths, key=lambda x: x[0])[:3] if paths else "No route found."