import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Add project root to path

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.file_io import save_edges, save_heritage, load_heritages, load_edges, load_visitors, reset_visitors

def show_login_dialog(root, password, success_callback):
    top = tk.Toplevel(root)
    top.title("Admin Login")
    top.geometry("300x150")
    top.configure(bg="#f5f5f5")

    ttk.Label(top, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
    pass_entry = ttk.Entry(top, show="*", font=("Arial", 10))
    pass_entry.pack(pady=5)

    def check():
        if pass_entry.get() == password:
            top.destroy()
            success_callback()
        else:
            messagebox.showerror("Access Denied", "Incorrect password")

    try:
        login_icon = Image.open(Path(__file__).resolve().parent.parent / "assets" / "login_icon.png")
        login_icon = login_icon.resize((30, 30), Image.Resampling.LANCZOS)
        login_photo = ImageTk.PhotoImage(login_icon)
        login_btn = tk.Button(top, image=login_photo, command=check,
                            bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
        login_btn.pack(pady=10)
    except FileNotFoundError:
        login_btn = tk.Button(top, text="Login", command=check,
                            font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
        login_btn.pack(pady=10)

class AdminPanel(tk.Frame):
    def __init__(self, master, app, go_frame):
        super().__init__(master, bg="#f5f5f5")
        self.app = app
        self.go_frame = go_frame
        root_path = Path(__file__).resolve().parent.parent

        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns_frame = tk.Frame(main_frame, bg="#f5f5f5")
        columns_frame.pack(fill="both", expand=True)

        first_column = tk.Frame(columns_frame, bg="#f5f5f5", width=300)
        first_column.pack(side="left", fill="y", padx=5)

        ttk.Label(first_column, text="Add New City", font=("Arial", 12)).pack(pady=5)
        new_city_frame = tk.Frame(first_column, bg="#f5f5f5")
        new_city_frame.pack(pady=5)
        ttk.Label(new_city_frame, text="City:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        new_city_entry = ttk.Entry(new_city_frame, width=15, font=("Arial", 10))
        new_city_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(new_city_frame, text="To City:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        new_to_entry = ttk.Entry(new_city_frame, width=15, font=("Arial", 10))
        new_to_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(new_city_frame, text="Distance (km):", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=2, sticky="w")
        new_dist_entry = ttk.Entry(new_city_frame, width=15, font=("Arial", 10))
        new_dist_entry.grid(row=2, column=1, padx=5, pady=2)
        try:
            add_icon = Image.open(root_path / "assets" / "add_icon.png")
            add_icon = add_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.add_photo = ImageTk.PhotoImage(add_icon)
            add_new_btn = tk.Button(new_city_frame, image=self.add_photo, command=lambda: self.add_new_city(new_city_entry, new_to_entry, new_dist_entry),
                                  bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            add_new_btn.grid(row=3, column=0, columnspan=2, pady=5)
        except FileNotFoundError:
            add_new_btn = tk.Button(new_city_frame, text="Add", command=lambda: self.add_new_city(new_city_entry, new_to_entry, new_dist_entry),
                                  font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            add_new_btn.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(first_column, text="Add Intermediate City", font=("Arial", 12)).pack(pady=5)
        inter_city_frame = tk.Frame(first_column, bg="#f5f5f5")
        inter_city_frame.pack(pady=5)
        ttk.Label(inter_city_frame, text="City:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        inter_city_entry = ttk.Entry(inter_city_frame, width=15, font=("Arial", 10))
        inter_city_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(inter_city_frame, text="From City:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        inter_from_entry = ttk.Entry(inter_city_frame, width=15, font=("Arial", 10))
        inter_from_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(inter_city_frame, text="To City:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=2, sticky="w")
        inter_to_entry = ttk.Entry(inter_city_frame, width=15, font=("Arial", 10))
        inter_to_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Label(inter_city_frame, text="Distance from From City (km):", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=2, sticky="w")
        dist_from_entry = ttk.Entry(inter_city_frame, width=15, font=("Arial", 10))
        dist_from_entry.grid(row=3, column=1, padx=5, pady=2)
        ttk.Label(inter_city_frame, text="Distance to To City (km):", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=2, sticky="w")
        dist_to_entry = ttk.Entry(inter_city_frame, width=15, font=("Arial", 10))
        dist_to_entry.grid(row=4, column=1, padx=5, pady=2)
        try:
            add_inter_icon = Image.open(root_path / "assets" / "add_icon.png")
            add_inter_icon = add_inter_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.add_inter_photo = ImageTk.PhotoImage(add_inter_icon)
            add_inter_btn = tk.Button(inter_city_frame, image=self.add_inter_photo, command=lambda: self.add_intermediate_city(inter_city_entry, inter_from_entry, inter_to_entry, dist_from_entry, dist_to_entry),
                                    bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            add_inter_btn.grid(row=5, column=0, columnspan=2, pady=5)
        except FileNotFoundError:
            add_inter_btn = tk.Button(inter_city_frame, text="Add", command=lambda: self.add_intermediate_city(inter_city_entry, inter_from_entry, inter_to_entry, dist_from_entry, dist_to_entry),
                                    font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            add_inter_btn.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Label(first_column, text="Add Heritage", font=("Arial", 10)).pack(pady=5)
        heritage_frame = tk.Frame(first_column, bg="#f5f5f5")
        heritage_frame.pack(pady=5)
        ttk.Label(heritage_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        heritage_name_entry = ttk.Entry(heritage_frame, width=15, font=("Arial", 10))
        heritage_name_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(heritage_frame, text="City:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        heritage_city_entry = ttk.Entry(heritage_frame, width=15, font=("Arial", 10))
        heritage_city_entry.grid(row=1, column=1, padx=5, pady=2)
        try:
            heritage_add_icon = Image.open(root_path / "assets" / "add_icon.png")
            heritage_add_icon = heritage_add_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.heritage_add_photo = ImageTk.PhotoImage(heritage_add_icon)
            heritage_add_btn = tk.Button(heritage_frame, image=self.heritage_add_photo, command=lambda: self.add_heritage(heritage_name_entry, heritage_city_entry),
                                       bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            heritage_add_btn.grid(row=2, column=0, columnspan=2, pady=5)
        except FileNotFoundError:
            heritage_add_btn = tk.Button(heritage_frame, text="Add", command=lambda: self.add_heritage(heritage_name_entry, heritage_city_entry),
                                       font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            heritage_add_btn.grid(row=2, column=0, columnspan=2, pady=5)

        second_column = tk.Frame(columns_frame, bg="#f5f5f5", width=300)
        second_column.pack(side="left", fill="y", padx=5)

        ttk.Label(second_column, text="Delete City", style="Red.TLabel").pack(pady=5)
        del_frame = tk.Frame(second_column, bg="#f5f5f5")
        del_frame.pack(pady=5)
        ttk.Label(del_frame, text="City:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        del_entry = ttk.Entry(del_frame, width=15, font=("Arial", 10))
        del_entry.grid(row=0, column=1, padx=5, pady=2)
        try:
            del_icon = Image.open(root_path / "assets" / "delete_icon.png")
            del_icon = del_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.del_photo = ImageTk.PhotoImage(del_icon)
            del_btn = tk.Button(del_frame, image=self.del_photo, command=lambda: self.delete_city(del_entry),
                              bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            del_btn.grid(row=1, column=0, columnspan=2, pady=5)
        except FileNotFoundError:
            del_btn = tk.Button(del_frame, text="Delete", command=lambda: self.delete_city(del_entry),
                              font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            del_btn.grid(row=1, column=0, columnspan=2, pady=5)

        third_column = tk.Frame(columns_frame, bg="#f5f5f5", width=300)
        third_column.pack(side="left", fill="y", padx=5)

        ttk.Label(third_column, text="Visitor Analytics", font=("Arial", 12)).pack(pady=5)
        canvas = tk.Canvas(third_column, bg="#f5f5f5", height=400, width=300)
        scrollbar = ttk.Scrollbar(third_column, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for city, count in sorted(self.app.visitors.items()):
            tk.Label(scrollable_frame, text=f"{city}: {count} visits", bg="#f5f5f5", fg="#333", font=("Arial", 10)).pack(anchor="w", padx=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Frame(columns_frame, bg="#ccc", width=2).pack(side="left", fill="y", padx=5)
        tk.Frame(columns_frame, bg="#ccc", width=2).pack(side="left", fill="y", padx=5)

        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill="x", pady=10)

        try:
            undo_icon = Image.open(root_path / "assets" / "undo_icon.png")
            undo_icon = undo_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.undo_photo = ImageTk.PhotoImage(undo_icon)
            undo_btn = tk.Button(buttons_frame, image=self.undo_photo, command=self.undo,
                               bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            undo_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            undo_btn = tk.Button(buttons_frame, text="Undo", command=self.undo,
                               font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            undo_btn.pack(side="left", padx=10)

        try:
            backup_icon = Image.open(root_path / "assets" / "backup_icon.png")
            backup_icon = backup_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.backup_photo = ImageTk.PhotoImage(backup_icon)
            backup_btn = tk.Button(buttons_frame, image=self.backup_photo, command=self.backup,
                                 bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            backup_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            backup_btn = tk.Button(buttons_frame, text="Backup", command=self.backup,
                                 font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            backup_btn.pack(side="left", padx=10)

        try:
            restore_icon = Image.open(root_path / "assets" / "restore_icon.png")
            restore_icon = restore_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.restore_photo = ImageTk.PhotoImage(restore_icon)
            restore_btn = tk.Button(buttons_frame, image=self.restore_photo, command=self.restore,
                                  bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            restore_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            restore_btn = tk.Button(buttons_frame, text="Restore", command=self.restore,
                                  font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            restore_btn.pack(side="left", padx=10)

        try:
            reset_icon = Image.open(root_path / "assets" / "reset_icon.png")
            reset_icon = reset_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.reset_photo = ImageTk.PhotoImage(reset_icon)
            reset_btn = tk.Button(buttons_frame, image=self.reset_photo, command=self.reset_visitors_action,
                                bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            reset_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            reset_btn = tk.Button(buttons_frame, text="Reset Visitors", command=self.reset_visitors_action,
                                font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            reset_btn.pack(side="left", padx=10)

        try:
            map_icon = Image.open(root_path / "assets" / "map_icon.png")
            map_icon = map_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.map_photo = ImageTk.PhotoImage(map_icon)
            map_btn = tk.Button(buttons_frame, image=self.map_photo, command=self.show_whole_map,
                              bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            map_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            map_btn = tk.Button(buttons_frame, text="Whole Map", command=self.show_whole_map,
                              font=("Arial", 12), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            map_btn.pack(side="left", padx=10)

    def add_new_city(self, city_entry, to_entry, dist_entry):
        city = city_entry.get().strip()
        to_city = to_entry.get().strip()
        try:
            distance = int(dist_entry.get().strip())
            if city and to_city and distance > 0:
                if (city, to_city) in [(u, v) for u in self.app.graph.edges for v, _ in self.app.graph.edges[u]] or \
                   (to_city, city) in [(u, v) for u in self.app.graph.edges for v, _ in self.app.graph.edges[u]]:
                    messagebox.showerror("Duplicate Edge", f"An edge already exists between {city} and {to_city}.")
                    return
                self.app.admin.add_city("new", city, to_city, distance=distance)
                self.app.city_list.append(city)
                self.app.city_list = sorted(self.app.graph.edges.keys())
                self.go_frame.start_city["values"] = self.app.city_list
                self.go_frame.end_city["values"] = self.app.city_list
                # Save updated edges
                edges_data = [(u, v, d) for u in self.app.graph.edges for v, d in self.app.graph.edges[u]]
                save_edges(edges_data)
                messagebox.showinfo("Success", f"New city {city} connected to {to_city} with {distance} km.")
            else:
                messagebox.showerror("Invalid Input", "Please fill all fields correctly.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Distance must be a positive integer.")

    def add_intermediate_city(self, city_entry, from_entry, to_entry, dist_from_entry, dist_to_entry):
        city = city_entry.get().strip()
        from_city = from_entry.get().strip()
        to_city = to_entry.get().strip()
        dist_from_str = dist_from_entry.get().strip()
        dist_to_str = dist_to_entry.get().strip()

        try:
            dist_from = int(dist_from_str)
            dist_to = int(dist_to_str)
            if not (city and from_city and to_city and dist_from > 0 and dist_to > 0):
                messagebox.showerror("Invalid Input", "Please fill all fields with positive integers.")
                return

            if from_city not in self.app.graph.edges or to_city not in self.app.graph.edges:
                messagebox.showerror("Error", "Both from and to cities must exist.")
                return

            # Check if direct edge exists and delete it
            if any(v == to_city for v, _ in self.app.graph.edges.get(from_city, [])):
                self.app.graph.delete_edge(from_city, to_city)

            # Add new edges with the specified distances
            self.app.graph.add_edge(from_city, city, dist_from)
            self.app.graph.add_edge(city, to_city, dist_to)

            # Save updated edges
            edges_data = [(u, v, d) for u in self.app.graph.edges for v, d in self.app.graph.edges[u]]
            save_edges(edges_data)

            if city not in self.app.city_list:
                self.app.city_list.append(city)
            self.app.city_list = sorted(self.app.graph.edges.keys())
            self.go_frame.start_city["values"] = self.app.city_list
            self.go_frame.end_city["values"] = self.app.city_list
            messagebox.showinfo("Success", f"Intermediate city {city} added.\n"
                                         f"Distance {from_city} to {city}: {dist_from} km\n"
                                         f"Distance {city} to {to_city}: {dist_to} km")
        except ValueError:
            messagebox.showerror("Invalid Input", "Distances must be positive integers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def add_heritage(self, name_entry, city_entry):
        name = name_entry.get().strip()
        city = city_entry.get().strip()
        if name and city:
            save_heritage(name, city)
            self.app.heritages = load_heritages()
            messagebox.showinfo("Success", f"Heritage '{name}' added in {city}.")
        else:
            messagebox.showerror("Invalid Input", "Name and city cannot be empty.")

    def delete_city(self, del_entry):
        city = del_entry.get().strip()
        if city:
            if city in self.app.graph.edges:
                # Remove all edges connected to the city
                for u in list(self.app.graph.edges.keys()):
                    if city in [v for v, _ in self.app.graph.edges.get(u, [])]:
                        self.app.graph.delete_edge(u, city)
                del self.app.graph.edges[city]
                if city in self.app.city_list:
                    self.app.city_list.remove(city)
                self.go_frame.start_city["values"] = self.app.city_list
                self.go_frame.end_city["values"] = self.app.city_list
                # Save updated edges
                edges_data = [(u, v, d) for u in self.app.graph.edges for v, d in self.app.graph.edges[u]]
                save_edges(edges_data)
                messagebox.showinfo("Success", f"City '{city}' deleted.")
            else:
                messagebox.showwarning("Not Found", f"City '{city}' does not exist.")
        else:
            messagebox.showerror("Invalid Input", "City name cannot be empty.")

    def undo(self):
        try:
            self.app.admin.undo()
            self.app.city_list = sorted(self.app.graph.edges.keys())
            self.go_frame.start_city["values"] = self.app.city_list
            self.go_frame.end_city["values"] = self.app.city_list
            # Save updated edges
            edges_data = [(u, v, d) for u in self.app.graph.edges for v, d in self.app.graph.edges[u]]
            save_edges(edges_data)
            messagebox.showinfo("Success", "Last operation undone.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def backup(self):
        try:
            from utils.file_io import backup_database
            if backup_database(force=True):
                messagebox.showinfo("Success", "Database backed up.")
            else:
                messagebox.showerror("Error", "Backup failed.")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")

    def restore(self):
        try:
            from utils.file_io import restore_database
            if restore_database():
                self.app.graph = Graph()  # Assuming Graph is your custom class
                self.app.edges = load_edges()
                for from_city, to_city, distance in self.app.edges:
                    self.app.graph.add_edge(from_city, to_city, distance)
                self.app.city_list = sorted(self.app.graph.edges.keys())
                self.app.heritages = load_heritages()
                self.app.visitors = load_visitors()
                self.go_frame.start_city["values"] = self.app.city_list
                self.go_frame.end_city["values"] = self.app.city_list
                # Save updated edges
                edges_data = [(u, v, d) for u in self.app.graph.edges for v, d in self.app.graph.edges[u]]
                save_edges(edges_data)
                messagebox.showinfo("Success", "Database restored.")
            else:
                messagebox.showerror("Error", "Restore failed.")
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")

    def reset_visitors_action(self):
        reset_visitors()
        self.app.visitors.clear()
        messagebox.showinfo("Success", "Visitor counts reset.")

    def show_whole_map(self):
        top = tk.Toplevel(self.master)
        top.title("Whole Map")
        top.geometry("800x600")
        top.configure(bg="#f5f5f5")

        # Create a networkx graph from the custom graph
        G = nx.Graph()
        for city in self.app.graph.edges.keys():
            G.add_node(city)
            for neighbor, distance in self.app.graph.edges.get(city, []):
                G.add_edge(city, neighbor, weight=distance)

        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.title("City Network Map", fontsize=16, pad=10)
        nx.draw_networkx_nodes(G, pos, node_color="#4CAF50", node_size=500, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#666", width=2, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, ax=ax)
        ax.set_axis_off()
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)