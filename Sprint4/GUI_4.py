import tkinter as tk
from tkinter import ttk
import pylint
import unittest


def create_player_frame(parent, row, column, player, move_char):
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
    ttk.Radiobutton(frame, text='S', variable=move_char, value='S').grid(row=1, column=0, sticky=tk.W, pady=2)
    ttk.Radiobutton(frame, text='O', variable=move_char, value='O').grid(row=2, column=0, sticky=tk.W, pady=2)

    return frame


class GameConfig:
    """This class improves the encapsulation of game configuration data, and the cohesion of the data and related methods
    """

    def __init__(self):
        self.dimensions = tk.StringVar(value='')
        self.rule_set = tk.StringVar(value='')
        self.p1_move = tk.StringVar(value='S')
        self.p2_move = tk.StringVar(value='S')
        self.game_type = tk.StringVar(value='Human')

    def config_complete(self):
        """Check if all configuration options are selected"""
        return all([self.dimensions.get(), self.rule_set.get(), self.game_type.get()])


class gameBoard:
    def __init__(self, root):

        # Define parent window that application runs in
        self.root = root
        self.root.title("SOS Game")

        self.config = GameConfig()

        # Create Frames that setup and main game will run in
        self.setup_frame = tk.Frame(
            self.root)  # This creates the setup Frame where the player is asked to set up their board, ties it to the parent window self.root
        self.game_frame = tk.Frame(
            self.root)  # Creates Frame where the game will take place, ties to parent window self.root

        # Create list to hold the cells of the game board and a list to hold moves that have been made
        self.cells = []  # Store the cells of the game board

        self.setup_ui_components()


    def setup_ui_components(self):
        """Setup the UI components without making any changes to game logic, separates UI and Game Logic"""
        self.board_size_dropdown()
        self.rule_set_radio_buttons()
        self.player_type_radio_buttons()

        # Track configuration types
        self.config.dimensions.trace('w', self.start_conditions)
        self.config.rule_set.trace('w', self.start_conditions)
        self.config.game_type.trace('w', self.start_conditions)

    def board_size_dropdown(self):
        """Setup the dropdown menu for the game board size selection"""
        self.setup_frame.grid(row=0, column=0, sticky='nsew')

        title_label = tk.Label(self.setup_frame, text='Setup Your Game!', font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        size_label = tk.Label(self.setup_frame, text='Choose the size of your game board from the dropdown menu')
        size_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        sizes = [f"{i}x{i}" for i in range(3, 13)]
        ttk.Combobox(self.setup_frame, textvariable=self.config.dimensions, values=sizes,
                     state='readonly', width=10).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

    def rule_set_radio_buttons(self):
        """Setup rule set selection UI widgets"""
        rule_label = tk.Label(self.setup_frame, text='Choose the rule set you will use')
        rule_label.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10,0))

        ttk.Radiobutton(self.setup_frame, text='Simple, first SOS wins!', variable=self.config.rule_set,
                        value='Simple').grid(row=2, column=1, sticy=tk.W, pady=2, padx=(10,0))
        ttk.Radiobutton(self.setup_frame, text='General, most SOS chains wins!', variable=self.config.rule_set,
                        value='General').grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10,0))

    def player_type_radio_buttons(self):
        """Setup player type selection widgets"""
        player_type = tk.Label(self.setup_frame, text='Choose opponent type')
        player_type.grid(row=4, column=0, sticky=tk.W, pady=5)

        ttk.Radiobutton(self.setup_frame, text='Human vs Human', variable=self.config.game_type, value='Human'
                        ).grid(row=4, column=1, sticky=tk.W, pady=2, padx=(10,0))
        ttk.Radiobutton(self.setup_frame, text='Human vs Computer', variable=self.config.game_type, value='Computer'
                        ).grid(row=4, column=2, sticky=tk.W, pady=2, padx=(10,0))

    def start_conditions(self):
        """Check if game can be started, show begin button if ready to start"""
        if self.config.config_complete():
            begin_label = tk.Label(self.setup_frame, text=f"You've chose to play a {self.config.rule_set.get()} game "
                                                          f"on a {self.config.dimensions.get()} sized board, against a"
                                                          f"{self.config.game_type.get()}, begin?")

            begin_label.grid(row=6, column=0, sticky=tk.W, pady=5)

            start_game = tk.Button(self.setup_frame, text='Begin', command=self.start_game)
            start_game.grid(row=6, column=1, sticky=tk.W, pady=5)





    def startGame(self):
        """Template method that will be implemented by subclasses in SOSGame_4.py file
"""

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
        gameType = self.gameType.get()

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
        gameInstance.gameType.set(gameType)
        gameInstance.p1Move.set(p1MoveVal)
        gameInstance.p2Move.set(p2MoveVal)

        self.instance = gameInstance
        gameInstance.startGame()
