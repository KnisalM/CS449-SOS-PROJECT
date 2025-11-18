import tkinter as tk
from tkinter import messagebox
from GUI_4 import gameBoard


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

        self.gameInstance = None

    def setChar(self, character):
        """This function will set the character for the player to play based on their selection in the frame"""
        if character in ['S', 'O']:
            self.character = character

    def getChar(self):
        """Get the current selected character"""
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
    pass


class SOSGame(gameBoard):
    """This class will extend the class gameBoard from GUI_2.py, and will begin implementing the actual game logic onto the board"""

    def __init__(self, root):
        # Initialize gameBoard components
        super().__init__(root)

        # Initialize game variables
        self.players = []
        self.currentPlayer = 0  # Start with Player 1
        self.activeGame = True
        self.cellState = []  # Track the state of the cells and whether there is currently a play made on a cell
        self.cellOwner = []  # Track ownership of cells

    def initializePlayers(self):
        """Initialize the players based on selected player types for each player"""
        # Player 2 changes based on the game type selected
        if self.p1_type.get() == 'Human':
            player1 = Player(1, 'Human')
        else:
            player1 = computerPlayer(1)

        # Player 2 changes based on the game type selected
        if self.p2_type.get() == 'Human':
            player2 = Player(2, 'Human')
        else:
            player2 = computerPlayer(2)

        self.players = [player1, player2]

    def getCurrentPlayer(self):
        """Get and return the current player"""
        return self.players[self.currentPlayer]

    def switchTurn(self):
        """Switch turns so that player who is not playing can't make a move and scores are tracked appropriately"""
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.updateTurnFrame(self.getCurrentPlayer())

    def updatePlayerChar(self):
        """get what character the player has selected for the move to be made"""
        self.players[0].setChar(self.p1Move.get())
        self.players[1].setChar(self.p2Move.get())

    def cellClicked(self, row, col):
        """Define the events when an empty cell is clicked"""
        if not self.activeGame or self.cellState[row][col] != '':
            return

        self.updatePlayerChar()
        currentPlayer = self.getCurrentPlayer()
        moveChar = currentPlayer.getChar()

        self.makeAMove(row, col, moveChar, currentPlayer.color)

    def makeAMove(self, row, col, moveChar, color):
        """Execute when a valid move is made to reflect on board and update game state
    Commonly Used Functionality between both general and simple SOSGame subclasses"""
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
        self.cellOwner[row][col] = self.currentPlayer  # Track player that made move
        self.cells[row][col].config(text=moveChar, fg=color, state='disabled', disabledforeground=color,
                                    relief='sunken', font=fontConfig)

        # Check for a SOS chain after the move by calling checkSOSFormed function
        sosChains = self.checkSOSFormed(row, col)
        currentPlayer = self.getCurrentPlayer()
        for chain in sosChains:
            self.drawSOSChain(chain, currentPlayer.color)
            currentPlayer.incrementScore()

        self.gameOverHandler()

    def checkSOSFormed(self, row, col):
        """This function will check if an SOS has been formed after each move. If a player has created an SOS, then their
        score will be incremented. A simple game will utilize this to tell a game is over when one of the player's score
        is !=0, and a general game will use this to increment the player's score and track who wins by who has the most
        SOS made when there are no moves left"""
        sosChains = []
        boardDim = len(self.cellState)

        # Define the directions to check in, their opposites are handled by checking in both directions
        directionsToCheck = [
            (0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)
        ]

        # Use a set to track unique SOS Chains
        uniqueChains = set()

        for directionOne, directionTwo in directionsToCheck:

            # Updating function to check both directions from an O placed in the middle and check when a char is placed at beginning or end
            patternsToCheck = [
                [0, 1, 2],
                [-1, 0, 1],
                [-2, -1, 0]
            ]

            for pattern in patternsToCheck:

                # Calculate what the positions are for the 3 positions that would form an SOS in this direction
                positions = []
                validPositions = True

                for offset in pattern:
                    r = row + (offset * directionOne)
                    c = col + (offset * directionTwo)

                    if 0 <= r < boardDim and 0 <= c < boardDim:
                        positions.append((r, c))
                    else:
                        validPositions = False
                        break

                # If there are 3 valid positions in the list, check if they form an SOS
                if validPositions and len(positions) == 3:
                    # get cell values and owners
                    cellValues = []
                    cellOwners = []

                    for posRow, posCol in positions:
                        cellValues.append(self.cellState[posRow][posCol])
                        cellOwners.append(self.cellOwner[posRow][posCol])

                    # Check if pattern is an SOS
                    if cellValues[0] == 'S' and cellValues[1] == 'O' and cellValues[2] == 'S':
                        # Check all cells are same player
                        if (cellOwners[0] is not None and
                                cellOwners[0] == cellOwners[1] == cellOwners[2]):

                            chainId = tuple(sorted(positions))  # Sort to make order consistent
                            if chainId not in uniqueChains:
                                uniqueChains.add(chainId)
                                sosChains.append(positions)

        return sosChains

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
        messagebox.showinfo("Game Over", message)
        for row in self.cells:
            for cell in row:
                cell.config(state='disabled')

    def startGame(self):
        """Initialize the game board state and prepare it for the game"""
        self.createUIElements()
        self.initializePlayers()

        dimN = int(self.dimensions.get().split('x')[0])

        # Initialize the game state
        self.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]
        self.cellOwner = [[None for _ in range(dimN)] for _ in range(dimN)]

        self.activeGame = True

        # Ensure all scores are reset
        for player in self.players:
            player.score = 0

        # Set up cell clicks
        for i in range(dimN):
            for j in range(dimN):
                self.cells[i][j].config(command=lambda row=i, col=j: self.cellClicked(row, col))

        self.updatePlayerChar()
        self.updateTurnFrame(self.getCurrentPlayer())


class simpleSOSGame(SOSGame):
    """This class will implement the SOS game with the general rule set, in which the player who completes an SOS chain
    first wins the game"""

    def gameOverHandler(self):
        """This function will be called after a move has been made to determine if the move that was made
        created an SOS chain, and if so, end the game and announce the player who made the SOS as the winner"""

        currentPlayer = self.getCurrentPlayer()

        # If Player scored, they win game
        if currentPlayer.score > 0:
            self.endGame(f"{currentPlayer.name} wins!")
        elif self.isBoardFull():
            # Board is now full and no SOS was made
            self.endGame("Game ended in a draw, no one scored!")
        else:
            # Switch turns if no SOS was formed
            self.switchTurn()


class generalSOSGame(SOSGame):
    """This class will implement the SOS game with the general rule set, in which the player
    with the most complete SOS chains at the end of the game will be the winner"""

    def gameOverHandler(self):
        """This function will determine if a general game has ended by checking if there are valid moves left to make
        if there are no valid moves left, the function will evaluate which of the two player's has scored the most
        points, and will announce that that player is the winner"""
        if self.isBoardFull():
            # Board is full - determine winner
            self.determineWinner()
        else:
            # Continue game - switch turns
            self.switchTurn()

    def determineWinner(self):
        """Determine and announce the winner when the board is full in a general game"""
        p1Score = self.players[0].score
        p2Score = self.players[1].score

        if p1Score > p2Score:
            winner = self.players[0]
            message = f"{winner.name} wins the game with a score of {winner.score}"
        elif p2Score > p1Score:
            winner = self.players[1]
            message = f"{winner.name} wins the game with a score of {winner.score}"
        else:
            message = f"It's a tie! Both Players scored {p1Score} points"

        self.endGame(message)

    # Create a setup class to handle rule selection, will look at refactoring into classes, but testing for function


def main():
    root = tk.Tk()
    root.title('SOS GAME')
    root.geometry('1000x800')
    root.resizable(True, True)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Import setupGame locally to prevent circular imports
    from GUI_4 import setupGame
    setupInstance = setupGame(root)

    root.mainloop()


if __name__ == '__main__':
    main()
