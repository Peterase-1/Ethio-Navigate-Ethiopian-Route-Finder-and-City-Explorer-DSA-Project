import heapq

def find_all_paths(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    paths = []

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            paths.append((cost, path))
        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return sorted(paths, key=lambda x: x[0])