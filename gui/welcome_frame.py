import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

class WelcomeFrame(tk.Frame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, bg="#f5f5f5")
        self.show_frame = show_frame_callback
        root_path = Path(__file__).resolve().parent.parent

        try:
            image_path = root_path / "assets" / "ethiopia_bg.jpg"
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((1200, 800), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self, bg="#f5f5f5")

        title = tk.Label(self, text="Visit Ethiopia", font=("Helvetica", 48), fg="white", bg="#f5f5f5")
        title.place(relx=0.5, rely=0.4, anchor="center")

        try:
            explore_icon = Image.open(root_path / "assets" / "explore_icon.png")
            explore_icon = explore_icon.resize((40, 40), Image.Resampling.LANCZOS)
            self.explore_photo = ImageTk.PhotoImage(explore_icon)
            explore_btn = tk.Button(self, image=self.explore_photo, command=lambda: show_frame_callback("mode"),
                                 bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            explore_btn.place(relx=0.5, rely=0.6, anchor="center")
        except FileNotFoundError:
            explore_btn = tk.Button(self, text="Explore", command=lambda: show_frame_callback("mode"),
                                 font=("Arial", 16), bg="#f5f5f5", bd=1, highlightbackground="#26A69A", activebackground="#e0e0e0")
            explore_btn.place(relx=0.5, rely=0.6, anchor="center")
        explore_btn.config(highlightthickness=0)