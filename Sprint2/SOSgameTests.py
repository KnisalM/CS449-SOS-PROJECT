import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import SOSGame
import GUI_2 as gui
from GUI_2 import gameBoard


class TestPlayerClass(unittest.TestCase):
    """This class of tests will verify the function of the Player class
    At this time, the only testable method in the player class is setChar, which was created to replace the standard
    .set() function for the variable self.character. In later sprints, I will implement a method to increment the
    player's score as well. An important note is that while I have implemented tests that demonstrate the error
    catching capability of the function, there is no way for an invalid character to be passed to the function
    in the real game implementation, as the only call for the setChar method is associated with the radio buttons
    within the player frame, which exclusively contain the valid values 'S' and 'O'"""

    def setUp(self):
        # Set up text fixtures
        self.player = SOSGame.Player(player_number=1)

    def testAC5_7and5_8_SetCharUpdatesCharacterWhenValidCharacterO(self):
        """Verify that setChar updated self.character when passed 'O'"""

        # Setup initial state
        initialChar = self.player.character
        self.assertEqual(initialChar, 'S')  # 'S' is the default character as established in the Player class

        # Call method with valid character 'O'
        self.player.setChar('O')

        # Verify that self.character was updated
        self.assertEqual(self.player.character, 'O')

    def testAC5_7and5_8_SetCharUpdatesCharacterWhenValidCharacterS(self):
        """Verify that when self.character = 'O' and setChar passes 'S', self.character is updated to 'S'"""

        # Already verified that when passed 'O', setChar updates from default state 'S' to 'O', start here in this test
        self.player.setChar('O')
        self.assertEqual(self.player.character, 'O')

        # Call method setChar with valid character 'S'
        self.player.setChar('S')
        self.assertEqual(self.player.character, 'S')

    def testAC5_7and5_8_SetCharDoesNotUpdateWhenInvalidCharacter(self):
        """Verify that setChar doesn't update the variable self.dimensions when passed an invalid character, and that
        self.dimensions retains the last valid value"""
        invalidTests = ['x', 'a', 'F', 'B', '1', '', 'So', 'SO', 'OS']

        for invalidChar in invalidTests:
            # Set to known valid state before each test
            self.player.setChar('S')

            # Call method with invalidChar
            self.player.setChar(invalidChar)

            # Verify character was NOT updated
            self.assertEqual(self.player.character, 'S')



class TestSOSGameClass(unittest.TestCase):
    """This class will test the functionality and fulfillment of acceptance criteria for the SOSGame class"""

    def setUp(self):
        # Create a root window for testing to occur in
        self.testRealRoot = tk.Tk()
        self.testRealRoot.withdraw()

        # Create an instance of the SOS game with mocked dependencies
        with patch('tkinter.Frame') as mockFrame:
            self.sosGame = SOSGame.SOSGame(self.testRealRoot)


    def tearDown(self):
        """Clean up the windows after tests"""
        if hasattr(self, 'testRealRoot'):
            self.testRealRoot.destroy()

    """This getCurrentPlayer() function is a helper function. It does not directly fulfill any acceptance criteria in and of itself,
        but it does assist with several user stories and their corresponding acceptance criteria. The stories it
        helps with are 5, 7, 8, and 10. This function assists by getting which is the current player and returning
        that value from the list self.players, so that the functions that call this method can read
        attributes from the player, and will be able to fulfill these user stories in their entirety. The tests for 
        this function will demonstrate that it returns a Player object, and that the attributes of this Player
        object can be accessed"""
    def testGetCurrentPlayerReturnsCorrectPlayerWithIndex(self):
        """Verify that getCurrentPlayer returns a Player Object and that it is the correct Player from self.players[
        self.currentPlayer]"""

        # Test with currentPlayer = 0 (player 1)
        self.sosGame.currentPlayer = 0
        player1 = self.sosGame.getCurrentPlayer()

        # Verify that this call returns the correct player object
        self.assertIsInstance(player1, SOSGame.Player)
        self.assertEqual(player1, self.sosGame.players[0])

        # Test with currentPlayer = 1 (player 2)
        self.sosGame.currentPlayer = 1
        player2 = self.sosGame.getCurrentPlayer()

        # Verify that this call returns the correct player object
        self.assertIsInstance(player2, SOSGame.Player)
        self.assertEqual(player2, self.sosGame.players[1])

    def testGetCurrentPlayerReturnedPlayerAttributesAccessible(self):
        """Verify that the currently needed Player attributes self.name, self.color, self.character, are all accessible"""

        # Test that attributes are accessible in returned player objects
        playerIndexes = [0, 1]
        for index in playerIndexes:
            self.sosGame.currentPlayer = index
            player = self.sosGame.getCurrentPlayer()

            # Verify that all the necessary attributes are accessible
            self.assertNotEqual(player.name, '')
            self.assertNotEqual(player.color, '')
            self.assertEqual(player.character, 'S')

    def testAC5_1and8_1TurnUpdatedToBlueWhenRedMakesValidMove(self):
        """This test will demonstrate that when the Red Player makes a valid move, the turn will be updated to blue
        player's turn. These AC will be tested together because the AC are exactly the same regardless of game rules"""

        # Setup conditions such that it is Red Player's turn
        self.sosGame.currentPlayer = 0
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 1)
        self.assertEqual(firstPlayer.color, 'red')

        # Simulate switchTurn method being called
        with patch.object(self.sosGame, 'updateTurnFrame') as mockUpdateTurn:
            self.sosGame.switchTurn()

            # Check that current player is updated to Player 2
            self.assertEqual(self.sosGame.currentPlayer, 1)
            secondPlayer = self.sosGame.getCurrentPlayer()
            self.assertEqual(secondPlayer.player_number, 2)
            self.assertEqual(secondPlayer.color, 'blue')

            # Verify that updateTurnFrame was called once
            mockUpdateTurn.assert_called_once()

    def testAC5_4and8_4TurnUpdatedToRedWhenBlueMakesValidMove(self):
        """This test will demonstrate that when the Red Player makes a valid move, the turn will be updated to blue
        player's turn. These AC will be tested together because the AC are exactly the same regardless of game rules"""

        # Setup conditions such that it is Blue Player's turn
        self.sosGame.currentPlayer = 1
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 2)
        self.assertEqual(firstPlayer.color, 'blue')

        # Simulate switchTurn method being called
        with patch.object(self.sosGame, 'updateTurnFrame') as mockUpdateTurn:
            self.sosGame.switchTurn()

            # Check that current player is updated to Player 1
            self.assertEqual(self.sosGame.currentPlayer, 0)
            secondPlayer = self.sosGame.getCurrentPlayer()
            self.assertEqual(secondPlayer.player_number, 1)
            self.assertEqual(secondPlayer.color, 'red')

            # Verify that updateTurnFrame was called once
            mockUpdateTurn.assert_called_once()

    def testAC5_2and8_2RedPlayerAttemptsAMoveOnAnOccupiedCell(self):
        """Verify that when a move is attempted on a cell that is already occupied, the cell will not be changed,
        and the player turn update method will not be called"""




class TestgameBoardClass(unittest.TestCase):
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
    these tests will demonstrate that the function "createPlayerFrame()" displays the player who the frame belongs to, 
    that this frame contains two radio buttons with options 'S' and 'O', and that frames can be created for both players 
    such that the selection of radio buttons in one frame has no impacton the selected character to place in the other 
    player's frame. This will assist with user stories 5-6, 8-10 (Make move in simple game human, make move in simple 
    game computer, make move in general game human, make move in general game computer, determine general game is over),
    with some tests still to be implemented in future sprints"""

    def testCreatePlayerFrameCreatesPlayerNameLabel(self):
        testNames = ['Red Player', 'Blue Player']

        for playerName in testNames:
            with patch('tkinter.Label') as mockLabel, patch('tkinter.Frame') as mockFrame, \
                    patch('tkinter.ttk.Radiobutton'):
                mockParent = Mock()
                mockSubFrame = Mock()
                mockFrame.return_value = mockSubFrame
                mockLabelInstance = Mock()
                mockLabel.return_value = mockLabelInstance

                gui.createPlayerFrame(mockParent, 1, 0, playerName, self.testBoard.p1Move)

                # Verify that label was created with correct parent text and font
                mockLabel.assert_any_call(mockSubFrame, text=playerName, font=('Arial', 12))

                # Verify label was placed in grid properly
                mockLabelInstance.grid.assert_any_call(row=0, column=0, columnspan=2, pady=(0, 10))

    def testCreatePlayerFrameCreatesRadioButtons(self):
        """Verify that a player frame has two radio buttons with values 'S' and 'O' """
        with patch('tkinter.ttk.Radiobutton') as mockRadioButton:
            mockParent = Mock()
            mockSubFrame = Mock()

            with patch('tkinter.Frame', return_value=mockSubFrame), patch('tkinter.Label'):
                # Mock the radio button instances
                mockSButton = Mock()
                mockOButton = Mock()
                mockRadioButton.side_effect = [mockSButton, mockOButton]

                gui.createPlayerFrame(mockParent, 1, 0, 'Red Player', self.testBoard.p1Move)

                # Verify two radio buttons were created
                self.assertEqual(mockRadioButton.call_count, 2)

                # Make a list of the calls to make a radio button
                calls = mockRadioButton.call_args_list

                # Verify the properties of the 'S' radio button
                sCall = calls[0]
                self.assertEqual(sCall[0][0], mockSubFrame)
                self.assertEqual(sCall[1]['text'], 'S')
                self.assertEqual(sCall[1]['variable'], self.testBoard.p1Move)
                self.assertEqual(sCall[1]['value'], 'S')

                # Verify same properties for 'O' radio button
                oCall = calls[1]
                self.assertEqual(oCall[0][0], mockSubFrame)
                self.assertEqual(oCall[1]['text'], 'O')
                self.assertEqual(oCall[1]['variable'], self.testBoard.p1Move)
                self.assertEqual(oCall[1]['value'], 'O')

                # Verify grid placements of radio buttons
                mockSButton.grid.assert_called_once_with(row=1, column=0, sticky=tk.W, pady=2)
                mockOButton.grid.assert_called_once_with(row=2, column=0, sticky=tk.W, pady=2)

    def testCreatePlayerFrameWithDifferentMoveVariableAssociated(self):
        """Verify that two frames can be created with different associated move variables"""
        with patch('tkinter.Frame') as mockFrame, patch('tkinter.Label') as mockLabel, \
                patch('tkinter.ttk.Radiobutton') as mockRadioButton:

            mockParent = Mock()
            mockSubFrame = Mock()
            mockFrame.return_value = mockSubFrame

            # Test creation with p1 move
            gui.createPlayerFrame(mockParent, 1, 0, 'Red Player', self.testBoard.p1Move)

            # Verify that radio buttons in this frame use p1Move variable
            callsWithP1 = mockRadioButton.call_args_list
            for callArgs in callsWithP1:
                self.assertEqual(callArgs[1]['variable'], self.testBoard.p1Move)

            # Reset the Mock and test with p2 move
            mockRadioButton.reset_mock()

            # Test creation with p1 move
            gui.createPlayerFrame(mockParent, 1, 2, 'Blue Player', self.testBoard.p2Move)

            # Verify that radio buttons in this frame use p2Move variable
            callsWithP2 = mockRadioButton.call_args_list
            for callArgs in callsWithP2:
                self.assertEqual(callArgs[1]['variable'], self.testBoard.p2Move)

    """The following tests will verify the functionality of the startGame() method in the GUI class, demonstrating
    at this time that when the begin button is pressed, calling startGame(), then a board of selectable buttons
    will be created in the proper dimension selected, and that there will be 2 player frames in addition to the game 
    board. I will not be demonstrating in the following tests that the radio buttons exist in the player frame,
    or that their values are correct, or that they update the correct variable, as this was all validated by my 
    tests on the createPlayerFrame() method. I also will not be testing any of the logic implementation in the 
    following tests, as those will be tested by my unit tests for the logic file, SOSGame.py, in which
    the method startGame() inherits this method, and will implement rule set and computer vs human / human vs human"""

    def testAC4_1and4_2_startGameGeneratesBoardWithCorrectDimensions(self):
        """Verify that when the startGame() method is called and the board is created, the board that is created
        has the correct dimensions that match the value from self.dimensions, selected by the player"""

        # Testing with various board sizes,  not just one test case
        testSizes = ['3x3', '5x5', '8x8', '11x11']

        for size in testSizes:
            with self.subTest(boardSize=size), patch.object(self.testBoard.setupFrame, 'destroy'), \
                    patch('tkinter.Frame') as mockFrame, patch('tkinter.Button') as mockButton, \
                    patch('GUI_2.createPlayerFrame'):

                # Set up dimensions
                self.testBoard.dimensions.set(size)
                self.testBoard.ruleSet.set('simple')
                expectedDim = int(size.split('x')[0])

                # Mock board frame and buttons
                mockBoardFrame = Mock()
                mockFrame.return_value = mockBoardFrame

                # Clear existing cells from any previous tests that weren't wiped
                self.testBoard.cells = []

                # Reset mock counter to ensure buttons called prior to this are not counted
                mockButton.reset_mock()

                # Call method we are testing
                self.testBoard.startGame()

                # Verify that correct # of buttons are created (total number of buttons equals expectedDim^2
                expectedButtonTotal = expectedDim * expectedDim
                self.assertEqual(mockButton.call_count, expectedButtonTotal)

                # Verify cell list has proper amount of rows and columns, showing that the formatting is correct
                self.assertEqual(len(self.testBoard.cells), expectedDim)

                for rowIndex, row in enumerate(self.testBoard.cells):
                    self.assertEqual(len(row), expectedDim)

    def testAC4_1and4_2_startGameCreatesPlayerFrames(self):
        """Verify that when startGame() is ran, the method GUI_2.createPlayerFrame is called twice, and that the frames
        have the appropriate attributes for the 2 players frames that are created"""

        with patch.object(self.testBoard.setupFrame, 'destroy'), patch('tkinter.Frame') as mockFrame, \
                patch('tkinter.Button') as mockButton, patch('GUI_2.createPlayerFrame') as mockCreatePlayerFrame:
            # Set up valid conditions
            self.testBoard.dimensions.set('5x5')
            self.testBoard.ruleSet.set('simple')

            # Create a Mock of the board frame
            mockBoardFrame = Mock()
            mockFrame.return_value = mockBoardFrame

            # Call the method we are testing
            self.testBoard.startGame()

            # Verify that createPlayerFrame was called twice, showing that both players were attributed a sub frame
            self.assertEqual(mockCreatePlayerFrame.call_count, 2)

            # Create a list of all the calls to mockCreatePlayerFrame so that we can verify their attributes
            calls = mockCreatePlayerFrame.call_args_list

            # Verify that the Red Player's frame was created with the correct parameters
            redPlayerCall = calls[0]
            self.assertEqual(redPlayerCall[0][0], self.testBoard.gameFrame)
            self.assertEqual(redPlayerCall[0][3], 'Red Player')
            self.assertEqual(redPlayerCall[0][4], self.testBoard.p1Move)

            # Verify that the Blue Player's frame was created with the correct parameters
            bluePlayerCall = calls[1]
            self.assertEqual(bluePlayerCall[0][0], self.testBoard.gameFrame)
            self.assertEqual(bluePlayerCall[0][3], 'Blue Player')
            self.assertEqual(bluePlayerCall[0][4], self.testBoard.p2Move)


if __name__ == '__main__':
    unittest.main()
