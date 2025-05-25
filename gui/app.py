import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

# Ensure the project root is in sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from gui.welcome_frame import WelcomeFrame
from gui.mode_frame import ModeFrame
from gui.go_frame import GoFrame
from gui.admin_panel import AdminPanel
from core.graph import Graph
from utils.file_io import load_edges, load_heritages, load_password, load_visitors, save_visitors, reset_visitors, save_heritage, save_edges, close_db_connection, initialize_database
from modes.admin_mode import Admin

class EthioNavigatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EthioNavigator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the database
        initialize_database()

        # Initialize the graph and city list
        self.graph = Graph()
        self.edges = load_edges()
        for from_city, to_city, distance in self.edges:
            self.graph.add_edge(from_city, to_city, distance)
        self.city_list = sorted(self.graph.edges.keys())

        self.heritages = load_heritages()
        self.password = load_password()
        self.visitors = load_visitors()
        self.admin = Admin(self.graph)

        self.frames = {}
        self.setup_frames()
        self.show_frame("welcome")

    def on_closing(self):
        close_db_connection()
        self.root.destroy()

    def setup_frames(self):
        self.frames["welcome"] = WelcomeFrame(self.root, self.show_frame)
        self.frames["mode"] = ModeFrame(self.root, self.show_frame, self.admin_login)
        self.go_frame = GoFrame(self.root, self)  # Store GoFrame instance
        self.frames["go"] = self.go_frame
        self.frames["admin"] = AdminPanel(self.root, self, self.go_frame)  # Pass GoFrame to AdminPanel

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

    def admin_login(self):
        from gui.admin_panel import show_login_dialog
        show_login_dialog(self.root, self.password, lambda: self.show_frame("admin"))

if __name__ == '__main__':
    root = tk.Tk()
    app = EthioNavigatorGUI(root)
    root.mainloop()