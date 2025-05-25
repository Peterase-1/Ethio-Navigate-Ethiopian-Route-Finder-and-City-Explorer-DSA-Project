def find_all_paths(graph, start, end, path=None, cost=0, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    visited.add(start)

    if start == end:
        return [(cost, path)]

    paths = []
    for neighbor, distance in graph.get_neighbors(start):
        if neighbor not in visited:
            new_path = path + [neighbor]
            new_cost = cost + distance
            paths.extend(find_all_paths(graph, neighbor, end, new_path, new_cost, visited.copy()))
    paths.sort(key=lambda x: x[0])  # Sort by cost
    return paths