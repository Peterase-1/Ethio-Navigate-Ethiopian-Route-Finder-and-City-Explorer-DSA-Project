from utils.pathfinder import find_all_paths

def normal_navigator(graph, start, end):
    if start not in graph.edges or end not in graph.edges:
        return "City not registered."
    paths = find_all_paths(graph, start, end)
    if not paths:
        return "No route found."
    return paths