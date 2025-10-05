import tkinter as tk
import pylint
import unittest


class gameBoard():
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.dimensions = tk.IntVar(value='')  # The variable that will store the player's selection for the dimensions of the board
        self.ruleSet = tk.StringVar(value='')  # This variable will store whether the player has selected to play a
        self.setupFrame = tk.Frame(self.root, padding=20) # This assigns the properties for the setup Frame where the player is asked to set up their board, including the parent window being self.root
        self.setupFrameGrid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # This implements the grid manager for the Frame setupFrame, including the sticky constants which will allow the assignment of widgets in the Frame by directional commands
        # self.opponentType = '' Will Implement later, this will store the player's selection for Human v Human or Human v Machine
        # self.currentTurn = '' Will Implement later, this will store which player's turn it currently is for the moves placed on the board
        # self.active = '' Implement in later sprint, will track game state and update when game is over
        self.cells = [] # Store the cells of the game board
        # self.cellsState = [] Implement in later Sprint, will track the state of the cells and prevent further moves from being played on them once played

        def boardSetup(self):
            titleLabel = tk.Label(self.setupFrame, text='Setup Your Game!', font=('Arial', 16, 'bold'))
            titleLabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))

            sizeLabel = tk.Label(self.setupFrame, text='Choose the size of your game board from the dropdown menu.')
            sizeLabel.grid(row=1, column=0, sticky=tk.W, pady=5)

