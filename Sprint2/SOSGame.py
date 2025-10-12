import tkinter
from GUI_2 import gameBoard


class Player:
    """This class represents the player's of the game, and their related data"""

    def __init__(self, player_number,
                 player_type="human"):  # Later sprints will implement that this can be a computer player
        self.player_number = player_number  # Tracks if this is player 1 or 2
        self.player_type = player_type  # Will come into use later when implementing a human or computer opponent
        self.score = 0  # score for all player's must begin at 0
        self.character = 'S'  # S character selected by default, but at time of event will be updated to selected character
        self.color = 'red' if player_number == 1 else 'blue'  # Color of character's placed on board
        self.name = f"Player {player_number}"  # Determines Player Name for displaying on the board whose turn it is

    """This function will set the character for the player to play based on their selection in the frame"""

    def setChar(self, character):
        if character in ['S', 'O']:
            self.character = character

    """Get the current selected character"""

    def getChar(self):
        return self.character

    """Increment Player's score in a general game when they create a SOS chain"""

    def incrementScore(self):
        self.score += 1


class SOSGame(gameBoard):
    """This class will extend the class gameBoard from GUI_2.py, and will begin implementing the actual game logic onto the board"""

    def __init__(self, root):
        super().__init__(root)

        self.players = [Player(1, 'human'),  # Player 1 Red
                        Player(2, 'human')]  # Player 2 Blue
        self.currentPlayer = 0  # Start with Player 1
        self.activeGame = True
        self.cellState = []

     """Get and return the current player"""
    def getCurrentPlayer(self):
        return self.players[self.currentPlayer]

    """Switch turns so that player who is not playing can't make a move and scores are tracked appropriately"""


