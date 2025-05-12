import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
from pathlib import Path

# Ensure the project root is in sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from core.graph import Graph
from utils.file_io import load_edges, load_heritages, load_password
from modes.normal_mode import normal_navigator
from modes.tourist_mode import tourist_navigator
from modes.admin_mode import Admin


class EthioNavigatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethio Navigator")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.graph = self.initialize_graph()
        self.heritages = load_heritages("data/heritages.txt")
        self.password = load_password("data/admin_password.txt")
        self.admin = Admin(self.graph, self.password)

        self.frames = {}
        self.setup_frames()
        self.show_frame("welcome")

    def initialize_graph(self):
        graph = Graph()
        for from_city, to_city, distance in load_edges("data/cities.txt"):
            graph.add_edge(from_city, to_city, distance)
        return graph

    def setup_frames(self):
        self.frames["welcome"] = self.create_welcome_frame()
        self.frames["mode"] = self.create_mode_frame()
        self.frames["go"] = self.create_go_frame()

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

    def create_welcome_frame(self):
        frame = tk.Frame(self.root)

        bg_image = Image.open("assets/ethiopia_bg.jpg")
        bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(frame, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        title = tk.Label(frame, text="Visit Ethiopia", font=("Helvetica", 36, "bold"), bg="#000", fg="white")
        title.place(relx=0.5, rely=0.3, anchor="center")

        explore_btn = ttk.Button(frame, text="Explore", command=lambda: self.show_frame("mode"))
        explore_btn.place(relx=0.5, rely=0.5, anchor="center")

        return frame

    def create_mode_frame(self):
        frame = tk.Frame(self.root)

        left = tk.Frame(frame, width=450, height=600)
        right = tk.Frame(frame, width=450, height=600, bg="#f0f0f0")
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        road_image = Image.open("assets/road.jpg")
        road_image = road_image.resize((450, 600), Image.Resampling.LANCZOS)
        self.road_photo = ImageTk.PhotoImage(road_image)
        road_label = tk.Label(left, image=self.road_photo)
        road_label.pack(fill="both", expand=True)

        ttk.Label(right, text="Choose Mode", font=("Arial", 20)).pack(pady=50)
        ttk.Button(right, text="Go", width=20, command=lambda: self.show_frame("go")).pack(pady=20)
        ttk.Button(right, text="Admin", width=20, command=self.admin_login).pack(pady=20)

        return frame

    def create_go_frame(self):
        frame = tk.Frame(self.root, padx=20, pady=20)

        ttk.Label(frame, text="Start City:").pack()
        self.city_list = sorted(self.graph.edges.keys())
        self.start_city = ttk.Combobox(frame, values=self.city_list)
        self.start_city.pack()

        ttk.Label(frame, text="Destination City:").pack()
        self.end_city = ttk.Combobox(frame, values=self.city_list)
        self.end_city.pack()

        self.mode = tk.StringVar()
        ttk.Radiobutton(frame, text="Normal", variable=self.mode, value="normal").pack(anchor="w")
        ttk.Radiobutton(frame, text="Tourist", variable=self.mode, value="tourist").pack(anchor="w")

        ttk.Button(frame, text="Navigate", command=self.navigate).pack(pady=10)

        self.output = tk.Text(frame, height=15, width=100)
        self.output.pack()

        ttk.Button(frame, text="Back", command=lambda: self.show_frame("mode")).pack(pady=5)

        return frame

    def admin_login(self):
        top = tk.Toplevel(self.root)
        top.title("Admin Login")
        top.geometry("300x150")

        ttk.Label(top, text="Enter Admin Password:").pack(pady=10)
        pass_entry = ttk.Entry(top, show="*")
        pass_entry.pack()

        def check():
            if pass_entry.get() == self.password:
                top.destroy()
                self.admin_panel()
            else:
                messagebox.showerror("Access Denied", "Incorrect password")

        ttk.Button(top, text="Login", command=check).pack(pady=10)

    def navigate(self):
        start = self.start_city.get()
        end = self.end_city.get()
        mode = self.mode.get()

        if not start or not end:
            messagebox.showerror("Input Error", "Please select both start and destination cities.")
            return

        if mode == "normal":
            result = normal_navigator(self.graph, start, end)
            self.display_routes(result)

        elif mode == "tourist":
            result = tourist_navigator(self.graph, start, end, self.heritages)
            self.display_tourist_routes(result)
        else:
            messagebox.showerror("Mode Error", "Please select a mode.")

    def display_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            for cost, path in result:
                self.output.insert(tk.END, f"Path: {' -> '.join(path)}, Cost: {cost}km\n")

    def display_tourist_routes(self, result):
        self.output.delete('1.0', tk.END)
        if isinstance(result, str):
            self.output.insert(tk.END, result)
        else:
            for cost, path, sites in result:
                self.output.insert(tk.END, f"Path: {' -> '.join(path)} | Cost: {cost}km | Heritage Sites: {', '.join(sites)}\n")

    def admin_panel(self):
        top = tk.Toplevel(self.root)
        top.title("Admin Control Panel")

        ttk.Label(top, text="Add New City Connection: (From, To, Distance)").pack()
        from_entry = ttk.Entry(top)
        from_entry.pack()
        to_entry = ttk.Entry(top)
        to_entry.pack()
        dist_entry = ttk.Entry(top)
        dist_entry.pack()

        def add():
            try:
                dist = int(dist_entry.get())
                self.admin.add_city(from_entry.get(), to_entry.get(), dist)
                messagebox.showinfo("Success", "City connection added.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Distance must be an integer.")

        ttk.Button(top, text="Add Connection", command=add).pack(pady=5)

        ttk.Label(top, text="Delete City:").pack()
        del_entry = ttk.Entry(top)
        del_entry.pack()

        def delete():
            self.admin.delete_city(del_entry.get())
            messagebox.showinfo("Success", "City deleted from graph.")

        ttk.Button(top, text="Delete City", command=delete).pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    app = EthioNavigatorGUI(root)
    root.mainloop()
