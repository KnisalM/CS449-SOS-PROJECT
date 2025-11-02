import tkinter as tk
from tkinter import ttk
import pylint
import unittest

"""This is a helper function designed in assistance with Deepseek LLM to reduce doubling up on code in the 
    player frame creation process
    
    Preconditions: Parent is a valid frame, row and column are valid unoccupied placements in the grid manager for the Parent window,
    player is a valid String, and moveChar is a variable assigned to one of the players on the board
    
    Post conditions: A sub-Frame will be created and placed within the parent Frame. This frame will have the player label
    at the top, and will have two radio buttons with options 'S' and 'O' """


def createPlayerFrame(parent, row, column, player, moveChar):
    frame = tk.Frame(parent, width=150)
    frame.grid(row=row, column=column, sticky='nsew')
    frame.grid_propagate(False)

    tk.Label(frame, text=player, font=('Arial', 12)).grid(row=0, column=0, columnspan=2, pady=(0, 10))
    ttk.Radiobutton(frame, text='S', variable=moveChar, value='S').grid(row=1, column=0, sticky=tk.W, pady=2)
    ttk.Radiobutton(frame, text='O', variable=moveChar, value='O').grid(row=2, column=0, sticky=tk.W, pady=2)

    return frame


class gameBoard:
    def __init__(self, root):

        # Define parent window that application runs in
        self.root = root
        self.root.title("SOS Game")

        # Variables that the board will utilize for setup and play
        self.dimensions = tk.StringVar(
            value='')  # store the player's selection for the dimensions of the board
        self.ruleSet = tk.StringVar(
            value='')  # store whether the player has selected to play a Simple or General game mode
        self.p2Move = tk.StringVar(value='S')  # Is p2 making an 'S' or 'O' move
        self.p1Move = tk.StringVar(value='S')  # is p1 making an 'S' or 'O' move

        # Create Frames that setup and main game will run in
        self.setupFrame = tk.Frame(
            self.root)  # This creates the setup Frame where the player is asked to set up their board, ties it to the parent window self.root
        self.gameFrame = tk.Frame(
            self.root)  # Creates Frame where the game will take place, ties to parent window self.root

        # Create list to hold the cells of the game board and a list to hold moves that have been made
        self.cells = []  # Store the cells of the game board

        # Game logic controller variable
        self.gameLogic = None

        self.boardSize()
        self.ruleSetSelection()

    """This function creates the setup widgets for the game board, allowing the user to select their game board Size, 
    their Rule Set, and in future Sprints will include the player choosing between playing against another human, or 
    playing versus an algorithm"""

    def boardSize(self):
        # Load the setup frame into the grid manager
        self.setupFrame.grid(row=0, column=0, sticky='nsew')

        # Title Widget
        titleLabel = tk.Label(self.setupFrame, text='Setup Your Game!', font=('Arial', 16, 'bold'))
        titleLabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Board Size selection Widgets
        sizeLabel = tk.Label(self.setupFrame, text='Choose the size of your game board from the dropdown menu.')
        sizeLabel.grid(row=1, column=0, sticky=tk.W, pady=5)
        sizes = [f"{i}x{i}" for i in range(3, 13)]
        sizeDropdown = ttk.Combobox(self.setupFrame, textvariable=self.dimensions, values=sizes, state='readonly',
                                    width=10)
        sizeDropdown.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

    def ruleSetSelection(self):
        # Rule Set selection Widgets
        rulesLabel = tk.Label(self.setupFrame, text='Choose the rules that you will play by.')
        rulesLabel.grid(row=2, column=0, sticky=tk.W, pady=5)
        simpleRB = ttk.Radiobutton(self.setupFrame, text="Simple, First SOS Wins!",
                                   variable=self.ruleSet, value="simple")
        generalRB = ttk.Radiobutton(self.setupFrame, text="General, Most SOS Wins!",
                                    variable=self.ruleSet, value="general")
        simpleRB.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        generalRB.grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10, 0))

        # Track the state of the game conditions, dimensions and ruleSet, display begin button when conditions are satisfied
        self.dimensions.trace('w', self.startConditions)
        self.ruleSet.trace('w', self.startConditions)

    """This function determines when the conditions dimensions and ruleSet have been chosen, and allows the user to 
    select a 'Begin' button that will create the game board with their chosen conditions
    
    Preconditions: Player has opened the application and is in the process of choosing how they would like to play 
     the game
     
    Post conditions: The player will see a button displayed that says 'Begin', that will initialize the game board when pressed """

    def startConditions(self, *args):
        # Check if the player has selected their game board dimensions and ruleSet yet, create and display Begin button
        if self.dimensions.get() and self.ruleSet.get():
            beginLabel = tk.Label(self.setupFrame,
                                  text=f"You've chosen to play a {self.ruleSet.get()} game on a {self.dimensions.get()} sized board, begin?")
            beginLabel.grid(row=5, column=0, sticky=tk.W, pady=5)
            startGame = tk.Button(self.setupFrame, text='Begin', command=self.startGame)
            startGame.grid(row=5, column=1, sticky=tk.W, pady=5)

    """This Function Initializes the game board
    
    Preconditions: The player has selected a valid dimension, ruleSet, and has selected the 'Begin' button
    
    Post conditions: The player will be presented with a game board of their selected dimensions and ruleSet, with a
    grid of selectable buttons in their chosen dimension"""

    def startGame(self):

        self.setupFrame.destroy()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.gameFrame.grid(row=0, column=0, sticky='nsew')
        self.gameFrame.grid_rowconfigure(1, weight=1)
        self.gameFrame.grid_columnconfigure(0, weight=0)  # Left p1Frame, do not expand at all
        self.gameFrame.grid_columnconfigure(1, weight=1)  # Board Frame, expand to fill
        self.gameFrame.grid_columnconfigure(2, weight=0)  # p2Frame, do not expand

        dimN = int(self.dimensions.get().split('x')[0])

        boardFrame = tk.Frame(self.gameFrame)
        boardFrame.grid(row=1, column=1, sticky='nsew')

        for i in range(dimN):
            row = []
            for j in range(dimN):
                button = tk.Button(boardFrame, text='', width=4, height=2)
                button.grid(row=i, column=j, sticky='nswe')
                row.append(button)
            self.cells.append(row)

            # Configure grid properly to scale with window
            boardFrame.grid_rowconfigure(i, weight=1)
            boardFrame.grid_columnconfigure(i, weight=1)

        # Create Player Frames
        createPlayerFrame(self.gameFrame, 1, 0, 'Red Player', self.p1Move)
        createPlayerFrame(self.gameFrame, 1, 2, 'Blue Player', self.p2Move)

        # Initialize the game logic to the board based on rule selection
        if self.ruleSet.get() == 'simple':
            self.gameLogic =

    def drawSOSChain(self, cellLocations, pColor):
        """This function will be the helper function that will create the drawn line
        on the game board when a player creates a valid SOS chain"""

        for row, col in cellLocations:
            self.cells[row][col].config(fg='white', bg=pColor)

