import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from GUI_2 import gameBoard  # Replace with your actual import


class TestSOSGameLogic(unittest.TestCase):
    """This class contains the unit tests for SOSGame.py"""
    pass



class TestSOSGUI(unittest.TestCase):
    """This class will test the function and fulfillment of acceptance criteria for the GUI
    """

    def setUp(self):
        """Set up test fixtures"""
        self.testRoot = tk.Tk()
        self.testRoot.withdraw()

        # Create a gameBoard instance with mocked dependencies to not create those GUI objects during tests
        with patch('tkinter.Frame') as mockFrame:
            self.testBoard = gameBoard(self.testRoot)


    def tearDown(self):
        """Clean up after tests"""
        self.testRoot.destroy()

    def testAC1_1_SizeMenuCreatedOnLaunch(self):
        """Verify that the dropdown menu is created upon launch of the program"""

        with patch('tkinter.Label') as mockLabel, patch('tkinter.ttk.Combobox') as mockComboBox:

            # Call the boardSize() method
            self.testBoard.boardSize()

            # Verify dropdown menu created
            mockComboBox.assert_called_once()

            # Verify that this dropdown menu was created within the correct setup frame
            callArgs = mockComboBox.call_args
            self.assertEqual(callArgs[0][0], self.testBoard.setupFrame)

    def testAC1_1_DropdownMenuValuesAreInRange(self):
        """Test that the dropdown menu values are within the range of 3x3-12x12"""
        with patch('tkinter.ttk.Combobox') as mockComboBox:
            self.testBoard.boardSize()

            # Get the values that are passed to the combo box dropdown menu
            callRargs = mockComboBox.call_args[1]
            realVals = callRargs['values']

            # verify that all values are in correct range and formatting
            expectedVals = [f"{i}x{i}" for i in range(3,13)]
            self.assertEqual(realVals, expectedVals)





if __name__ == '__main__':
    unittest.main()
