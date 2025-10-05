import tkinter as tk
import pylint
import unittest


class gameBoard():
    def __init__(self):
        self.root = tk.Tk()
        self.rootTitle("SOS Game")
        self.dimensions = '' # The variable that will store the player's selection for the dimensions of the board
        self.ruleSet = '' # This variable will store whether the player has selected to play a
        #self.opponentType = '' Will Implement later, this will store the player's selection for Human v Human or Human v Machine
        self.currentTurn = ''
        #self.active = '' Implement in later sprint, will track game state and update when game is over
        self.cells = []
        #self.cellsState = [] Implement in later Sprint, will track the state of the cells
        #self.player1Score = 0
        #self.player2Score = 0

