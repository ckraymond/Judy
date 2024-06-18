import tkinter as tk

class photoCanvas:
    def __init__(self, root, screen_dims):
        self.canvas = tk.Canvas(root,
                                width = screen_dims['x'],
                                height = screen_dims['y'],
                                bg='#000000')
        self.canvas.pack()
