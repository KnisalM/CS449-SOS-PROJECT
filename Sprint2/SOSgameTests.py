import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from GUI_2 import gameBoard


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

        with patch('tkinter.ttk.Combobox') as mockComboBox:
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
            expectedVals = [f"{i}x{i}" for i in range(3, 13)]
            self.assertEqual(realVals, expectedVals)

    def testAC1_1_SelectionStoredInDimensions(self):
        """Verify that the player's selection can be properly split and stored in self.dimensions"""

        # Create list of test inputs
        testSizes = ['5x5', '8x8', '12x12']

        for testInput in testSizes:
            with self.subTest(boardDim=testInput):
                # Simulate the player selecting testInput as their dimensions
                self.testBoard.dimensions.set(testInput)

                # Verify here that the value is stored and retreivable
                storedVal = self.testBoard.dimensions.get()
                self.assertEqual(storedVal, testInput)

                # Verify that it is stored as a string and can be split and parsed
                dimensions = int(storedVal.split('x')[0])
                self.assertIsInstance(dimensions, int)

    def testAC2_1_SimpleandGeneralRadioButtonsExist(self):
        """Verify that the radio buttons for simple and general both exist"""
        with patch('tkinter.ttk.Radiobutton') as mockRadioButton:
            # Call the method ruleSetSelection()
            self.testBoard.ruleSetSelection()

            # Verify that for 2 radio buttons, radio buttons was called twice
            self.assertEqual(mockRadioButton.call_count, 2)

            # Put calls to radio buttons in a list
            calls = mockRadioButton.call_args_list

            # Verify properties of radio buttons (simpleRB)
            simpleCall = calls[0]
            self.assertEqual(simpleCall[0][0], self.testBoard.setupFrame)
            self.assertEqual(simpleCall[1]['variable'], self.testBoard.ruleSet)
            self.assertEqual(simpleCall[1]['value'], 'simple')

            # Verify properties of radio buttons (generalRB)
            generalCall = calls[1]
            self.assertEqual(generalCall[0][0], self.testBoard.setupFrame)
            self.assertEqual(generalCall[1]['variable'], self.testBoard.ruleSet)
            self.assertEqual(generalCall[1]['value'], 'general')

    def testAC2_1_UpdateRuleSetStoredProperly(self):
        """Verify that radio buttons are exclusive and store the value correctly as a string in the self.ruleSet variable"""

        # Test that the selected rule set is stored properly
        self.testBoard.ruleSet.set('simple')
        self.assertEqual(self.testBoard.ruleSet.get(), 'simple')
        self.assertNotEqual(self.testBoard.ruleSet.get(), 'general')

        # Switch to general and ensure it was properly stored
        self.testBoard.ruleSet.set('general')
        self.assertEqual(self.testBoard.ruleSet.get(), 'general')
        self.assertNotEqual(self.testBoard.ruleSet.get(), 'simple')

        # Switch back to simple and ensure it was properly stored
        self.testBoard.ruleSet.set('simple')
        self.assertEqual(self.testBoard.ruleSet.get(), 'simple')
        self.assertNotEqual(self.testBoard.ruleSet.get(), 'general')

        # Test that variable holds a str value and is one of the two valid options
        self.assertIsInstance(self.testBoard.ruleSet.get(), str)
        self.assertIn(self.testBoard.ruleSet.get(), ['simple', 'general'])

    """The following tests will later be retitled to reflect the start buttons connection to User Story 4 and its
        corresponding acceptance criteria, however at the moment I do not have the player modes created,
        so I cannot test user story 4 in its entirety. The following tests will test the conditions under when the 
        begin game button is called, and ensures that it is not called when not all conditions are met"""

    def testBeginButtonNotShownWhenNoConditionsMet(self):
        with patch('tkinter.Button') as mockButton:
            # Test case when neither self.dimensions or self.ruleSet has a value
            self.testBoard.dimensions.set('')
            self.testBoard.ruleSet.set('')
            self.testBoard.startConditions()

            # Verify that with variables empty, no button was created
            mockButton.assert_not_called()

    def testBeginButtonNotShownWhenOnlyDimensionsSet(self):
        with patch('tkinter.Button') as mockButton:
            # Test case where only dimension has values
            self.testBoard.dimensions.set('5x5')
            self.testBoard.ruleSet.set('')
            self.testBoard.startConditions()

            # Verify that with only self.dimensions occupied, the button hasn't been called
            mockButton.assert_not_called()

    def testBeginButtonNotShownWhenOnlyRuleSetSet(self):
        with patch('tkinter.Button') as mockButton:
            # Test case where only self.ruleSet has value
            self.testBoard.dimensions.set('')
            self.testBoard.ruleSet.set('simple')
            self.testBoard.startConditions()

            # Verify that with only self.ruleSet occupied, the button was not called
            mockButton.assert_not_called()

    def testBeginButtonShownWhenConditionsAreMet(self):
        with patch('tkinter.Button') as mockButton:

            # When conditions are met for self.dimensions and self.ruleSet, button is called
            self.testBoard.dimensions.set('5x5')
            self.testBoard.ruleSet.set('simple')
            self.testBoard.startConditions()

            # Verify that button was created when both conditions are filled
            mockButton.assert_called()

    """The following tests will apply to several user stories and their corresponding acceptance criteria
    these tests will demonstrate that the function "create player frame" creates a valid frame within
    the parent frame, that this frame displays the player who the frame belongs to, that this frame contains two
    radio buttons with options 'S' and 'O', and that when one of these radio buttons is selected, the other is 
    not selected, and that when a radio button is selected the value is stored in self.moveChar. This will assist with 
    user stories 5-6, 8-10 (Make move in simple game human, make move in simple game computer, make move in general game
    human, make move in general game computer, determine general game is over), with some tests still to be implemented
    in future sprints"""



if __name__ == '__main__':
    unittest.main()
