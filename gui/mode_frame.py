import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

class ModeFrame(tk.Frame):
    def __init__(self, master, show_frame_callback, admin_login_callback):
        super().__init__(master, bg="#f5f5f5")
        self.show_frame = show_frame_callback
        self.admin_login = admin_login_callback
        root_path = Path(__file__).resolve().parent.parent

        left = tk.Frame(self, width=600, height=800, bg="#f5f5f5")
        right = tk.Frame(self, width=600, height=800, bg="#f5f5f5")
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        try:
            image_path = root_path / "assets" / "road.jpg"
            road_image = Image.open(image_path)
            road_image = road_image.resize((600, 800), Image.Resampling.LANCZOS)
            self.road_photo = ImageTk.PhotoImage(road_image)
            road_label = tk.Label(left, image=self.road_photo, bg="#f5f5f5")
            road_label.pack(fill="both", expand=True)
        except FileNotFoundError:
            road_label = tk.Label(left, bg="#f5f5f5")

        ttk.Label(right, text="Choose Your Mode", font=("Arial", 18)).pack(pady=20)
        try:
            navigate_icon = Image.open(root_path / "assets" / "navigate_icon.png")
            navigate_icon = navigate_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.nav_photo = ImageTk.PhotoImage(navigate_icon)
            nav_btn = tk.Button(right, image=self.nav_photo, command=lambda: show_frame_callback("go"),
                              bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            nav_btn.pack(pady=10)
        except FileNotFoundError:
            nav_btn = tk.Button(right, text="Navigate", command=lambda: show_frame_callback("go"),
                              font=("Arial", 14), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            nav_btn.pack(pady=10)
        try:
            admin_icon = Image.open(root_path / "assets" / "admin_icon.png")
            admin_icon = admin_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.admin_photo = ImageTk.PhotoImage(admin_icon)
            admin_btn = tk.Button(right, image=self.admin_photo, command=admin_login_callback,
                                bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            admin_btn.pack(pady=10)
        except FileNotFoundError:
            admin_btn = tk.Button(right, text="Admin", command=admin_login_callback,
                                font=("Arial", 14), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            admin_btn.pack(pady=10)