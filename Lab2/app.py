import tkinter as tk
from tkinter import ttk, filedialog

class App:
    def __init__(self):
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

        ttk.Button(menu, text='Wygeneruj graf eulerowski', width=50, command=lambda: self.generate_euler()).grid(row=10, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=11, column=0, columnspan=3, sticky='EW', pady=15)

        ttk.Label(menu, text='n').grid(row=12, column=0)
        self.n = ttk.Entry(menu, width=10)
        self.n.grid(row=13, column=0)

        ttk.Label(menu, text='k').grid(row=12, column=2)
        self.k = ttk.Entry(menu, width=10)
        self.k.grid(row=13, column=2, padx=5)

        ttk.Button(menu, text='Wygeneruj graf k-regularny', width=50, command=lambda: self.generate_k_regular()).grid(row=14, column=0, pady=3, columnspan=3)
        ttk.Separator(menu, orient='horizontal').grid(row=15, column=0, columnspan=3, sticky='EW', pady=15)
        
        ttk.Button(menu, text='Wczytaj graf', width=50, command=lambda: self.load_graph()).grid(row=16, column=0, pady=3, columnspan=3)
        ttk.Button(menu, text='Znajdź cykl hamiltonowski', width=50, command=lambda: self.find_hamiltonian_cycle()).grid(row=17, column=0, pady=3, columnspan=3)

        self.window.mainloop()

    def check_sequence(self):
        pass

    def randomize_graph(self):
        pass

    def show_connected_components(self):
        pass

    def generate_euler(self):
        pass

    def generate_k_regular(self):
        pass

    def load_graph(self):
        pass

    def find_hamiltonian_cycle(self):
        pass


if __name__ == '__main__':
    app = App()
