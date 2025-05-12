import os

def load_edges(file_path):
    edges = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                edges.append((parts[0], parts[1], int(parts[2])))
    return edges

def load_heritages(file_path):
    heritage = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, city = line.strip().split(',')
            heritage.setdefault(city, []).append(name)
    return heritage

def save_edge(file_path, from_city, to_city, distance):
    with open(file_path, 'a') as file:
        file.write(f"{from_city},{to_city},{distance}\n")

def load_password(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()