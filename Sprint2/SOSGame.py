import GUI_2

class Player:
    """This class represents the player's of the game, and their related data"""

    def __init(self, player_number, player_type="human"): # Later sprints will implement that this can be a computer player
        self.player_number = player_number
        self.player_type = player_type
        self.score = 0
