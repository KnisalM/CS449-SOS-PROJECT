import unittest
from unittest.mock import Mock, patch
from SOSGame import *
from GUI_2 import *
import tkinter as tk


class TestSOSGameLogic(unittest.TestCase):
    """This class contains the unit tests for SOSGame.py
    This class will ensure that all game logic based acceptance
    criteria for this Sprint are met by the code that has been
    implemented in SOSGame.py"""


class TestSOSGUI(unittest.TestCase):
    def setUp(self):
        """set up a root window for each test """
        self.root = tk.Tk()
        self.root.withdraw() # Hide the window from showing up during tests

    def tearDown(self):
        """Clean up fixtures after test"""
        self.root.destroy()





if __name__ == '__main__':
    unittest.main()





