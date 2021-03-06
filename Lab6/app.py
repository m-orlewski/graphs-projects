import tkinter as tk
from tkinter import ttk
from src import utils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from tools.tkinter import InfoLabel
from src.digraph import Digraph

class App:
    def __init__(self, g=None):
        self.graph = g
        self.f = Figure(figsize=(10,10), dpi=75)
        self.a = self.f.add_subplot(111)
        self.f.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.a.axis('off')

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 6')
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

        ttk.Button(menu, text='Page Rank a)', width=50, command=lambda: self.page_rank_a()).grid(row=4, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Page Rank b)', width=50, command=lambda: self.page_rank_b()).grid(row=6, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Metoda symulowanego wy??arzania', width=50, command=lambda: self.burn_in_method()).grid(row=8, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')
        self.draw_graph()
        self.result.show_normal(str(Digraph(from_graph=self.graph).to_adj_list()))
        self.d=0.15
        self.window.mainloop()

    def generate_digraph(self):
        n = int(self.n.get())
        p = float(self.p.get())
        if n > 0 and p >= 0.0 and p <= 1.0:

            self.graph = utils.generate_digraph(n, p).graph
            adj_list = Digraph(from_graph=self.graph).to_adj_list()
            while min(adj_list.representation.values(), key=len)==[]:
                self.graph = utils.generate_digraph(n, p).graph
                adj_list = Digraph(from_graph=self.graph).to_adj_list()
            self.result.show_normal(str(adj_list))
            self.draw_graph()
        else:
            self.result.show_normal("Bledne parametry")

    def page_rank_a(self):
        s=''
        for el in utils.page_rank_a(self.graph,self.d):
            s+=str(el[0])+" ==> "+str(el[1])+"\n"
        self.result.show_normal(s)

    def page_rank_b(self):
        s=""
        for el in utils.page_rank_b(self.graph,self.d):
            s+=str(el[0])+" ==> "+str(el[1])+"\n"
        self.result.show_normal(s)

    def burn_in_method(self):
        pass

    def draw_graph(self):
        self.a.clear()
        options = {
            'node_color': 'yellow',
            'node_size': 600,
            'width': 1,
            'arrowstyle': '-|>',
            'arrowsize': 15,
        }
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos, arrows=isinstance(self.graph, nx.DiGraph), **options, ax=self.a)
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
    g.add_vertices(range(1,13))
    for i in [(1,5),(1,6),(1,9),(2,1),(2,3),(2,6),(3,2),(3,4),(3,5),(3,12),(4,3),(4,5),(4,8),(4,9),(4,11),(5,3),(5,7),(5,8),(5,9),(6,2),(6,7),(7,5),(7,6),(7,8),(8,4),(8,7),(8,9),(8,12),(9,4),(9,5),(9,8),(9,10),(10,9),(11,4),(11,9),(12,1),(12,8)]:
        g.add_edge(i[0],i[1])

    app = App(g.graph)
