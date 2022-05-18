import tkinter as tk
from tkinter import ttk, filedialog

from src import utils

class App:
    def __init__(self):
        self.graph = None

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 3')
        self.window.geometry('1280x720')

        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_columnconfigure(2, weight=2)
        self.window.grid_columnconfigure(3, weight=0)
        self.window.grid_columnconfigure(4, weight=2)

        self.window.grid_rowconfigure(0, weight=1)

        menu = ttk.Frame(self.window)
        menu.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ttk.Label(menu, text='n').grid(row=0, column=0, columnspan=3, padx=3, pady=5)
        self.n = ttk.Entry(menu, width=50)
        self.n.grid(row=1, column=0)

        ttk.Button(menu, text='Wygeneruj graf losowy o n wierzchołkach', width=50, command=lambda: self.generate_random_graph_with_weights()).grid(row=2, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Dijkstra', width=50, command=lambda: self.dijkstra()).grid(row=4, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Wyznacz macierz odległości', width=50, command=lambda: self.calculate_distance_matrix()).grid(row=6, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Wyznacz centrum i minmax grafu', width=50, command=lambda: self.find_center_and_minmax_node()).grid(row=8, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Wyznacz minimalne drzewo rozpinające', width=50, command=lambda: self.minimum_spanning_tree()).grid(row=10, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=11, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')

        self.window.mainloop()

    def generate_random_graph_with_weights(self):
        pass

    def dijkstra(self):
        pass

    def calculate_distance_matrix(self):
        pass

    def find_center_and_minmax_node(self):
        pass

    def minimum_spanning_tree(self):
        pass




if __name__ == '__main__':
    app = App()
