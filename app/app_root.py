import tkinter as tk

from .app import App


class AppRoot:

    def __init__(self):
        self.root = tk.Tk()

        self.centerize()
        self.root.title('World Development Indicators')
        App(self.root)
        self.root.mainloop()

    def centerize(self):
        w = 900
        h = 700
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.minsize(width=w, height=h)
        self.root.maxsize(width=w, height=h)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(width=False, height=False)
