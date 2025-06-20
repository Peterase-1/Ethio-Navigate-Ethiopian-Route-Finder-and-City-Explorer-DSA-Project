import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
from PIL import Image, ImageTk
import requests
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.Ai_Chatbot import API_KEY, MODEL
import heapq
class GoFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#f5f5f5")
        self.app = app
        root_path = Path(__file__).resolve().parent.parent
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        # Left column: Route and controls
        left_frame = tk.Frame(self, bg="#f5f5f5")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Modern route display
        route_frame = tk.LabelFrame(left_frame, text="Route Information", font=("Arial", 12, "bold"), 
                                  bg="#ffffff", padx=10, pady=10)
        route_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.output = scrolledtext.ScrolledText(route_frame, height=8, wrap=tk.WORD, 
                                              font=("Arial", 11), bg="#ffffff", fg="#333")
        self.output.pack(fill="both", expand=True)
        
        # City selection
        city_frame = tk.Frame(left_frame, bg="#f5f5f5")
        city_frame.pack(fill="x", pady=5)
        
        tk.Label(city_frame, text="Start City:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.start_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.start_city.grid(row=0, column=1, padx=5, pady=5)
        self.start_city.bind('<KeyRelease>', self.autocomplete_city)
        
        tk.Label(city_frame, text="Destination:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.end_city = ttk.Combobox(city_frame, values=self.app.city_list, width=20, font=("Arial", 10))
        self.end_city.grid(row=1, column=1, padx=5, pady=5)
        self.end_city.bind('<KeyRelease>', self.autocomplete_city)
        
        # Mode selection
        mode_frame = tk.Frame(left_frame, bg="#f5f5f5")
        mode_frame.pack(fill="x", pady=5)
        self.mode = tk.StringVar(value="normal")
        tk.Label(mode_frame, text="Mode:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Radiobutton(mode_frame, text="Normal", variable=self.mode, value="normal", 
                      font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=0, column=1, padx=5, pady=5)
        tk.Radiobutton(mode_frame, text="Tourist", variable=self.mode, value="tourist", 
                      font=("Arial", 10), bg="#f5f5f5", fg="#26A69A").grid(row=0, column=2, padx=5, pady=5)
        
        # Control buttons
        btn_frame = tk.Frame(left_frame, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=10)
        
        # Button styling
        btn_style = {"bg": "#ffffff", "bd": 0, "highlightthickness": 0, 
                    "activebackground": "#e0e0e0", "font": ("Arial", 10)}
        
        tk.Button(btn_frame, text="Navigate", command=self.navigate, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_routes, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=lambda: self.app.show_frame("mode"), **btn_style).pack(side="left", padx=5)
        
        # Search and Sort panel
        search_frame = tk.LabelFrame(left_frame, text="Search & Sort", font=("Arial", 12, "bold"), 
                                   bg="#ffffff", padx=10, pady=10)
        search_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Current city for sorting
        tk.Label(search_frame, text="Current City:", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sort_city_entry = ttk.Entry(search_frame, width=15, font=("Arial", 10))
        self.sort_city_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(search_frame, text="Sort Cities", command=self.sort_by_current_city, 
                 bg="#f0f0f0", bd=0, highlightthickness=0, activebackground="#e0e0e0").grid(row=0, column=2, padx=5)
        
        # Search entry
        tk.Label(search_frame, text="Search City:", font=("Arial", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame, width=15, font=("Arial", 10))
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(search_frame, text="Search", command=self.search_city, 
                 bg="#f0f0f0", bd=0, highlightthickness=0, activebackground="#e0e0e0").grid(row=1, column=2, padx=5)
        
        # Search results
        self.search_results = tk.Listbox(search_frame, height=4, font=("Arial", 10))
        self.search_results.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Right column: AI Chat and Recent Cities
        right_frame = tk.Frame(self, bg="#f5f5f5")
        right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(0, weight=3)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Enhanced AI Chat
        ai_frame = tk.LabelFrame(right_frame, text="AI Assistant", font=("Arial", 12, "bold"), 
                               bg="#ffffff", padx=10, pady=10)
        ai_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        ai_frame.grid_columnconfigure(0, weight=1)
        ai_frame.grid_rowconfigure(0, weight=1)
        
        self.ai_output = scrolledtext.ScrolledText(ai_frame, height=15, wrap=tk.WORD, 
                                                 font=("Arial", 10), bg="#ffffff", fg="#333")
        self.ai_output.grid(row=0, column=0, sticky="nsew")
        self.ai_output.tag_configure("user", foreground="blue")
        self.ai_output.tag_configure("bot", foreground="green")
        
        # Input area below output
        input_frame = tk.Frame(ai_frame, bg="#ffffff")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        self.ai_question = ttk.Entry(input_frame, width=30, font=("Arial", 10))
        self.ai_question.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(input_frame, text="Ask", command=self.ask_ai, bg="#f0f0f0", bd=0, 
                 highlightthickness=0, activebackground="#e0e0e0").pack(side="right")
        
        # Recently viewed cities (using stack)
        recent_frame = tk.LabelFrame(right_frame, text="Recently Viewed", font=("Arial", 12, "bold"), 
                                  bg="#ffffff", padx=10, pady=10)
        recent_frame.grid(row=1, column=0, sticky="nsew")
        
        self.recent_list = tk.Listbox(recent_frame, height=5, font=("Arial", 10))
        self.recent_list.pack(fill="both", expand=True)
        self.update_recent_list()

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

        # Add to recent cities stack
        if end not in self.app.recent_cities:
            self.app.recent_cities.append(end)
            if len(self.app.recent_cities) > 5:  # Limit to 5 most recent
                self.app.recent_cities.pop(0)
            self.update_recent_list()

        # Update visitor count
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
                self.output.insert(tk.END, f"Distance: {shortest_cost} km\nTravel Time: {time:.2f} hours\n")
                self.output.insert(tk.END, f"Heritage Sites: {', '.join(shortest_sites)}")

    def ask_ai(self):
        question = self.ai_question.get().strip()
        if not question:
            messagebox.showerror("Input Error", "Please enter a question.")
            return
        self.ai_output.insert(tk.END, f"You: {question}\n", "user")
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
                self.ai_output.insert(tk.END, f"Bot: {bot_reply}\n\n", "bot")
            else:
                self.ai_output.insert(tk.END, f"Bot: Error: {result}\n", "bot")
        except Exception as e:
            self.ai_output.insert(tk.END, f"Bot: Error: {str(e)}\n", "bot")
        self.ai_question.delete(0, tk.END)

    def update_recent_list(self):
        self.recent_list.delete(0, tk.END)
        for city in reversed(self.app.recent_cities):  # Show most recent first
            self.recent_list.insert(tk.END, city)

    def sort_by_current_city(self):
        current_city = self.sort_city_entry.get().strip()
        if not current_city or current_city not in self.app.graph.edges:
            messagebox.showerror("Invalid Input", "Please enter a valid current city.")
            return

        # Get distances using Dijkstra's algorithm
        distances = {}
        pq = [(0, current_city)]
        visited = set()
        
        while pq:
            dist, city = heapq.heappop(pq)
            if city in visited:
                continue
            visited.add(city)
            distances[city] = dist
            
            for neighbor, distance in self.app.graph.get_neighbors(city):
                if neighbor not in visited:
                    heapq.heappush(pq, (dist + distance, neighbor))
        
        # Remove current city and sort
        if current_city in distances:
            del distances[current_city]
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        
        # Show results
        self.search_results.delete(0, tk.END)
        for city, dist in sorted_distances:
            self.search_results.insert(tk.END, f"{city}: {dist} km")

    def search_city(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return
            
        results = [city for city in self.app.city_list if query in city.lower()]
        self.search_results.delete(0, tk.END)
        
        if not results:
            self.search_results.insert(tk.END, "No matching cities found")
        else:
            for city in results:
                self.search_results.insert(tk.END, city)