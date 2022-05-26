import tkinter as tk
from tkinter import ttk
from src import utils
from src.flow_network import FlowNetwork
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
        self.window.title('Grafy - projekt 5')
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

        ttk.Label(menu, text='N').grid(row=0, column=0)
        self.N = ttk.Entry(menu, width=10)
        self.N.grid(row=1, column=0)

        ttk.Button(menu, text='Wygeneruj losową sieć przepływową', width=50, command=lambda: self.generate_flow_network()).grid(row=2, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Znajdź maksymalny przepływ(Ford-Fulkerson)', width=50, command=lambda: self.ford_fulkerson()).grid(row=4, column=0, columnspan=3, pady=3)
        ttk.Separator(menu, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')
        
        self.window.mainloop()

    def generate_flow_network(self):
        N = int(self.N.get())

        if N >= 2:
            self.flow_network = FlowNetwork(N)
            self.graph = self.flow_network.graph
            self.draw_graph()
            self.result.show_normal(self.flow_network)
        else:
            self.result.show_normal("Błędne parametry")

    def ford_fulkerson(self):
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
        edge_labels=dict([((u,v,),f"{d['flow']}/{d['capacity']}") for u,v,d in self.graph.edges(data=True)])
        print(edge_labels)
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
    app = App()
