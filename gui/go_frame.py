import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

class GoFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#e0f7fa")  # Solid color instead of gradient
        self.app = app
        root_path = Path(__file__).resolve().parent.parent

        # Route Display
        route_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10, relief="flat", bd=1, highlightbackground="#26A69A")
        route_frame.pack(fill="x", pady=10)
        self.output = tk.Text(route_frame, height=6, width=80, bg="#ffffff", fg="#333", font=("Arial", 12), bd=0)
        self.output.pack(pady=5)

        # City Selection
        city_frame = tk.Frame(self, bg="#e0f7fa")
        city_frame.pack(pady=10)
        ttk.Label(city_frame, text="Start City:", font=("Arial", 12)).pack(side="left", padx=5)
        self.start_city = ttk.Combobox(city_frame, values=self.app.city_list, width=25, font=("Arial", 12))
        self.start_city.pack(side="left", padx=5)
        self.start_city.bind('<KeyRelease>', self.autocomplete_city)

        ttk.Label(city_frame, text="Destination City:", font=("Arial", 12)).pack(side="left", padx=5)
        self.end_city = ttk.Combobox(city_frame, values=self.app.city_list, width=25, font=("Arial", 12))
        self.end_city.pack(side="left", padx=5)
        self.end_city.bind('<KeyRelease>', self.autocomplete_city)

        # Mode Selection
        mode_frame = tk.Frame(self, bg="#e0f7fa")
        mode_frame.pack(pady=10)
        self.mode = tk.StringVar(value="normal")
        ttk.Radiobutton(mode_frame, text="Normal", variable=self.mode, value="normal", style="Custom.TRadiobutton").pack(side="left", padx=10)
        ttk.Radiobutton(mode_frame, text="Tourist", variable=self.mode, value="tourist", style="Custom.TRadiobutton").pack(side="left", padx=10)

        # Button Frame
        button_frame = tk.Frame(self, bg="#e0f7fa")
        button_frame.pack(pady=20)

        # Navigate Button
        try:
            navigate_icon = Image.open(root_path / "assets" / "navigate_icon.png")
            navigate_icon = navigate_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.navigate_photo = ImageTk.PhotoImage(navigate_icon)
            navigate_btn = tk.Button(button_frame, image=self.navigate_photo, command=self.navigate,
                                  bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            navigate_btn = tk.Button(button_frame, text="Navigate", command=self.navigate,
                                  font=("Arial", 12), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            navigate_btn.pack(side="left", padx=10)

        # Refresh Button
        try:
            refresh_icon = Image.open(root_path / "assets" / "refresh_icon.png")
            refresh_icon = refresh_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.refresh_photo = ImageTk.PhotoImage(refresh_icon)
            refresh_btn = tk.Button(button_frame, image=self.refresh_photo, command=self.refresh_routes,
                                 bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_routes,
                                 font=("Arial", 12), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            refresh_btn.pack(side="left", padx=10)

        # Back Button
        try:
            back_icon = Image.open(root_path / "assets" / "back_icon.png")
            back_icon = back_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.back_photo = ImageTk.PhotoImage(back_icon)
            back_btn = tk.Button(button_frame, image=self.back_photo, command=lambda: self.app.show_frame("mode"),
                              bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(side="left", padx=10)
        except FileNotFoundError:
            back_btn = tk.Button(button_frame, text="Back", command=lambda: self.app.show_frame("mode"),
                              font=("Arial", 12), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            back_btn.pack(side="left", padx=10)

        # AI Question Section
        ai_frame = tk.Frame(self, bg="#e0f7fa")
        ai_frame.pack(pady=10, fill="x")
        ttk.Label(ai_frame, text="Ask a Question:", font=("Arial", 12)).pack(pady=5)
        self.ai_question = ttk.Entry(ai_frame, width=50, font=("Arial", 12))
        self.ai_question.pack(pady=5)
        try:
            ai_icon = Image.open(root_path / "assets" / "ai_icon.png")
            ai_icon = ai_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.ai_photo = ImageTk.PhotoImage(ai_icon)
            ai_btn = tk.Button(ai_frame, image=self.ai_photo, command=self.ask_ai,
                             bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=5)
        except FileNotFoundError:
            ai_btn = tk.Button(ai_frame, text="Ask AI", command=self.ask_ai,
                             font=("Arial", 12), bg="#ffffff", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            ai_btn.pack(pady=5)
        self.ai_output = tk.Text(ai_frame, height=4, width=60, bg="#ffffff", fg="#333", font=("Arial", 12), bd=0)
        self.ai_output.pack(pady=5)

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
            from utils.pathfinder import find_all_paths
            result = find_all_paths(self.app.graph, start, end)
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
        self.ai_output.insert(tk.END, f"Answer: {question} (Placeholder AI response)")