import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import SOSGame_4 as SOSGame
import GUI_4 as gui
from GUI_4 import gameBoard


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

    def testAC1_2BoardIsDestroyedAndPlayerReturnedToSetupFrame(self):
        """this test will verify upon creation that when the player selects to end the game they
        are currently in and begin a new game, they will be returned to a setup frame with the same
        conditions as the initial setup frame"""
        pass

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
        """Verify that when createUIElements() is called, the board has correct dimensions"""

        # Testing with various board sizes
        testSizes = ['3x3', '5x5', '8x8', '11x11']

        for size in testSizes:
            with self.subTest(boardSize=size), patch.object(self.testBoard.setupFrame, 'destroy'), \
                    patch('tkinter.Frame') as mockFrame, patch('tkinter.Button') as mockButton, \
                    patch('GUI_4.createPlayerFrame'):

                # Set up dimensions
                self.testBoard.dimensions.set(size)
                expectedDim = int(size.split('x')[0])

                # Mock board frame
                mockBoardFrame = Mock()
                mockFrame.return_value = mockBoardFrame

                # Clear existing cells
                self.testBoard.cells = []
                mockButton.reset_mock()

                # Call createUIElements directly
                self.testBoard.createUIElements()

                # Verify that correct # of buttons are created
                expectedButtonTotal = expectedDim * expectedDim
                self.assertEqual(mockButton.call_count, expectedButtonTotal)

                # Verify cell list has proper dimensions
                self.assertEqual(len(self.testBoard.cells), expectedDim)
                for row in self.testBoard.cells:
                    self.assertEqual(len(row), expectedDim)

    def testAC4_1and4_2_startGameCreatesPlayerFrames(self):
        """Verify that createUIElements creates player frames"""

        with patch.object(self.testBoard.setupFrame, 'destroy'), \
                patch('tkinter.Frame') as mockFrame, \
                patch('tkinter.Button'), \
                patch('GUI_4.createPlayerFrame') as mockCreatePlayerFrame:
            self.testBoard.dimensions.set('5x5')

            # Call createUIElements directly (this is called by startGame in subclasses)
            self.testBoard.createUIElements()

            # Verify createPlayerFrame was called twice
            self.assertEqual(mockCreatePlayerFrame.call_count, 2)


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

        # Set up common game condition
        self.sosGame.dimensions.set('3x3')
        self.sosGame.ruleSet.set('simple')
        self.sosGame.p1Move.set('S')
        self.sosGame.p2Move.set('O')

        # Initialize minimal game state without full UI
        dimN = 3
        self.sosGame.cells = [[Mock() for _ in range(dimN)] for _ in range(dimN)]

        # Mock the individual cell buttons
        for i in range(dimN):
            for j in range(dimN):
                self.sosGame.cells[i][j] = Mock()
                self.sosGame.cells[i][j].config = Mock()
                self.sosGame.cells[i][j].grid = Mock()  # Add grid method mock

        # Mock GUI methods
        self.sosGame.drawSOSChain = Mock()
        self.end_game_mock = Mock()
        self.sosGame.endGame = self.end_game_mock

        # Initialize game arrays with proper dimensions - CRITICAL FIX
        self.sosGame.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]
        self.sosGame.cellOwner = [[None for _ in range(dimN)] for _ in range(dimN)]

        # Set initial game state
        self.sosGame.activeGame = True
        self.sosGame.currentPlayer = 0  # Start with Red Player
        for player in self.sosGame.players:
            player.score = 0

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

    def testAC3_1PlayerChoosesToPlayAgainstAHuman(self):
        """This test will verify that when the player chooses to play against a human player, no computer
        player is generated"""

    def testAC3_2PlayerChoosesToPlayAgainstAComputer(self):
        """This test will verify that when the player chooses to play against a computer player, a computer
        player is generated"""

    def testAC5_1and8_1TurnUpdatedToBlueWhenRedMakesValidMove(self):
        """This test will demonstrate that when the Red Player makes a valid move, the turn will be updated to blue
        player's turn. These AC will be tested together because the AC are exactly the same regardless of game rules"""

        # Setup conditions such that it is Red Player's turn
        self.sosGame.currentPlayer = 0
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 1)
        self.assertEqual(firstPlayer.color, 'Red')

        # Simulate switchTurn method being called
        with patch.object(self.sosGame, 'updateTurnFrame') as mockUpdateTurn:
            self.sosGame.switchTurn()

            # Check that current player is updated to Player 2
            self.assertEqual(self.sosGame.currentPlayer, 1)
            secondPlayer = self.sosGame.getCurrentPlayer()
            self.assertEqual(secondPlayer.player_number, 2)
            self.assertEqual(secondPlayer.color, 'Blue')

            # Verify that updateTurnFrame was called once
            mockUpdateTurn.assert_called_once()

    def testAC5_2and8_2RedPlayerAttemptsAMoveOnAnOccupiedCell(self):
        """Verify that when a move is attempted on a cell that is already occupied, the cell will not be changed,
        and the player turn update method will not be called"""
        # Set up a mock 3x3 game board for move testing
        self.sosGame.cells = [[Mock() for _ in range(3)] for _ in range(3)]
        self.sosGame.cellState = [['' for _ in range(3)] for _ in range(3)]

        # Set up initial game state with Red Player's turn in an ongoing game
        self.sosGame.currentPlayer = 0
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 1)
        self.assertEqual(firstPlayer.color, 'Red')

        # Simulate that cell 0,0 is occupied by Blue Player
        occRow, occCol = 0, 0
        self.sosGame.makeAMove(occRow, occCol, 'S', 'Blue')
        self.assertEqual(self.sosGame.cellState[occRow][occCol], 'S')

        # Check that config was called with state='disabled' among other parameters
        self.sosGame.cells[occRow][occCol].config.assert_called_with(
            text='S', fg='Blue', state='disabled', disabledforeground='Blue',
            relief='sunken', font=('Arial', 14, 'bold')
        )

    def testAC5_4and8_4TurnUpdatedToRedWhenBlueMakesValidMove(self):
        """This test will demonstrate that when the Red Player makes a valid move, the turn will be updated to blue
        player's turn. These AC will be tested together because the AC are exactly the same regardless of game rules"""

        # Setup conditions such that it is Blue Player's turn
        self.sosGame.currentPlayer = 1
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 2)
        self.assertEqual(firstPlayer.color, 'Blue')

        # Simulate switchTurn method being called
        with patch.object(self.sosGame, 'updateTurnFrame') as mockUpdateTurn:
            self.sosGame.switchTurn()

            # Check that current player is updated to Player 1
            self.assertEqual(self.sosGame.currentPlayer, 0)
            secondPlayer = self.sosGame.getCurrentPlayer()
            self.assertEqual(secondPlayer.player_number, 1)
            self.assertEqual(secondPlayer.color, 'Red')

            # Verify that updateTurnFrame was called once
            mockUpdateTurn.assert_called_once()

    def testAC5_7and8_7RedPlayerMakesAnSMove(self):
        """Verify that Red Player's move updates game state correctly"""

        # Set up
        self.sosGame.currentPlayer = 0  # Red Player

        # Make move
        row, col = 1, 1
        self.sosGame.makeAMove(row, col, 'S', 'Red')

        # Simple assertions - just check the game state
        self.assertEqual(self.sosGame.cellState[row][col], 'S')
        self.assertEqual(self.sosGame.cellOwner[row][col], 0)
        self.assertTrue(self.sosGame.cells[row][col].config.called)

    def testAC5_7and8_7BluePlayerMakesAnSMove(self):
        """Verify that Blue Player's move updates game state correctly"""

        # Set up
        self.sosGame.currentPlayer = 1  # Blue Player

        # Make move
        row, col = 1, 1
        self.sosGame.makeAMove(row, col, 'S', 'blue')

        # Simple assertions - just check the game state
        self.assertEqual(self.sosGame.cellState[row][col], 'S')
        self.assertEqual(self.sosGame.cellOwner[row][col], 1)
        self.assertTrue(self.sosGame.cells[row][col].config.called)

    def testAC5_8and8_8RedPlayerMakesAnOMove(self):
        """Verify that Red Player's move updates game state correctly"""

        # Set up
        self.sosGame.currentPlayer = 0  # Red Player

        # Make move
        row, col = 1, 1
        self.sosGame.makeAMove(row, col, 'O', 'Red')

        # Simple assertions - just check the game state
        self.assertEqual(self.sosGame.cellState[row][col], 'O')
        self.assertEqual(self.sosGame.cellOwner[row][col], 0)
        self.assertTrue(self.sosGame.cells[row][col].config.called)

    def testAC5_8and8_8BluePlayerMakesAnOMove(self):
        """Verify that Blue Player's move updates game state correctly"""

        # Set up
        self.sosGame.currentPlayer = 1  # Blue Player

        # Make move
        row, col = 1, 1
        self.sosGame.makeAMove(row, col, 'S', 'Blue')

        # Simple assertions - just check the game state
        self.assertEqual(self.sosGame.cellState[row][col], 'S')
        self.assertEqual(self.sosGame.cellOwner[row][col], 1)
        self.assertTrue(self.sosGame.cells[row][col].config.called)

    def testAC5_5and8_5BluePlayerAttemptsAMoveOnAnOccupiedCell(self):
        """Verify that when a move is attempted on a cell that is already occupied, the cell will not be changed,
        and the player turn update method will not be called"""
        # Set up a mock 3x3 game board for move testing
        self.sosGame.cells = [[Mock() for _ in range(3)] for _ in range(3)]
        self.sosGame.cellState = [['' for _ in range(3)] for _ in range(3)]

        # Set up initial game state with Blue Player's turn in an ongoing game
        self.sosGame.currentPlayer = 1
        firstPlayer = self.sosGame.getCurrentPlayer()
        self.assertEqual(firstPlayer.player_number, 2)
        self.assertEqual(firstPlayer.color, 'Blue')

        # Simulate that cell 0,0 is occupied by Red Player
        occRow, occCol = 0, 0
        self.sosGame.makeAMove(occRow, occCol, 'O', 'Red')
        self.assertEqual(self.sosGame.cellState[occRow][occCol], 'O')

        # Check that config was called with state='disabled' among other parameters
        self.sosGame.cells[occRow][occCol].config.assert_called_with(
            text='O', fg='Red', state='disabled', disabledforeground='Red',
            relief='sunken', font=('Arial', 14, 'bold')
        )


class testSimpleSOSGame(unittest.TestCase):

    def setUp(self):
        """Set up a tkinter root window and game instance before each test"""
        from SOSGame_3 import simpleSOSGame

        self.root = tk.Tk()
        self.root.withdraw()
        self.game = simpleSOSGame(self.root)

        # Set up game conditions
        self.game.dimensions.set('3x3')
        self.game.ruleSet.set('simple')
        self.game.p1Move.set('S')
        self.game.p2Move.set('O')

        # Initialize game state without creating a UI
        dimN = 3
        self.game.cells = [[Mock() for _ in range(dimN)] for _ in range(dimN)]

        # Mock cell buttons to avoid GUI operations
        for i in range(dimN):
            for j in range(dimN):
                self.game.cells[i][j] = Mock()
                self.game.cells[i][j].config = Mock()

        # Mock GUI Methods
        self.game.drawSOSChain = Mock()
        self.end_game_mock = Mock()
        self.game.endGame = self.end_game_mock

        # Initialize game array
        self.game.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]
        self.game.cellOwner = [[None for _ in range(dimN)] for _ in range(dimN)]

        # Set initial game state
        self.game.activeGame = True
        self.game.currentPlayer = 0
        for player in self.game.players:
            player.score = 0

    def tearDown(self):
        """Destroy windows after tests"""
        self.root.destroy()

    def testAC7_1RedPlayerCreatesValidSOSChainWithS(self):
        """Test that when the Red Player completed a valid SOS chain by placing an S character, the game ends and the
        red player wins"""

        self.game.cellState = [
            ['S', '', ''],
            ['O', '', ''],
            ['', '', '']
        ]

        self.game.cellOwner = [
            [0, None, None],
            [0, None, None],
            [None, None, None]
        ]

        # Simulate Red making winning move with an S character placed
        row, col = 2, 0
        moveChar = 'S'
        color = 'Red'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify game ended
        self.assertEqual(self.end_game_mock.call_count, 1)

        # Verify that red won
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            self.assertIn('Player 1 wins!', message)

        # Verify that red had their score incremented
        self.assertEqual(self.game.players[0].score, 1)

    def testAC7_1RedPlayerCreatesValidSOSChainWithO(self):
        """Test that when the Red Player completed a valid SOS chain by placing an S character, the game ends and the
        red player wins"""

        self.game.cellState = [
            ['S', '', ''],
            ['', '', ''],
            ['S', '', '']
        ]

        self.game.cellOwner = [
            [0, None, None],
            [None, None, None],
            [0, None, None]
        ]

        # Simulate Red making winning move with an S character placed
        row, col = 1, 0
        moveChar = 'O'
        color = 'Red'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify game ended
        self.assertEqual(self.end_game_mock.call_count, 1)

        # Verify that red won
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            self.assertIn('Player 1 wins!', message)

        # Verify that red had their score incremented
        self.assertEqual(self.game.players[0].score, 1)

    def testAC7_2BluePlayerCreatesValidSOSChainWithS(self):
        """Test that when the Blue Player completed a valid SOS chain by placing an S character, the game ends and the
        Blue player wins"""

        self.game.cellState = [
            ['S', '', ''],
            ['O', '', ''],
            ['', '', '']
        ]

        self.game.cellOwner = [
            [1, None, None],
            [1, None, None],
            [None, None, None]
        ]

        # Ensure it is blues turn
        self.game.currentPlayer = 1
        self.end_game_mock.call_count = 0
        self.game.players[1].score = 0

        # Simulate Red making winning move with an S character placed
        row, col = 2, 0
        moveChar = 'S'
        color = 'Blue'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify game ended
        self.assertEqual(self.end_game_mock.call_count, 1)

        # Verify that red won
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            self.assertIn('Player 2 wins!', message)

        # Verify that red had their score incremented
        self.assertEqual(self.game.players[1].score, 1)

    def testAC7_2BluePlayerCreatesValidSOSChainWithO(self):
        """Test that when the Blue Player completed a valid SOS chain by placing an S character, the game ends and the
        Blue player wins"""

        self.game.cellState = [
            ['S', '', ''],
            ['', '', ''],
            ['S', '', '']
        ]

        self.game.cellOwner = [
            [1, None, None],
            [None, None, None],
            [1, None, None]
        ]

        # Ensure it is blues turn
        self.game.currentPlayer = 1
        self.end_game_mock.call_count = 0
        self.game.players[1].score = 0

        # Simulate Red making winning move with an S character placed
        row, col = 1, 0
        moveChar = 'O'
        color = 'Blue'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify game ended
        self.assertEqual(self.end_game_mock.call_count, 1)

        # Verify that red won
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            self.assertIn('Player 2 wins!', message)

        # Verify that red had their score incremented
        self.assertEqual(self.game.players[1].score, 1)

    def testAC7_3NeitherPlayerHasMadeAnSOSAndNoMovesLeft(self):

        """This unit test will verify that when no SOS is formed and the board is full, the game ends in a draw"""
        # Set up a nearly full board with no SOS opportunities
        self.game.cellState = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['S', 'O', '']
        ]

        self.game.cellOwner = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, None]
        ]

        # Set up player turn conditions
        self.game.currentPlayer = 0
        self.game.activeGame = True
        self.end_game_mock.call_count = 0

        row, col = 2, 2
        moveChar = 'S'
        color = 'Red'

        # Make this move
        self.game.makeAMove(row, col, moveChar, color)

        self.assertEqual(self.end_game_mock.call_count, 1)

        # Verify neither player scored
        self.assertEqual(self.game.players[0].score, 0)
        self.assertEqual(self.game.players[1].score, 0)

        # Verify game was called as a draw
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ''
            self.assertIn('draw', message.lower())


class testGeneralSOSGame(unittest.TestCase):
    def setUp(self):
        """Set up a tkinter root window and general game instance before each test"""
        from SOSGame_3 import generalSOSGame
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window

        # Create the general game instance
        self.game = generalSOSGame(self.root)

        # Set up common game conditions for general game
        self.game.dimensions.set('3x3')
        self.game.ruleSet.set('general')
        self.game.p1Move.set('S')
        self.game.p2Move.set('O')

        # Initialize minimal game state without full UI
        dimN = 3
        self.game.cells = [[Mock() for _ in range(dimN)] for _ in range(dimN)]

        # Mock the individual cell buttons
        for i in range(dimN):
            for j in range(dimN):
                self.game.cells[i][j] = Mock()
                self.game.cells[i][j].config = Mock()

        # Mock GUI methods
        self.game.drawSOSChain = Mock()
        self.end_game_mock = Mock()
        self.game.endGame = self.end_game_mock

        # Initialize game arrays
        self.game.cellState = [['' for _ in range(dimN)] for _ in range(dimN)]
        self.game.cellOwner = [[None for _ in range(dimN)] for _ in range(dimN)]

        # Set initial game state
        self.game.activeGame = True
        self.game.currentPlayer = 0  # Start with Red Player
        for player in self.game.players:
            player.score = 0

    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()

    def testAC8_9RedPlayerScoresSOSAndPlayContinuesInGeneralGame(self):
        # Set up initial board state with SOS opportunity
        self.game.cellState = [
            ['S', '', ''],
            ['', '', ''],
            ['S', '', '']
        ]
        self.game.cellOwner = [
            [0, None, None],
            [None, None, None],
            [0, None, None]
        ]

        # Reset mocks for this test
        self.end_game_mock.call_count = 0

        # Red Player makes move that completes SOS chain
        row, col = 1, 0  # Place O in the middle to complete vertical S-O-S
        moveChar = 'O'
        color = 'Red'

        self.game.makeAMove(row, col, moveChar, color)

        # Verify Red Player has one point added to their score
        self.assertEqual(self.game.players[0].score, 1,
                         "Red Player should have 1 point after completing SOS")

        # Verify Blue Player's score remains unchanged
        self.assertEqual(self.game.players[1].score, 0,
                         "Blue Player should still have 0 points")

        # Verify It changed to Blue Player's turn
        self.assertEqual(self.game.currentPlayer, 1,
                         "Current player should be Blue Player (1) after Red scores")

        # Verify Game is still active (not ended)
        self.assertTrue(self.game.activeGame,
                        "Game should still be active in general game after single SOS")

        # Verify endGame was NOT called (game continues)
        self.assertEqual(self.end_game_mock.call_count, 0,
                         "endGame should not be called in general game for single SOS")

    def testAC8_10BluePlayerScoresSOSAndPlayContinuesInGeneralGame(self):
        # Set up initial board state with SOS opportunity
        self.game.cellState = [
            ['S', '', ''],
            ['', '', ''],
            ['S', '', '']
        ]
        self.game.cellOwner = [
            [1, None, None],
            [None, None, None],
            [1, None, None]
        ]

        # Ensure it is blues turn
        self.game.currentPlayer = 1
        self.end_game_mock.call_count = 0
        self.game.players[1].score = 0

        # Red Player makes move that completes SOS chain
        row, col = 1, 0  # Place O in the middle to complete vertical S-O-S
        moveChar = 'O'
        color = 'Blue'

        self.game.makeAMove(row, col, moveChar, color)

        # Verify Blue Player has one point added to their score
        self.assertEqual(self.game.players[1].score, 1,
                         "Blue Player should have 1 point after completing SOS")

        # Verify Red Player's score remains unchanged
        self.assertEqual(self.game.players[0].score, 0,
                         "Red Player should still have 0 points")

        # Verify It changed to Red Player's turn
        self.assertEqual(self.game.currentPlayer, 0,
                         "Current player should be Red Player (0) after Blue scores")

        # Verify Game is still active (not ended)
        self.assertTrue(self.game.activeGame,
                        "Game should still be active in general game after single SOS")

        # Verify endGame was NOT called (game continues)
        self.assertEqual(self.end_game_mock.call_count, 0,
                         "endGame should not be called in general game for single SOS")

    def testAC10_1RedWinsWhenRedPlayerHasMoreSOSCompleteWhenNoMovesLeft(self):
        """Test that when Red Player has a higher score and no moves remain, Red wins the general game"""

        # Set up a nearly full board where Red has higher score
        self.game.cellState = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['S', 'O', '']
        ]

        self.game.cellOwner = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, None]
        ]

        # Set initial scores - Red has higher score
        self.game.players[0].score = 3  # Red Player
        self.game.players[1].score = 2  # Blue Player

        # Make sure it's a player's turn and game is active
        self.game.currentPlayer = 0  # Red Player's turn
        self.game.activeGame = True
        self.end_game_mock.call_count = 0

        # Make the move - this should fill the last cell and trigger game end
        row, col = 2, 2
        moveChar = 'S'
        color = 'Red'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify Game ended (endGame was called)
        self.assertEqual(self.end_game_mock.call_count, 1,
                         "endGame should be called when board is full in general game")

        # Verify Red Player wins with correct message
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            print(f"End game message: {message}")
            self.assertIn('Player 1 wins', message,
                          "Win message should indicate Player 1 (Red) won")
            self.assertIn('score of 3', message,
                          "Win message should show Red Player's score of 3")

        # Verify Scores remain unchanged (no new SOS created)
        self.assertEqual(self.game.players[0].score, 3,
                         "Red Player score should remain 3")
        self.assertEqual(self.game.players[1].score, 2,
                         "Blue Player score should remain 2")

    def testAC10_2BlueWinsWhenBluePlayerHasMoreSOSCompleteWhenNoMovesLeft(self):
        """Test that when Blue Player has a higher score and no moves remain, Blue wins the general game"""

        # Set up a nearly full board where Red has higher score
        self.game.cellState = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['S', 'O', '']
        ]

        self.game.cellOwner = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, None]
        ]

        # Set initial scores - Red has higher score
        self.game.players[0].score = 2  # Red Player
        self.game.players[1].score = 3  # Blue Player

        # Make sure it's a player's turn and game is active
        self.game.currentPlayer = 0
        self.game.activeGame = True
        self.end_game_mock.call_count = 0

        # Make the move - this should fill the last cell and trigger game end
        row, col = 2, 2
        moveChar = 'S'
        color = 'Red'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify Game ended (endGame was called)
        self.assertEqual(self.end_game_mock.call_count, 1,
                         "endGame should be called when board is full in general game")

        # Verify Red Player wins with correct message
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            print(f"End game message: {message}")
            self.assertIn('Player 2 wins', message,
                          "Win message should indicate Player 2 (Blue) won")
            self.assertIn('score of 3', message,
                          "Win message should show Blue Player's score of 3")

        # Verify Scores remain unchanged (no new SOS created)
        self.assertEqual(self.game.players[0].score, 2,
                         "Red Player score should remain 2")
        self.assertEqual(self.game.players[1].score, 3,
                         "Blue Player score should remain 3")

    def testAC10_3NeitherPlayerHasMoreSOSCompleteWhenNoMovesLeft(self):
        # Set up a nearly full board where Blue has higher score
        self.game.cellState = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['S', 'O', '']
        ]

        self.game.cellOwner = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, None]
        ]

        # Set initial scores - Red has higher score
        self.game.players[0].score = 2  # Red Player
        self.game.players[1].score = 3  # Blue Player

        # Make sure it's a player's turn and game is active
        self.game.currentPlayer = 0
        self.game.activeGame = True
        self.end_game_mock.call_count = 0

        # Make the move - this should fill the last cell and trigger game end
        row, col = 2, 2
        moveChar = 'S'
        color = 'Red'

        # Make the move
        self.game.makeAMove(row, col, moveChar, color)

        # Verify Game ended (endGame was called)
        self.assertEqual(self.end_game_mock.call_count, 1,
                         "endGame should be called when board is full in general game")

        # Verify No one wins with correct message
        if self.end_game_mock.called:
            callArgs = self.end_game_mock.call_args[0]
            message = callArgs[0] if callArgs else ""
            print(f"End game message: {message}")
            self.assertIn('tie', message.lower(),
                          "Draw message should indicate a tie")
            self.assertIn('both', message.lower(),
                          "Draw message should mention both players")
            self.assertIn('3', message,
                          "Draw message should show the tied score of 3")

        # Verify Scores remain unchanged (no new SOS created)
        self.assertEqual(self.game.players[0].score, 3,
                         "Red Player score should be 3")
        self.assertEqual(self.game.players[1].score, 3,
                         "Blue Player score should remain 3")


if __name__ == '__main__':
    unittest.main()
