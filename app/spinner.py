import tkinter as tk

from os import path

DIR_PATH = path.abspath(path.dirname(__file__))


class Spinner:

    def __init__(self, master):
        self.master = master

        self.frames = [tk.PhotoImage(file=path.join(DIR_PATH, '../assets/img/spinner.gif'),
                                     format='gif -index %i' % (i)) for i in range(30)]
        self.spinner_label = tk.Label(self.master)
        self.spinner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.listener = self.master.after(0, self.update_spinner, 0)

    def update_spinner(self, ind):
        frame = self.frames[ind]
        ind += 1

        self.spinner_label.configure(image=frame)

        self.listener = self.master.after(30, self.update_spinner, 0 if ind == 30 else ind)

    def destroy(self):
        self.master.after_cancel(self.listener)
        self.spinner_label.destroy()
