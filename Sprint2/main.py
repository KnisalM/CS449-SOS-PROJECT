import tkinter as tk
import pylint
import unittest


class GameSetup:
    def __init__(self,root):
        self.root.title("Game Setup")
        self.root.geometry("1000x800)")
        self.gameplay_mode = tk.StringVar(value="")
        self.board_size = tk.StringVar()
        self.create_widgets()


