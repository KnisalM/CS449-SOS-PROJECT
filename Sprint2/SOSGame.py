import tkinter as tk
from tkinter import messagebox
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
        self.turnDisplayLabel = None  # Displays whose turn it currently is

    """Get and return the current player"""

    def getCurrentPlayer(self):
        return self.players[self.currentPlayer]

    """Update the GUI to reflect the turn"""

    def updateTurnFrame(self):
        currentPlayer = self.getCurrentPlayer()

        if self.turnDisplayLabel:
            self.turnDisplayLabel.destroy()

        self.turnDisplayLabel = tk.Label(self.gameFrame, text=f"It is {currentPlayer.color}'s Turn", font=('Arial', 16),
                                         fg=currentPlayer.color)
        self.turnDisplayLabel.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')

    """Switch turns so that player who is not playing can't make a move and scores are tracked appropriately"""

    def switchTurn(self):
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.updateTurnFrame()

    """get what character the player has selected for the move to be made"""

    def updatePlayerChar(self):
        self.players[0].setChar(self.p1Move.get())
        self.players[1].setChar(self.p2Move.get())

    """Define the events when an empty cell is clicked"""

    def cellClicked(self, row, col):

        self.updatePlayerChar()

        currentPlayer = self.getCurrentPlayer()
        moveChar = currentPlayer.getChar()

        self.makeAMove(row, col, moveChar, currentPlayer.color)
        self.switchTurn()

    """Execute when a valid move is made to reflect on board and update game state"""

    def makeAMove(self, row, col, moveChar, color):
        boardSize = len(self.cells)
        if boardSize <= 5:
            fontSize=14
        elif boardSize <= 8:
            fontSize = 12
        elif boardSize <= 10:
            fontSize = 10
        else:
            fontSize = 9
        fontConfig = ('Arial', fontSize, 'bold')
        self.cellState[row][col] = moveChar
        self.cells[row][col].config(text=moveChar, fg=color, state='disabled', disabledforeground=color,
                                    relief='sunken', font=fontConfig)

        # in future sprints I will add functionality here to check for SOS chain completion
        # Function will be titled checkSOSFormed(self, row, col, moveChar)

    """Begin the game and apply the logic to the game board"""

    def start_game(self):

        super().start_game()
        dimN = int(self.dimensions.get().split('x')[0])

        self.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]

        for i in range(dimN):
            for j in range(dimN):
                self.cells[i][j].config(command=lambda row=i, col=j: self.cellClicked(row, col))

        self.updatePlayerChar()

        self.updateTurnFrame()


def main():
    root = tk.Tk()
    root.title('SOS GAME')
    root.geometry('1000x800')
    root.resizable(True, True)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    SOSGame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
