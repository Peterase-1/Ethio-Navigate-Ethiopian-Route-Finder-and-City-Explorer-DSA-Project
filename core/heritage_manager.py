# navigator.py

def find_all_paths(graph, start, end, path=[], visited=None):
    if visited is None:
        visited = set()
    path = path + [start]
    visited.add(start)

    if start == end:
        return [(path, calculate_total_distance(graph, path))]

    if start not in graph:
        return []

    paths = []
    for (node, _) in graph[start]:
        if node not in visited:
            new_paths = find_all_paths(graph, node, end, path, visited.copy())
            paths.extend(new_paths)
    return paths


def calculate_total_distance(graph, path):
    total = 0
    for i in range(len(path) - 1):
        neighbors = graph[path[i]]
        for neighbor, dist in neighbors:
            if neighbor == path[i + 1]:
                total += dist
                break
    return total


def display_sorted_paths(paths):
    if not paths:
        print("\n🚫 No route found between the selected cities.")
        return

    sorted_paths = sorted(paths, key=lambda x: x[1])
    print("\n🛣️ All Possible Routes (sorted by distance):")
    for i, (path, dist) in enumerate(sorted_paths, 1):
        print(f"  {i}. {' -> '.join(path)} | Total Distance: {dist} km")
