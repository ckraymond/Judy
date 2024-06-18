import tkinter as tk

class photoCanvas:
    def __init__(self, root):
        self.canvas = tk.Canvas(root,
                                width = root.winfo_screenwidth(),
                                height = root.winfo_screenheight())
        self.canvas.pack()
