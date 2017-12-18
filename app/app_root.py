import tkinter as tk

from .threaded_client import ThreadedClient


class AppRoot:
    WIDTH = 900
    HEIGHT = 700

    def __init__(self):
        self.root = tk.Tk()

        self.to_center()
        self.root.title('World Development Indicators')
        ThreadedClient(self.root)
        self.root.mainloop()

    def to_center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (self.WIDTH/2)
        y = (hs/2) - (self.HEIGHT/2)
        self.root.minsize(width=self.WIDTH, height=self.HEIGHT)
        self.root.maxsize(width=self.WIDTH, height=self.HEIGHT)
        self.root.geometry('%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, x, y))
        self.root.resizable(width=False, height=False)
