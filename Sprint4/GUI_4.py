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


class GameBoard:
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
        self.turn_display_label = None

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
        rule_label.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))

        ttk.Radiobutton(self.setup_frame, text='Simple, first SOS wins!', variable=self.config.rule_set,
                        value='Simple').grid(row=2, column=1, sticy=tk.W, pady=2, padx=(10, 0))
        ttk.Radiobutton(self.setup_frame, text='General, most SOS chains wins!', variable=self.config.rule_set,
                        value='General').grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10, 0))

    def player_type_radio_buttons(self):
        """Setup player type selection widgets"""
        player_type = tk.Label(self.setup_frame, text='Choose opponent type')
        player_type.grid(row=4, column=0, sticky=tk.W, pady=5)

        ttk.Radiobutton(self.setup_frame, text='Human vs Human', variable=self.config.game_type, value='Human'
                        ).grid(row=4, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Radiobutton(self.setup_frame, text='Human vs Computer', variable=self.config.game_type, value='Computer'
                        ).grid(row=4, column=2, sticky=tk.W, pady=2, padx=(10, 0))

    def start_conditions(self):
        """Check if game can be started, show begin button if ready to start"""
        if self.config.config_complete():
            begin_label = tk.Label(self.setup_frame, text=f"You've chose to play a {self.config.rule_set.get()} game "
                                                          f"on a {self.config.dimensions.get()} sized board, against a"
                                                          f"{self.config.game_type.get()}, begin?")

            begin_label.grid(row=6, column=0, sticky=tk.W, pady=5)

            start_game = tk.Button(self.setup_frame, text='Begin', command=self.start_game)
            start_game.grid(row=6, column=1, sticky=tk.W, pady=5)

    def create_gameboard_ui(self):
        """Create the UI for the gameboard in this function, common functionality for both classes"""
        # clear setup frame and setup game frame
        self.setup_frame.destroy()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.game_frame.grid(row=0, column=0, sticky='nsew')
        self.game_frame.grid_rowconfigure(1, weight=1)
        self.game_frame.grid_columnconfigure(0, weight=0)  # Left player frame
        self.game_frame.grid_columnconfigure(1, weight=1)  # Board frame - expands
        self.game_frame.grid_columnconfigure(2, weight=0)  # Right player frame

        dimension = int(self.config.dimensions.get().split('x')[0])

        # Create the board frame that will contain the cells
        board_frame = tk.Frame(self.game_frame)
        board_frame.grid(row=1, column=1, sticky='nsew')

        # Create the grid of cells
        self.cells = []
        for i in range(dimension):
            row_cells = []
            for j in range(dimension):
                # Create each cell as a button
                cell_button = tk.Button(
                    board_frame,
                    text='',
                    width=4,
                    height=2,
                    font=('Arial', 12, 'bold')
                )
                cell_button.grid(row=i, column=j, sticky='nswe')
                row_cells.append(cell_button)

                # Configure grid weights for proper scaling
                board_frame.grid_rowconfigure(i, weight=1)
                board_frame.grid_columnconfigure(j, weight=1)

            self.cells.append(row_cells)

        # Create player frames using the factory
        if self.config.game_type.get() == 'Human':
            create_player_frame(
                self.game_frame, 1, 0, 'Red Player', self.config.p1_move)
            create_player_frame(
                self.game_frame, 1, 2, 'Blue Player', self.config.p2_move)
        else:
            create_player_frame(
                self.game_frame, 1, 0, 'Human Player', self.config.p1_move)
            create_player_frame(
                self.game_frame, 1, 2, 'Computer Player', self.config.p2_move)

    def update_cell_appearance(self, row, col, character, color):
        """Update the visual appearance of a cell """
        board_size = len(self.cells)
        font_config = self.get_font_config(board_size)

        self.cells[row][col].config(
            text=character,
            fg=color,
            state='disabled',
            disabledforeground=color,
            relief='sunken',
            font=font_config
        )

    def draw_sos_chain(self, cell_locations, player_color):
        """Highlight an SOS chain on the board """
        for row, col in cell_locations:
            self.cells[row][col].config(
                disabledforeground='white',
                fg='white',
                bg=player_color
            )

    def update_turn_display(self, player_text, player_color):
        """Update the turn display label """
        if self.turn_display_label:
            self.turn_display_label.destroy()

        self.turn_display_label = tk.Label(
            self.game_frame,
            text=f"It is the {player_text}",
            font=('Arial', 16),
            fg=player_color
        )
        self.turn_display_label.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')

    def disable_all_cells(self):
        """Disable all cells when game ends"""
        for row in self.cells:
            for cell in row:
                cell.config(state='disabled')

    def set_cell_click_handler(self, row, col, handler):
        """Set click handler for a cell - game logic provides the handler"""
        self.cells[row][col].config(command=lambda: handler(row, col))

    def get_font_config(self, board_size):
        """Helper method to determine appropriate font size based on board dimensions"""
        if board_size <= 5:
            return 'Arial', 14, 'bold'
        elif board_size <= 8:
            return 'Arial', 12, 'bold'
        elif board_size <= 10:
            return 'Arial', 10, 'bold'
        else:
            return 'Arial', 9, 'bold'

    def start_game(self):
        """Template method to be implemented by subclasses"""
        pass


class SetupGame(GameBoard):
    """Handles game setup and initialization"""

    def __init__(self, root):
        super().__init__(root)
        self.game_instance = None

    def start_game(self):
        """Start the game with selected configuration"""
        # Create the game board UI first
        self.create_gameboard_ui()

        # Import locally to avoid circular imports
        from SOSGame_4 import SimpleSOSGame, GeneralSOSGame

        # Create appropriate game instance based on rule set
        if self.config.rule_set.get() == 'Simple':
            self.game_instance = SimpleSOSGame(self.root, self.config, self)
        else:
            self.game_instance = GeneralSOSGame(self.root, self.config, self)

        # Start the game logic
        self.game_instance.start_game()
