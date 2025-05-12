from core.graph import Graph
from utils.file_io import load_edges, load_heritages, load_password
from modes.normal_mode import normal_navigator
from modes.tourist_mode import tourist_navigator
from modes.admin_mode import Admin

def initialize_graph():
    graph = Graph()
    for from_city, to_city, distance in load_edges("data/cities.txt"):
        graph.add_edge(from_city, to_city, distance)
    return graph

def main():
    graph = initialize_graph()
    heritages = load_heritages("data/heritages.txt")
    password = load_password("data/admin_password.txt")
    admin = Admin(graph, password)

    while True:
        mode = input("Select mode (normal/tourist/admin/exit): ").strip().lower()

        if mode == "exit":
            break

        elif mode == "normal":
            start = input("Start city: ")
            end = input("Destination: ")
            routes = normal_navigator(graph, start, end)
            print(routes)

        elif mode == "tourist":
            start = input("Start city: ")
            end = input("Destination: ")
            routes = tourist_navigator(graph, start, end, heritages)
            for cost, path, sites in routes:
                print(f"{path} | Cost: {cost}km | Sites: {sites}")

        elif mode == "admin":
            attempt = input("Enter admin password: ")
            if attempt != password:
                print("Access Denied")
                continue
            act = input("Add or delete city? ").lower()
            if act == "add":
                from_city = input("From: ")
                to_city = input("To: ")
                dist = int(input("Distance: "))
                admin.add_city(from_city, to_city, dist)
            elif act == "delete":
                city = input("City to remove: ")
                admin.delete_city(city)

if __name__ == '__main__':
    main()