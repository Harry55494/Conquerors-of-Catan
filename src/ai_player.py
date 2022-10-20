from player import *

class ai_player(player):

    def __init__(self, number, colour):
        """
        Initialises an ai_player object.
        AI players inheirt from the player class, but have different methods for calculating their moves
        :param number: The player number
        :param colour: The colour of the player
        """
        super().__init__(number=number, colour=colour, human_or_ai='AI')
