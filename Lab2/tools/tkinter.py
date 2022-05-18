import tkinter as tk
from tkinter import ttk

class InfoLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def show_normal(self, text):
        super().grid()
        self['text'] = text
        self['foreground'] = 'black'

    def grid_quietly(self, row, column):
        super().grid(row=row, column=column)
        super().grid_remove()

    def hide(self):
        super().grid_remove()

    def show(self):
        super().grid()

    def clear(self):
        self['text'] = ''

    def append(self, text):
        self['text'] += text