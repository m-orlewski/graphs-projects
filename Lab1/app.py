import os
import tkinter as tk
from tkinter import ttk, filedialog

from src.adj_list import AdjList
from src.adj_matrix import AdjMatrix
from src.inc_matrix import IncMatrix
from src.random_graf import gen_n_l,gen_n_p

import tools.draw
from tools.tkinter import InfoLabel

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Grafy - projekt 1')
        self.window.geometry('1280x720')

        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_columnconfigure(2, weight=2)
        self.window.grid_columnconfigure(3, weight=0)
        self.window.grid_columnconfigure(4, weight=2)

        self.window.grid_rowconfigure(0, weight=1)

        menu = ttk.Frame(self.window)

        self.add_canvas(row=0, column=4)
        self.add_text_frame(row=0, column=2)

        menu.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ttk.Button(menu, text="Wczytaj graf", width=50, command=lambda: self.load_graph()).grid(row=0, column=0, pady=3, columnspan=3)

        ttk.Separator(menu, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text="Konwertuj do macierzy sąsiedztwa", width=50, command=lambda: self.convert_to_adj_matrix()).grid(row=2, column=0, pady=3, columnspan=3)
        ttk.Button(menu, text="Konwertuj do macierzy incydencji", width=50, command=lambda: self.convert_to_inc_matrix()).grid(row=3, column=0, pady=3, columnspan=3)
        ttk.Button(menu, text="Konwertuj do listy sąsiedztwa", width=50, command=lambda: self.convert_to_adj_list()).grid(row=4, column=0, pady=3, columnspan=3)

        ttk.Separator(menu, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Label(menu, text='n').grid(row=6, column=0)
        self.n = ttk.Entry(menu, width=10)
        self.n.grid(row=7, column=0)

        ttk.Label(menu, text='l').grid(row=6, column=1)
        self.l = ttk.Entry(menu, width=10)
        self.l.grid(row=7, column=1)

        ttk.Label(menu, text='p').grid(row=6, column=2)
        self.p = ttk.Entry(menu, width=10)
        self.p.grid(row=7, column=2)

        ttk.Button(menu, text="Graf losowy G(n, l)", width=50, command=lambda: self.generate_n_l_graph()).grid(row=8, column=0, pady=3, columnspan=3)
        ttk.Button(menu, text="Graf losowy G(n, p)", width=50, command=lambda: self.generate_n_p_graph()).grid(row=9, column=0, pady=3, columnspan=3)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')

        self.window.mainloop()

    def load_graph(self):
        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Wczytaj graf",
            filetypes=(('DAT', '*.dat'), )
        )

        with open(filepath, 'r') as f:
            first_line = f.readline()
            identifier = int(first_line.strip())
            if identifier == 1:
                self.graph = IncMatrix(filepath=filepath)
            elif identifier == 2:
                self.graph = AdjList(filepath=filepath)
            else:
                self.graph = AdjMatrix(filepath=filepath)
        
        self.draw_graph()
        self.print_graph()

    def draw_graph(self):
        if self.graph is not None:
            tools.draw.draw_graph(self.canvas, self.graph)

    def convert_to_adj_matrix(self):
        self.graph = self.graph.convert_to_adj_matrix()
        self.print_graph()

    def convert_to_inc_matrix(self):
        self.graph = self.graph.convert_to_inc_matrix()
        self.print_graph()

    def convert_to_adj_list(self):
        self.graph = self.graph.convert_to_adj_list()
        self.print_graph()

    def generate_n_l_graph(self):
        try:
            self.graph = AdjList(data=gen_n_l(int(self.n.get()),int(self.l.get())))
            self.draw_graph()
            self.print_graph()
        except:
            self.result.show_normal("Błędne wartości: n>=2, l>=0, l<=(n*(n-1)/2)")
        
        

    def generate_n_p_graph(self):
        try:
            self.graph = AdjList(data=gen_n_p(int(self.n.get()),float(self.p.get())))
            self.draw_graph()
            self.print_graph()
        except:
            self.result.show_normal("Błędne wartości: n>=2, p>=0, p<=1")

    def add_text_frame(self, row, column):
        frame = ttk.Frame(self.window)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        self.result = InfoLabel(frame, font=("Helvetica", 16))
        self.result.grid(row=1, column=0)
    
    def add_canvas(self, row, column):
        frame = ttk.Frame(self.window)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = tk.Canvas(frame)
        self.canvas.grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def print_graph(self):
        if self.graph is not None:
            self.result.show_normal(str(self.graph))

if __name__ == '__main__':
    app = App()
