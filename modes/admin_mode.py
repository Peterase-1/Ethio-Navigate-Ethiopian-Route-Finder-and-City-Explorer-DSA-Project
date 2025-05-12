from utils.file_io import save_edge

class Admin:
    def __init__(self, graph, password):
        self.graph = graph
        self.password = password

    def add_city(self, from_city, to_city, distance):
        self.graph.add_edge(from_city, to_city, distance)
        save_edge('data/cities.txt', from_city, to_city, distance)

    def delete_city(self, city):
        self.graph.remove_city(city)