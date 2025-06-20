from utils.pathfinder import find_all_paths

def normal_navigator(graph, start, end):
    paths = find_all_paths(graph, start, end)
    if not paths:
        return "No path found between the cities."
    return paths