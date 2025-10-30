import tkinter as tk
from tkinter import messagebox
from GUI_3 import gameBoard


class Player:
    """This class represents the player's of the game, and their related data"""

    def __init__(self, player_number,
                 player_type="human"):  # Later sprints will implement that this can be a computer player
        self.player_number = player_number  # Tracks if this is player 1 or 2
        self.player_type = player_type  # Will come into use later when implementing a human or computer opponent
        self.score = 0  # score for all player's must begin at 0
        self.character = 'S'  # S character selected by default, but at time of event will be updated to selected character
        self.color = 'Red' if player_number == 1 else 'Blue'  # Color of character's placed on board
        self.name = f"Player {player_number}"  # Determines Player Name for displaying on the board whose turn it is

    """This function will set the character for the player to play based on their selection in the frame"""

    def setChar(self, character):
        if character in ['S', 'O']:
            self.character = character

    """Get the current selected character"""

    def getChar(self):
        return self.character

    def incrementScore(self):
        """This function will increment the player's score when they create a valid SOS
         The simple game will utilize this function to end the game when a player's score
         != 0, and will track the player's score in a general game until there are no moves left"""
        self.score += 1


class computerPlayer(Player):
    """this class will extend the Player class to a computer player's logic. This class will
    implement the logic for a computer player to choose how it makes decisions on move placement,
    blocking the other player from making an SOS, and making moves to lay out a path to create
    an SOS ahead of time"""


class SOSGame(gameBoard):
    """This class will extend the class gameBoard from GUI_2.py, and will begin implementing the actual game logic onto the board"""

    def __init__(self, root):
        super().__init__(root)

        self.players = [Player(1, 'human'),  # Player 1 Red
                        Player(2, 'human')]  # Player 2 Blue
        self.currentPlayer = 0  # Start with Player 1
        self.activeGame = True
        self.cellState = []  # Track the state of the cells and whether there is currently a play made on a cell
        self.turnDisplayLabel = None  # Displays whose turn it currently is
        self.versusType = ''

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
        if not self.activeGame or self.cellState[row][col] != '':
            return

        self.updatePlayerChar()

        currentPlayer = self.getCurrentPlayer()
        moveChar = currentPlayer.getChar()

        self.makeAMove(row, col, moveChar, currentPlayer.color)
        self.switchTurn()

    """Execute when a valid move is made to reflect on board and update game state
    Commonly Used Functionality between both general and simple SOSGame subclasses"""

    def makeAMove(self, row, col, moveChar, color):
        boardSize = len(self.cells)
        if boardSize <= 5:
            fontSize = 14
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

        # Check for a SOS chain after the move by calling checkSOSFormed function
        self.checkSOSFormed(row, col, moveChar)

        self.gameOverHandler()

    def checkSOSFormed(self, row, col, player):
        """This function will check if an SOS has been formed after each move. If a player has created an SOS, then their
        score will be incremented. A simple game will utilize this to tell a game is over when one of the player's score
        is !=0, and a general game will use this to increment the player's score and track who wins by who has the most
        SOS made when there are no moves left"""
        sosChains = []
        boardDim = len(self.cellState)

        # Define the 4 directions to check in, their opposites are handled by checking in both directions
        directionsToCheck = [
            (0, 1), (1, 0), (1, 1), (1, -1)
        ]  # Vertical 1 up, Horizontal 1 to the right, Up Right, Down Right, opposites will be checked

        for directionOne, directionTwo in directionsToCheck:
            # Create a negative factor to multiply by so we can check in opposite directions
            for directionalFactor in [1, -1]:
                actualDirectionOne, actualDirectionTwo = directionOne * directionalFactor, directionTwo * directionalFactor

                # Calculate what the positions are for the 3 positions that would form an SOS in this direction
                positions = []
                validPositions = True

                for i in range(3):
                    r = row + (i * actualDirectionOne)
                    c = col + (i * actualDirectionTwo)

                    if 0 <= r < boardDim and 0 <= c < boardDim:
                        positions.append((r, c))
                    else:
                        validPositions = False
                        break

                # If there are 3 valid positions in the list, check if they form an SOS
                if validPositions and len(positions) == 3:
                    cell1 = self.cellState[positions[0][0]][positions[0][1]]
                    cell2 = self.cellState[positions[1][0]][positions[1][1]]
                    cell3 = self.cellState[positions[2][0]][positions[2][1]]

                    if cell1 == 'S' and cell2 == 'O' and cell3 == 'S':
                        sosChains.append(positions)

        # If SOS returned, the list sosChains will have values for the following iterator, which will draw the SOS
        currentPlayer = self.getCurrentPlayer()
        for chain in sosChains:
            self.drawSOSChain(chain, currentPlayer.color)
            currentPlayer.incrementScore()

    def gameOverHandler(self):
        """Template Method to be overriden by the subclasses"""
        pass

    def isBoardFull(self):
        """Function will check to see if there are remaining moves
        this will be used by general game to declare a tie if both player's scores = 0 when this function is called
        and returns a positive boolean value, and will be the end game trigger in the general game to determine
        when the game is over, check the scores, and declare a winner"""
        return all(cell != '' for row in self.cellState for cell in row)

    def endGame(self, message):
        """Common logic for the end of a game"""
        self.activeGame = False
        for row in self.cells:
            for cell in row:
                cell.config(state='disabled')
        messagebox.showinfo("Game Over", message)

    def startGame(self):
        """Begin the game and apply the logic to the game board
        Common functionality for both subclasses"""
        super().startGame()
        dimN = int(self.dimensions.get().split('x')[0])

        self.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]
        self.activeGame = True

        # Ensure no score data was held from previous game
        for player in self.players:
            if player.score != 0:
                player.score = 0

        for i in range(dimN):
            for j in range(dimN):
                self.cells[i][j].config(command=lambda row=i, col=j: self.cellClicked(row, col))

        self.updatePlayerChar()

        self.updateTurnFrame()


class simpleSOSGame(SOSGame):
    """This class will implement the SOS game with the general rule set, in which the player who completes an SOS chain
    first wins the game"""

    def simpleGameOver(self):
        """This function will be called after a move has been made to determine if the move that was made
        created an SOS chain, and if so, end the game and announce the player who made the SOS as the winner"""


class generalSOSGame(SOSGame):
    """This class will implement the SOS game with the general rule set, in which the player
    with the most complete SOS chains at the end of the game will be the winner"""

    def generalGameOver(self):
        """This function will determine if a general game has ended by checking if there are valid moves left to make
        if there are no valid moves left, the function will evaluate which of the two player's has scored the most
        points, and will announce that that player is the winner"""
        pass


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
