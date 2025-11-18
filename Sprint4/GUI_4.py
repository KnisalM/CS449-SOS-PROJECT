import tkinter as tk
from tkinter import ttk
import pylint
import unittest


def createPlayerFrame(parent, row, column, player, moveChar):
    """This is a helper function designed in assistance with Deepseek LLM to reduce doubling up on code in the
    player frame creation process

    Preconditions: Parent is a valid frame, row and column are valid unoccupied placements in the grid manager for the Parent window,
    player is a valid String, and moveChar is a variable assigned to one of the players on the board

    Post conditions: A sub-Frame will be created and placed within the parent Frame. This frame will have the player label
    at the top, and will have two radio buttons with options 'S' and 'O' """
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
        self.p1_type = tk.StringVar(value='Human')  # GUI tracking instance variable for Red Player Human or Computer
        self.p2_type = tk.StringVar(value='Human')  # GUI tracking instance variable for Red Player Human or Computer

        # Create Frames that setup and main game will run in
        self.setupFrame = tk.Frame(
            self.root)  # This creates the setup Frame where the player is asked to set up their board, ties it to the parent window self.root
        self.turnDisplayLabel = None  # Displays whose turn it currently is
        self.gameFrame = tk.Frame(
            self.root)  # Creates Frame where the game will take place, ties to parent window self.root

        # Create list to hold the cells of the game board and a list to hold moves that have been made
        self.cells = []  # Store the cells of the game board

        self.boardSize()
        self.ruleSetSelection()
        self.playerTypeSelection()

    def boardSize(self):
        """This function creates the setup widgets for the game board, allowing the user to select their game board Size,
    their Rule Set, and in future Sprints will include the player choosing between playing against another human, or
    playing versus an algorithm"""
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

    def playerTypeSelection(self):
        """This function will implement the selection of the player opponent type
        with either red or blue player being human or computer"""

        player_label = tk.Label(self.setupFrame, text='Choose Player Types', font=('Arial', 12, 'bold'))
        player_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 15))

        # Red Player Type Selection
        red_player_label = tk.Label(self.setupFrame, text='Red Player Type')
        red_player_label.grid(row=6, column=1, sticky=tk.W, pady=5)

        red_human_RB = ttk.Radiobutton(self.setupFrame, text='Human', variable=self.p1_type, value='Human')
        red_computer_RB = ttk.Radiobutton(self.setupFrame, text='Computer', variable=self.p1_type, value='Computer')

        red_human_RB.grid(row=7, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        red_computer_RB.grid(row=8, column=1, sticky=tk.W, pady=2, padx=(10, 0))

        # Blue Player Type Selection
        blue_player_label = tk.Label(self.setupFrame, text='Blue Player Type')
        blue_player_label.grid(row=6, column=2, sticky=tk.W, pady=5)

        blue_human_RB = ttk.Radiobutton(self.setupFrame, text='Human', variable=self.p2_type, value='Human')
        blue_computer_RB = ttk.Radiobutton(self.setupFrame, text='Computer', variable=self.p2_type, value='Computer')

        blue_human_RB.grid(row=7, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        blue_computer_RB.grid(row=8, column=2, sticky=tk.W, pady=2, padx=(10, 0))

        # Add a Trace to the function so that when the conditions are met
        self.dimensions.trace('w', self.startConditions)
        self.ruleSet.trace('w', self.startConditions)
        self.p1_type.trace('w', self.startConditions)
        self.p2_type.trace('w', self.startConditions)

    def startConditions(self, *args):
        """This function determines when the conditions dimensions and ruleSet have been chosen, and allows the user to
    select a 'Begin' button that will create the game board with their chosen conditions

    Preconditions: Player has opened the application and is in the process of choosing how they would like to play
     the game

    Post conditions: The player will see a button displayed that says 'Begin', that will initialize the game board when pressed """
        # Check if the player has selected their game board dimensions and ruleSet yet, create and display Begin button
        if self.dimensions.get() and self.ruleSet.get() and self.p1_type.get() and self.p2_type.get():
            beginLabel = tk.Label(self.setupFrame,
                                  text=f"You've chosen to play a {self.ruleSet.get()} game on a {self.dimensions.get()} "
                                       f"sized board, with Red Played by a {self.p1_type.get()}, and Blue Played by a"
                                       f" {self.p2_type.get()}, begin?")
            beginLabel.grid(row=10, column=0, sticky=tk.W, pady=5)
            startGame = tk.Button(self.setupFrame, text='Begin', command=self.startGame)
            startGame.grid(row=10, column=1, sticky=tk.W, pady=5)

    def createUIElements(self):
        """This Function Initializes the game board

    Preconditions: The player has selected a valid dimension, ruleSet, and has selected the 'Begin' button

    Post conditions: The player will be presented with a game board of their selected dimensions and ruleSet, with a
    grid of selectable buttons in their chosen dimension"""

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
                button.grid(row=i, column=j, sticky=tk.NSEW)
                row.append(button)
            self.cells.append(row)

            # Configure grid properly to scale with window
            boardFrame.grid_rowconfigure(i, weight=1)
            boardFrame.grid_columnconfigure(i, weight=1)

        # Create Player Frames
        createPlayerFrame(self.gameFrame, 1, 0, 'Red Player', self.p1Move)
        createPlayerFrame(self.gameFrame, 1, 2, 'Blue Player', self.p1Move)

    def startGame(self):
        """Template method that will be implemented by subclasses in SOSGame_4.py file
"""

    def updateTurnFrame(self, current_player):
        if self.turnDisplayLabel:
            self.turnDisplayLabel.destroy()

        self.turnDisplayLabel = tk.Label(self.gameFrame, text=f"It is the {current_player.color} Player's turn",
                                         font=('Arial', 16), fg=current_player.color)
        self.turnDisplayLabel.grid(row=3, column=0, columnspan=3, pady=10, sticky=tk.EW)


    def drawSOSChain(self, cellLocations, pColor):
        """This function will be the helper function that will create the drawn line
        on the game board when a player creates a valid SOS chain"""

        for row, col in cellLocations:
            self.cells[row][col].config(disabledforeground='white', fg='white', bg=pColor)


class setupGame(gameBoard):

    def __init__(self, root):
        super().__init__(root)
        self.instance = None

    def startGame(self):
        """Override startGame to create appropriate game instance based on rules"""
        ruleSet = self.ruleSet.get()
        dimensions = self.dimensions.get()

        # Store the move values
        p1MoveVal = self.p1Move.get()
        p2MoveVal = self.p2Move.get()

        # Destroy setup frame
        self.setupFrame.destroy()

        # Import game classes locally to avoid any import issues
        from SOSGame_4 import simpleSOSGame, generalSOSGame

        # Create appropriate game instance based on the selected rule set
        if ruleSet == 'simple':
            gameInstance = simpleSOSGame(self.root)
        else:  # Covers general condition
            gameInstance = generalSOSGame(self.root)

        # Pass variables to game instance
        gameInstance.dimensions.set(dimensions)
        gameInstance.ruleSet.set(ruleSet)
        gameInstance.p1Move.set(p1MoveVal)
        gameInstance.p2Move.set(p2MoveVal)

        self.instance = gameInstance
        gameInstance.startGame()
