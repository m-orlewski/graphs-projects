import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, filedialog
import random
from tools.tkinter import InfoLabel

from src import utils

matplotlib.use('TkAgg')

class App:
    def __init__(self):
        self.f = Figure(figsize=(10,10), dpi=75)
        self.a = self.f.add_subplot(111)
        self.f.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.a.axis('off')

        self.graph = None

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 3')
        self.window.geometry('1600x900')

        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_columnconfigure(2, weight=2)
        self.window.grid_columnconfigure(3, weight=0)
        self.window.grid_columnconfigure(4, weight=4)

        self.window.grid_rowconfigure(0, weight=1)

        self.add_canvas(0,4)
        self.add_text_frame(0,2)

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

        ttk.Button(menu, text='Wyznacz minimalne drzewo rozpinające(Prim)', width=50, command=lambda: self.minimum_spanning_tree_Prim()).grid(row=10, column=0, pady=3, columnspan=3)
        ttk.Button(menu, text='Wyznacz minimalne drzewo rozpinające(Kruskal)', width=50, command=lambda: self.minimum_spanning_tree_Kruskal()).grid(row=11, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=12, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')

        self.window.mainloop()

    def generate_random_graph_with_weights(self):
        n=int(self.n.get())
        seq=[random.randrange(1,n-1) for _ in range(n)]
        while utils.check_sequence(seq.copy())==False:
            seq=[random.randrange(1,n-1) for _ in range(n)]

        self.graph = utils.create_graph_from_sequence(seq)
        self.draw_graph()
        pass

    def dijkstra(self):
        utils.dijkstra(self.graph,1)
        self.result.show_normal(utils.print_graph_paths(self.graph,1))

    def calculate_distance_matrix(self):
        dmat = utils.create_dist_matrix(self.graph)
        output = ""
        for el in dmat:
            output+=str(el)
            output+="\n"
        self.result.show_normal(output)

    def find_center_and_minmax_node(self):
        output = f'Centrum = {utils.sum_dist_min(self.graph)[0]} (suma odl.: {utils.sum_dist_min(self.graph)[1]})'
        output+= f'\nCentrum minimax = {utils.max_dist_min(self.graph)[0]} (odl. od najdalszego: {utils.max_dist_min(self.graph)[1]})'
        self.result.show_normal(output)

    def minimum_spanning_tree_Prim(self):
        self.graph=utils.minimal_spanning_tree_Prim(self.graph)
        self.draw_graph()
    
    def minimum_spanning_tree_Kruskal(self):
        self.graph=utils.minimal_spanning_tree_Kruskal(self.graph)
        self.draw_graph()

    def draw_graph(self):
        self.a.clear()
        options = {
            'node_color': 'yellow',
            'node_size': 1000,
            'width': 1,
            'arrowstyle': '-|>',
            'arrowsize': 15,
        }
        edge_labels=dict([((u,v,),d['weight'])
                    for u,v,d in self.graph.edges(data=True)])
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos, arrows=isinstance(self.graph, nx.DiGraph), **options, ax=self.a)
        nx.draw_networkx_edge_labels(self.graph,pos,edge_labels=edge_labels, ax=self.a)
        self.canvas.draw()
        
    def add_canvas(self, row, column):
        frame = ttk.Frame(self.window)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = FigureCanvasTkAgg(self.f, master=frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def add_text_frame(self, row, column):
        frame = ttk.Frame(self.window)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        self.result = InfoLabel(frame, font=("Helvetica", 16))
        self.result.grid(row=1, column=0)

if __name__ == '__main__':
    app = App()
