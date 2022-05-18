import tkinter as tk
from tkinter import ttk, filedialog

from src import utils

class App:
    def __init__(self):
        self.graph = None

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 4')
        self.window.geometry('1280x720')

        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_columnconfigure(2, weight=2)
        self.window.grid_columnconfigure(3, weight=0)
        self.window.grid_columnconfigure(4, weight=2)

        self.window.grid_rowconfigure(0, weight=1)

        menu = ttk.Frame(self.window)
        menu.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ttk.Label(menu, text='n').grid(row=0, column=0)
        self.n = ttk.Entry(menu, width=10)
        self.n.grid(row=1, column=0)

        ttk.Label(menu, text='p').grid(row=0, column=1)
        self.p = ttk.Entry(menu, width=10)
        self.p.grid(row=1, column=1, padx=5)

        ttk.Button(menu, text='Wygeneruj digraf G(n,p)', width=50, command=lambda: self.generate_digraph()).grid(row=2, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Znajdź silnie spójne składowe digrafu', width=50, command=lambda: self.find_strongly_connected_components()).grid(row=4, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Wygeneruj silnie spójny digraf z wagami', width=50, command=lambda: self.generate_strongly_connected_digraph()).grid(row=6, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Znajdź odległości pomiędzy wszystkimi parami wierzchołków', width=50, command=lambda: self.find_distances()).grid(row=8, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')
        
        self.window.mainloop()

    def generate_digraph(self):
        pass

    def find_strongly_connected_components(self):
        pass

    def generate_strongly_connected_digraph(self):
        pass

    def find_distances(self):
        pass


if __name__ == '__main__':
    app = App()
