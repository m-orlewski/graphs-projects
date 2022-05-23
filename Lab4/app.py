import tkinter as tk
from tkinter import ttk
from src.utils import generate_strongly_connected_digraph
from src import utils
from src.digraph import Digraph
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from tools.tkinter import InfoLabel

class App:
    def __init__(self, g=None):
        self.graph = g
        self.f = Figure(figsize=(10,10), dpi=75)
        self.a = self.f.add_subplot(111)
        self.f.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.a.axis('off')

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 4')
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


        ttk.Button(menu, text='Johnson', width=50, command=lambda: self.find_distances_johnson()).grid(row=8, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')
        
        self.window.mainloop()

    def generate_digraph(self):
        n = int(self.n.get())
        p = float(self.p.get())
        if n > 0 and p >= 0.0 and p <= 1.0:
            self.graph = utils.generate_digraph(n, p).graph
            adj_list = Digraph(from_graph=self.graph).to_adj_list()
            self.result.show_normal(str(adj_list))
            self.draw_graph()
        else:
            self.result.show_normal("Bledne parametry")

    def find_strongly_connected_components(self):
        if self.graph:
            comp = utils.Kosaraj(self.graph)
            result = ""
            for key, value in comp.items():
                result += f"{key}: {value}\n"

            self.draw_graph()
            self.result.show_normal(result)

    def generate_strongly_connected_digraph(self):
        n = int(self.n.get())
        p = float(self.p.get())
        if n>0 and p>0 and p<1:
            digraph = generate_strongly_connected_digraph(n,p)
            self.graph = digraph.graph
            self.draw_graph()
            self.result.show_normal(str(digraph.to_adj_list()))
        else:
            self.result.show_normal("Bledne parametry!")


    def find_distances_johnson(self):
        data = utils.johnson(self.graph)
        print(data)
        result = ""
        for el in data:
            result+=str(el)+'\n'
        self.result.show_normal(result)

    def draw_graph(self):
        self.a.clear()
        options = {
            'node_color': 'yellow',
            'node_size': 600,
            'width': 1,
            'arrowstyle': '-|>',
            'arrowsize': 15,
        }
        edge_labels=dict([((u,v,),d['weight'])
                    for u,v,d in self.graph.edges(data=True)])
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos, arrows=isinstance(self.graph, nx.DiGraph), **options, ax=self.a)
        nx.draw_networkx_edge_labels(self.graph,pos,edge_labels=edge_labels, ax=self.a, label_pos=0.4)
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
    g = Digraph()
    g.add_vertices([1,2,3,4,5,6,7]) # przykład silnie spójnego grafu
    g.add_edge(1, 2, weight = 6)
    g.add_edge(1, 3, weight = 3)
    g.add_edge(1, 5, weight = -1)
    g.add_edge(2, 1, weight = 10)
    g.add_edge(2, 3, weight = -5)
    g.add_edge(2, 4, weight = -4)
    g.add_edge(2, 5, weight = 4)
    g.add_edge(2, 7, weight = 4)
    g.add_edge(3, 6, weight = 2)
    g.add_edge(4, 2, weight = 5)
    g.add_edge(4, 7, weight = 9)
    g.add_edge(5, 7, weight = -4)
    g.add_edge(6, 2, weight = 9)
    g.add_edge(7, 6, weight = 4)

    #utils.find_bellman_ford_path(g.graph, 1)
    #utils.johnson(g.graph)

    app = App(g=g.graph)
