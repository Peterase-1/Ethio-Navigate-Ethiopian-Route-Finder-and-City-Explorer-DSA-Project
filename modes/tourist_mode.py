from utils.pathfinder import find_all_paths

def tourist_navigator(graph, start, end, heritages):
    if start not in graph.edges or end not in graph.edges:
        return "City not registered."
    paths = find_all_paths(graph, start, end)
    if not paths:
        return "No route found."

    result = []
    for cost, path in paths[:3]:
        included_heritages = [heritage for city in path for heritage in heritages.get(city, [])]
        result.append((cost, path, included_heritages))
    return result