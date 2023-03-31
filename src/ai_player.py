"""
AI Player Interface Class

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

import os
import sys

import logging

from src.player import *


class ai_player(player):
    """
    AI Player Interface Class
    Implements the player class, but has methods for discovering moves.
    Is inherited by other AI Player classes, each with their own strategy for calculating moves
    """

    class notImplementedError(Exception):
        """
        Exception raised when a function is not implemented in the child class
        Lists what the function is and what class it is not implemented in
        """

        def __init__(self, function):
            self.function = function
            self.message = f'Function {function} not implemented in {sys._getframe(1).f_locals["self"].__class__.__name__}'
            super().__init__(self.message)
            raise self

    def __init__(self, number, colour, strategy: str = "random"):
        """
        Initialises an ai_player object.
        AI players inherit from the player class, but have different methods for calculating their moves
        Also sets up a logger for the ai player
        :param number: The player number
        :param colour: The colour of the player
        :param strategy: The strategy that the ai player will use to calculate moves
        """

        # Prevent direct instantiation of ai_player
        if self.__class__ is ai_player:
            raise TypeError("ai_player cannot be instantiated directly")

        # Call the parent class constructor
        super().__init__(number=number, colour=colour)

        self.strategy = strategy

        # Setup logging

        self.file_path = f"player_{self.number}-{self.strategy}.log"

        # Delete the file if it already exists
        if os.path.exists(f"logs/players/{self.file_path}"):
            os.remove(f"logs/players/{self.file_path}")
        with open(f"logs/players/{self.file_path}", "w"):
            pass

        # Setup the logger, setting the minimum level to debug, and specifying the format of the log
        self.logger = logging.getLogger(f"{self.file_path}")
        self.logger.setLevel(logging.DEBUG)
        file_format = logging.Formatter("[%(asctime)s] %(message)s")
        fh = logging.FileHandler(f"logs/players/{self.file_path}")
        fh.setFormatter(file_format)
        self.logger.addHandler(fh)

        # Log the initialisation of the player
        self.logger.debug(f"{self.strategy} Initialised - Player " + str(number))

        # List of all moves made by the player
        self.entire_game_moves = []

    def log(self, action):
        """
        Logs an action to the file
        :param action: The action to log
        :return: None
        """
        if "Beginning minimax search on turn" in action:
            self.logger.debug("\n")
        self.logger.debug(f"{action}")

    def dump_moves(self):
        """
        Dumps the entire game moves to a file
        :return: None
        """
        self.log("\n\n")
        self.log("Entire game moves:")
        for move in self.entire_game_moves:
            self.log(move)

    def __str__(self):
        """
        Overrides the str method
        :return: The name of the player, with the colour of the player
        """
        return f"{self.coloured_name}  (AI - {self.strategy.capitalize()})"

    # The methods below raise an error if the function is not implemented in the child class
    # This is to ensure that all AI players have the same methods, and that they are all implemented

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

    def respond_to_trade(self, original_player, receiving, giving):
        raise self.notImplementedError("respond_to_trade")

    def trade_with_port(self, interface):
        raise self.notImplementedError("trade_with_port")

    def play_development_card(self, interface):
        raise self.notImplementedError("play_development_card")

    def turn_actions(self, interface):
        raise self.notImplementedError("turn_actions")
