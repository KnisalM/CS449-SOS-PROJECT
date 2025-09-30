import tkinter as tk
import pylint
import unittest


class GameSetup:
    def __init__(self, root):
        self.root.title("Game Setup")  # Title of window
        self.root.geometry("1000x800)")  # Size of window
        self.gameplay_mode = tk.StringVar(value="")  # Variable to store the selected gameplay mode
        self.board_size = tk.StringVar()  # Variable to store the board size input by the player, which will be converted to an INT
        self.create_widgets()  # This function will create and place the widgets in the beginning screen

    def create_widgets(self):
