from player import *


class ai_player(player):
    """
    AI Player Interface Class
    Implements the player class, but has methods for discovering moves.
    Is inherited by other AI Player classes, each with their own strategy for calculating moves
    """

    def __init__(self, number, colour, strategy: str = "random"):
        """
        Initialises an ai_player object.
        AI players inherit from the player class, but have different methods for calculating their moves
        :param number: The player number
        :param colour: The colour of the player
        """

        if self.__class__ is ai_player:
            raise TypeError("ai_player cannot be instantiated directly")

        super().__init__(number=number, colour=colour)
        self.strategy = strategy

    def __str__(self):
        return f"{self.coloured_name}  (AI - {self.strategy.capitalize()})"
