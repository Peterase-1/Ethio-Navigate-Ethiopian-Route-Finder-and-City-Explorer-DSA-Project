import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import requests
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.Ai_Chatbot import API_KEY, MODEL

class GoFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#f5f5f5")
        self.app = app
        root_path = Path(__file__).resolve().parent.parent

        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns_frame = tk.Frame(main_frame, bg="#f5f5f5")
        columns_frame.pack(fill="both", expand=True)

        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        columns_frame.grid_columnconfigure(2, weight=1)

        col1 = tk.Frame(columns_frame, bg="#f5f5f5")
        col1.grid(row=0, column=0, sticky="nsew", padx=5)

        route_frame = tk.Frame(col1, bg="#ffffff", padx=5, pady=5, relief="flat", bd=1, highlightbackground="#26A69A")
        route_frame.pack(fill="x", pady=2)
        self.output = tk.Text(route_frame, height=3, width=40, bg="#ffffff", fg="#333", font=("Arial", 10), bd=0)
        self.output.pack(pady=2, fill="x")

        city_frame = tk.Frame(col1, bg="#f5f5f5")
        city_frame.pack(pady=2, fill="x")

        tk.Label(city_frame, text="Start City:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.start_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.start_city.grid(row=0, column=1, padx=2, pady=2)
        self.start_city.bind('<KeyRelease>', self.autocomplete_city)

        tk.Label(city_frame, text="Destination City:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.end_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.end_city.grid(row=1, column=1, padx=2, pady=2)
        self.end_city.bind('<KeyRelease>', self.autocomplete_city)

        mode_frame = tk.Frame(col1, bg="#f5f5f5")
        mode_frame.pack(pady=2, fill="x")
        self.mode = tk.StringVar(value="normal")
        tk.Label(mode_frame, text="Mode:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        tk.Radiobutton(mode_frame, text="Normal", variable=self.mode, value="normal", font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=0, column=1, padx=2, pady=2, sticky="w")
        tk.Radiobutton(mode_frame, text="Tourist", variable=self.mode, value="tourist", font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=1, column=1, padx=2, pady=2, sticky="w")

        tk.Frame(columns_frame, bg="#ccc", width=2).grid(row=0, column=1, sticky="ns")

        col2 = tk.Frame(columns_frame, bg="#f5f5f5")
        col2.grid(row=0, column=2, sticky="nsew", padx=5)

        button_frame = tk.Frame(col2, bg="#f5f5f5")
        button_frame.pack(pady=2, fill="both", expand=True)

        try:
            navigate_icon = Image.open(root_path / "assets" / "navigate_icon.png")
            navigate_icon = navigate_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.navigate_photo = ImageTk.PhotoImage(navigate_icon)
            navigate_btn = tk.Button(button_frame, image=self.navigate_photo, command=self.navigate,
                                  bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            navigate_btn = tk.Button(button_frame, text="Navigate", command=self.navigate,
                                  font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(pady=2, fill="x")

        try:
            refresh_icon = Image.open(root_path / "assets" / "refresh_icon.png")
            refresh_icon = refresh_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.refresh_photo = ImageTk.PhotoImage(refresh_icon)
            refresh_btn = tk.Button(button_frame, image=self.refresh_photo, command=self.refresh_routes,
                                 bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_routes,
                                 font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(pady=2, fill="x")

        try:
            back_icon = Image.open(root_path / "assets" / "back_icon.png")
            back_icon = back_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.back_photo = ImageTk.PhotoImage(back_icon)
            back_btn = tk.Button(button_frame, image=self.back_photo, command=lambda: self.app.show_frame("mode"),
                              bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            back_btn = tk.Button(button_frame, text="Back", command=lambda: self.app.show_frame("mode"),
                              font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(pady=2, fill="x")

        tk.Frame(columns_frame, bg="#ccc", width=2).grid(row=0, column=3, sticky="ns")

        col3 = tk.Frame(columns_frame, bg="#f5f5f5")
        col3.grid(row=0, column=4, sticky="nsew", padx=5)

        ai_frame = tk.Frame(col3, bg="#f5f5f5")
        ai_frame.pack(fill="both", expand=True, pady=2)

        tk.Label(ai_frame, text="Ask a Question:", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w", padx=2, pady=2)
        self.ai_question = ttk.Entry(ai_frame, width=30, font=("Arial", 10))
        self.ai_question.pack(pady=2, fill="x")
        try:
            ai_icon = Image.open(root_path / "assets" / "ai_icon.png")
            ai_icon = ai_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.ai_photo = ImageTk.PhotoImage(ai_icon)
            ai_btn = tk.Button(ai_frame, image=self.ai_photo, command=self.ask_ai,
                             bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            ai_btn = tk.Button(ai_frame, text="Ask AI", command=self.ask_ai,
                             font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=2, fill="x")
        self.ai_output = tk.Text(ai_frame, height=10, width=40, bg="#ffffff", fg="#333", font=("Arial", 10), bd=0)  # Increased height
        self.ai_output.pack(pady=2, fill="both", expand=True)

    def autocomplete_city(self, event):
        widget = event.widget
        value = widget.get().strip().lower()
        if value == "":
            widget['values'] = self.app.city_list
        else:
            matches = [city for city in self.app.city_list if value in city.lower()]
            widget['values'] = matches

    def navigate(self):
        start = self.start_city.get()
        end = self.end_city.get()
        mode = self.mode.get()

        if not start or not end:
            messagebox.showerror("Input Error", "Please select both start and destination cities.")
            return

        self.app.all_paths = []
        if mode == "normal":
            from utils.pathfinder import find_shortest_paths
            result = find_shortest_paths(self.app.graph, start, end)
            self.app.all_paths = result
            self.display_routes(result)
        elif mode == "tourist":
            from core.heritage_manager import find_tourist_paths
            result = find_tourist_paths(self.app.graph, start, end, self.app.heritages)
            self.app.all_paths = result
            self.display_tourist_routes(result)
        else:
            messagebox.showerror("Mode Error", "Please select a mode.")
            return

        self.app.visitors[end] = self.app.visitors.get(end, 0) + 1
        from utils.file_io import save_visitors
        save_visitors(self.app.visitors)

    def refresh_routes(self):
        self.navigate()

    def display_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            if self.app.all_paths:
                shortest_cost, shortest_path = min(self.app.all_paths, key=lambda x: x[0])
                time = shortest_cost * 2 / 60
                self.output.insert(tk.END, f"Route: {' → '.join(shortest_path)}\n")
                self.output.insert(tk.END, f"Distance: {shortest_cost} km\nTravel Time: {time:.2f} hours")

    def display_tourist_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            if self.app.all_paths:
                shortest_cost, shortest_path, shortest_sites = min(self.app.all_paths, key=lambda x: x[0])
                time = shortest_cost * 2 / 60
                self.output.insert(tk.END, f"Route: {' → '.join(shortest_path)}\n")
                self.output.insert(tk.END, f"Distance: {shortest_cost} km\nTravel Time: {time:.2f} hours\nHeritage Sites: {', '.join(shortest_sites)}")

    def ask_ai(self):
        question = self.ai_question.get().strip()
        if not question:
            messagebox.showerror("Input Error", "Please enter a question.")
            return
        self.ai_output.delete('1.0', tk.END)
        self.ai_output.insert(tk.END, f"You: {question}\n", "user")  # User message
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": question}]
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            result = response.json()
            if "choices" in result:
                bot_reply = result["choices"][0]["message"]["content"]
                self.ai_output.insert(tk.END, f"Bot: {bot_reply}\n", "bot")  # Bot response
                # Check if user requested a graph piece
                if "show graph" in question.lower() and "from" in question.lower() and "to" in question.lower():
                    start = next((word for word in question.lower().split() if word in self.app.city_list), None)
                    end = next((word for word in question.lower().split() if word in self.app.city_list and word != start), None)
                    if start and end:
                        self.display_graph_piece(start, end)
            else:
                self.ai_output.insert(tk.END, f"Bot: Error: {result}\n", "bot")
        except Exception as e:
            self.ai_output.insert(tk.END, f"Bot: Error: {str(e)}\n", "bot")
        self.ai_question.delete(0, tk.END)

    def display_graph_piece(self, start, end):
        G = nx.Graph()
        visited = set()
        def add_path(city):
            if city not in visited:
                visited.add(city)
                G.add_node(city)
                for neighbor, distance in self.app.graph.get_neighbors(city):
                    G.add_edge(city, neighbor, weight=distance)
                    add_path(neighbor)

        add_path(start)
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.title(f"Graph Piece from {start} to {end}", fontsize=12, pad=5)
        nx.draw_networkx_nodes(G, pos, node_color="#4CAF50", node_size=300, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#666", width=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=6, font_color="white", ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=4, ax=ax)
        ax.set_axis_off()
        plt.tight_layout()

        # Clear previous graph if exists
        for widget in self.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)

    def __init__(self, master, app):
        super().__init__(master, bg="#f5f5f5")
        self.app = app
        root_path = Path(__file__).resolve().parent.parent

        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns_frame = tk.Frame(main_frame, bg="#f5f5f5")
        columns_frame.pack(fill="both", expand=True)

        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        columns_frame.grid_columnconfigure(2, weight=1)

        col1 = tk.Frame(columns_frame, bg="#f5f5f5")
        col1.grid(row=0, column=0, sticky="nsew", padx=5)

        route_frame = tk.Frame(col1, bg="#ffffff", padx=5, pady=5, relief="flat", bd=1, highlightbackground="#26A69A")
        route_frame.pack(fill="x", pady=2)
        self.output = tk.Text(route_frame, height=3, width=40, bg="#ffffff", fg="#333", font=("Arial", 10), bd=0)
        self.output.pack(pady=2, fill="x")

        city_frame = tk.Frame(col1, bg="#f5f5f5")
        city_frame.pack(pady=2, fill="x")

        tk.Label(city_frame, text="Start City:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.start_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.start_city.grid(row=0, column=1, padx=2, pady=2)
        self.start_city.bind('<KeyRelease>', self.autocomplete_city)

        tk.Label(city_frame, text="Destination City:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.end_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.end_city.grid(row=1, column=1, padx=2, pady=2)
        self.end_city.bind('<KeyRelease>', self.autocomplete_city)

        mode_frame = tk.Frame(col1, bg="#f5f5f5")
        mode_frame.pack(pady=2, fill="x")
        self.mode = tk.StringVar(value="normal")
        tk.Label(mode_frame, text="Mode:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        tk.Radiobutton(mode_frame, text="Normal", variable=self.mode, value="normal", font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=0, column=1, padx=2, pady=2, sticky="w")
        tk.Radiobutton(mode_frame, text="Tourist", variable=self.mode, value="tourist", font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=1, column=1, padx=2, pady=2, sticky="w")

        tk.Frame(columns_frame, bg="#ccc", width=2).grid(row=0, column=1, sticky="ns")

        col2 = tk.Frame(columns_frame, bg="#f5f5f5")
        col2.grid(row=0, column=2, sticky="nsew", padx=5)

        button_frame = tk.Frame(col2, bg="#f5f5f5")
        button_frame.pack(pady=2, fill="both", expand=True)

        try:
            navigate_icon = Image.open(root_path / "assets" / "navigate_icon.png")
            navigate_icon = navigate_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.navigate_photo = ImageTk.PhotoImage(navigate_icon)
            navigate_btn = tk.Button(button_frame, image=self.navigate_photo, command=self.navigate,
                                  bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            navigate_btn = tk.Button(button_frame, text="Navigate", command=self.navigate,
                                  font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(pady=2, fill="x")

        try:
            refresh_icon = Image.open(root_path / "assets" / "refresh_icon.png")
            refresh_icon = refresh_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.refresh_photo = ImageTk.PhotoImage(refresh_icon)
            refresh_btn = tk.Button(button_frame, image=self.refresh_photo, command=self.refresh_routes,
                                 bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_routes,
                                 font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(pady=2, fill="x")

        try:
            back_icon = Image.open(root_path / "assets" / "back_icon.png")
            back_icon = back_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.back_photo = ImageTk.PhotoImage(back_icon)
            back_btn = tk.Button(button_frame, image=self.back_photo, command=lambda: self.app.show_frame("mode"),
                              bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            back_btn = tk.Button(button_frame, text="Back", command=lambda: self.app.show_frame("mode"),
                              font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(pady=2, fill="x")

        tk.Frame(columns_frame, bg="#ccc", width=2).grid(row=0, column=3, sticky="ns")

        col3 = tk.Frame(columns_frame, bg="#f5f5f5")
        col3.grid(row=0, column=4, sticky="nsew", padx=5)

        ai_frame = tk.Frame(col3, bg="#f5f5f5")
        ai_frame.pack(fill="both", expand=True, pady=2)

        tk.Label(ai_frame, text="Ask a Question:", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w", padx=2, pady=2)
        self.ai_question = ttk.Entry(ai_frame, width=30, font=("Arial", 10))
        self.ai_question.pack(pady=2, fill="x")
        try:
            ai_icon = Image.open(root_path / "assets" / "ai_icon.png")
            ai_icon = ai_icon.resize((25, 25), Image.Resampling.LANCZOS)
            self.ai_photo = ImageTk.PhotoImage(ai_icon)
            ai_btn = tk.Button(ai_frame, image=self.ai_photo, command=self.ask_ai,
                             bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=2, fill="x")
        except FileNotFoundError:
            ai_btn = tk.Button(ai_frame, text="Ask AI", command=self.ask_ai,
                             font=("Arial", 10), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=2, fill="x")
        self.ai_output = tk.Text(ai_frame, height=10, width=40, bg="#ffffff", fg="#333", font=("Arial", 10), bd=0)
        self.ai_output.tag_configure("user", foreground="blue")
        self.ai_output.tag_configure("bot", foreground="green")
        self.ai_output.pack(pady=2, fill="both", expand=True)

    def autocomplete_city(self, event):
        widget = event.widget
        value = widget.get().strip().lower()
        if value == "":
            widget['values'] = self.app.city_list
        else:
            matches = [city for city in self.app.city_list if value in city.lower()]
            widget['values'] = matches

    def navigate(self):
        start = self.start_city.get()
        end = self.end_city.get()
        mode = self.mode.get()

        if not start or not end:
            messagebox.showerror("Input Error", "Please select both start and destination cities.")
            return

        self.app.all_paths = []
        if mode == "normal":
            from utils.pathfinder import find_shortest_paths
            result = find_shortest_paths(self.app.graph, start, end)
            self.app.all_paths = result
            self.display_routes(result)
        elif mode == "tourist":
            from core.heritage_manager import find_tourist_paths
            result = find_tourist_paths(self.app.graph, start, end, self.app.heritages)
            self.app.all_paths = result
            self.display_tourist_routes(result)
        else:
            messagebox.showerror("Mode Error", "Please select a mode.")
            return

        self.app.visitors[end] = self.app.visitors.get(end, 0) + 1
        from utils.file_io import save_visitors
        save_visitors(self.app.visitors)

    def refresh_routes(self):
        self.navigate()

    def display_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            if self.app.all_paths:
                shortest_cost, shortest_path = min(self.app.all_paths, key=lambda x: x[0])
                time = shortest_cost * 2 / 60
                self.output.insert(tk.END, f"Route: {' → '.join(shortest_path)}\n")
                self.output.insert(tk.END, f"Distance: {shortest_cost} km\nTravel Time: {time:.2f} hours")

    def display_tourist_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            if self.app.all_paths:
                shortest_cost, shortest_path, shortest_sites = min(self.app.all_paths, key=lambda x: x[0])
                time = shortest_cost * 2 / 60
                self.output.insert(tk.END, f"Route: {' → '.join(shortest_path)}\n")
                self.output.insert(tk.END, f"Distance: {shortest_cost} km\nTravel Time: {time:.2f} hours\nHeritage Sites: {', '.join(shortest_sites)}")

    def ask_ai(self):
        question = self.ai_question.get().strip()
        if not question:
            messagebox.showerror("Input Error", "Please enter a question.")
            return
        self.ai_output.insert(tk.END, f"You: {question}\n", "user")  # User message
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": question}]
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            result = response.json()
            if "choices" in result:
                bot_reply = result["choices"][0]["message"]["content"]
                self.ai_output.insert(tk.END, f"Bot: {bot_reply}\n", "bot")  # Bot response
                # Check if user requested a graph piece
                if "show graph" in question.lower() and "from" in question.lower() and "to" in question.lower():
                    start = next((word for word in question.lower().split() if word in self.app.city_list), None)
                    end = next((word for word in question.lower().split() if word in self.app.city_list and word != start), None)
                    if start and end:
                        self.display_graph_piece(start, end)
            else:
                self.ai_output.insert(tk.END, f"Bot: Error: {result}\n", "bot")
        except Exception as e:
            self.ai_output.insert(tk.END, f"Bot: Error: {str(e)}\n", "bot")
        self.ai_question.delete(0, tk.END)

    def display_graph_piece(self, start, end):
        G = nx.Graph()
        visited = set()
        def add_path(city):
            if city not in visited:
                visited.add(city)
                G.add_node(city)
                for neighbor, distance in self.app.graph.get_neighbors(city):
                    G.add_edge(city, neighbor, weight=distance)
                    add_path(neighbor)

        add_path(start)
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.title(f"Graph Piece from {start} to {end}", fontsize=12, pad=5)
        nx.draw_networkx_nodes(G, pos, node_color="#4CAF50", node_size=300, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#666", width=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=6, font_color="white", ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=4, ax=ax)
        ax.set_axis_off()
        plt.tight_layout()

        # Clear previous graph if exists
        for widget in self.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)