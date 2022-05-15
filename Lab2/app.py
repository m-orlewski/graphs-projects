import tkinter as tk
from tkinter import ttk, filedialog
# from tools.draw import draw_graph

from src import utils

import tools.draw
from tools.tkinter import InfoLabel

class App:
    def __init__(self):
        self.graph = None

        self.window = tk.Tk()
        self.window.title('Grafy - projekt 2')
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


        ttk.Label(menu, text='Podaj ciąg graficzny:').grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.sequence = ttk.Entry(menu, width=50)
        self.sequence.grid(row=1, column=0, columnspan=3, pady=3)
        ttk.Button(menu, text='Sprawdź sekwencję', width=50, command=lambda: self.check_sequence()).grid(row=2, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Label(menu, text='Podaj ilość randomizacji:').grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.randomize_count = ttk.Entry(menu, width=50)
        self.randomize_count.grid(row=5, column=0, columnspan=3, pady=3)
        ttk.Button(menu, text='Randomizuj', width=50, command=lambda: self.randomize_graph()).grid(row=6, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Button(menu, text='Pokaż spójne składowe', width=50, command=lambda: self.show_connected_components()).grid(row=8, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Label(menu, text='n').grid(row=10, column=0)
        self.n1 = ttk.Entry(menu, width=10)
        self.n1.grid(row=11, column=0)
        ttk.Button(menu, text='Wygeneruj graf eulerowski', width=50, command=lambda: self.generate_euler()).grid(row=12, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=13, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Label(menu, text='n').grid(row=14, column=0)
        self.n2 = ttk.Entry(menu, width=10)
        self.n2.grid(row=15, column=0)

        ttk.Label(menu, text='k').grid(row=14, column=2)
        self.k = ttk.Entry(menu, width=10)
        self.k.grid(row=15, column=2, padx=5)

        ttk.Button(menu, text='Wygeneruj graf k-regularny', width=50, command=lambda: self.generate_k_regular()).grid(row=16, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=17, column=0, columnspan=3, sticky='EW', pady=15)
        
        ttk.Button(menu, text='Znajdź cykl hamiltonowski', width=50, command=lambda: self.find_hamiltonian_cycle()).grid(row=18, column=0, pady=3, columnspan=3)

        ttk.Separator(self.window, orient='vertical').grid(row=0, column=1, pady=5, sticky='NS')
        ttk.Separator(self.window, orient='vertical').grid(row=0, column=3, pady=5, sticky='NS')

        self.window.mainloop()

    def check_sequence(self):
        l = []
        for c in self.sequence.get():
            if c not in '0123456789':
                return False
            else:
                l.append(int(c))

        if utils.check_sequence(l.copy()):
            self.graph = utils.create_graph_from_sequence(l.copy())
            self.draw_graph()
            self.print_graph("Sekwencja jest ciągiem graficznym\n")
            return True
        else:
            self.result.show_normal("Ciąg nie jest graficzny!")
            self.canvas.delete("all")
            return False


    def randomize_graph(self):
        if not self.check_sequence():
            self.result.show_normal("Ciąg nie jest graficzny!")
            return False

        count = int(self.randomize_count.get())
        self.graph = utils.randomize_graph(self.graph, count)
        self.draw_graph()
        self.print_graph()
        

    def show_connected_components(self):
        if self.graph:
            self.components = utils.components(self.graph)

            comp = {}
            for key, value in self.components.items():
                if value not in comp.keys():
                    comp[value] = [key]
                else:
                    comp[value].append(key)

            longest_comp = []
            for value in comp.values():
                if len(value) > len(longest_comp):
                    longest_comp = value

            tools.draw.draw_graph_with_components(self.canvas, utils.nx_graph_to_representation(self.graph), longest_comp)
            


    def generate_euler(self):
        self.graph = utils.generate_random_euler_graph(int(self.n1.get()))
        cycle = utils.find_euler_cycle(self.graph)
        self.draw_graph()
        self.result.show_normal(f"Cykl Eulera: {cycle}")

    def generate_k_regular(self):
        self.graph = utils.generate_random_k_regular(int(self.k.get()), int(self.n2.get()))
        if self.graph is None:
            self.result.show_normal("Blad generowania!")
            self.canvas.delete("all")
        self.draw_graph()
        self.print_graph()


    def find_hamiltonian_cycle(self):
        (isHamilton, cycle) = utils.isHamilton(self.graph)
        if isHamilton:
            self.print_graph(f"Znaleziony cykl:\n{cycle}\n\n")
        else:
            self.result.show_normal("Nie znaleziono cyklu")

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

    def print_graph(self, comment=""):
        if self.graph is not None:
            result = comment
            for vertex, neighbors in utils.nx_graph_to_representation(self.graph).items():
                result += str(vertex) + ': '
                result += ', '.join(map(str, neighbors))
                result += '\n'
            self.result.show_normal(result)
    
    def draw_graph(self):
        if self.graph is not None:
            tools.draw.draw_graph(self.canvas, utils.nx_graph_to_representation(self.graph))

if __name__ == '__main__':
    app = App()
