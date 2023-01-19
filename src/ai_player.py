import sys

import logging

from src.player import player


class ai_player(player):
    """
    AI Player Interface Class
    Implements the player class, but has methods for discovering moves.
    Is inherited by other AI Player classes, each with their own strategy for calculating moves
    """

    class notImplementedError(Exception):
        def __init__(self, function):
            self.function = function
            self.message = f'Function {function} not implemented in {sys._getframe(1).f_locals["self"].__class__.__name__}'
            super().__init__(self.message)
            raise self

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

        self.file_path = f"player_{self.number}-{self.strategy}.log"

        with open(f"logs/players/{self.file_path}", "w") as f:
            pass

        self.logger = logging.getLogger(f"{self.file_path}")
        self.logger.setLevel(logging.DEBUG)
        file_format = logging.Formatter("[%(asctime)s] %(message)s")
        fh = logging.FileHandler(f"logs/players/{self.file_path}")
        fh.setFormatter(file_format)
        self.logger.addHandler(fh)
        self.logger.debug(f"{self.strategy} Initialised - Player " + str(number))

        self.entire_game_moves = []

    def log_action(self, action):
        if "Beginning minimax search on turn" in action:
            self.logger.debug("\n")
        self.logger.debug(f"{action}")

    def dump_moves(self):
        self.log_action("\n\n")
        self.log_action("Entire game moves:")
        for move in self.entire_game_moves:
            self.log_action(move)

    def __str__(self):
        return f"{self.coloured_name}  (AI - {self.strategy.capitalize()})"

    # Raise an error if the function is not implemented in the child class

    def choose_placement_location(self, interface, type_="settlement"):
        raise self.notImplementedError("choose_placement_location")

    def choose_road_location(self, interface):
        raise self.notImplementedError("choose_road_location")

    def initial_placement(self, interface):
        raise self.notImplementedError("initial_placement")

    def robber(self, interface):
        raise self.notImplementedError("robber")

    def robber_discard(self, interface):
        raise self.notImplementedError("robber_discard")

    def play_development_card(self, interface):
        raise self.notImplementedError("play_development_card")

    def turn_actions(self, interface):
        raise self.notImplementedError("turn_actions")
