"""
Tile Class File for Board

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""


class tile:
    def __init__(self, dice_number, letter, resource):
        """
        Initialises a tile object
        :param dice_number: The number that needs to be rolled to get resources from this tile
        :param letter: The unique letter that identifies this tile, for used in the board dictionary
        :param resource: The resource gained from rolling this tile
        """
        self.dice_number = dice_number
        self.resource = resource
        self.letter = letter
        self.contains_robber = False

        # Set the symbol for the tile
        if resource == "wheat":
            self.symbol = "🌾"
        elif resource == "wood":
            self.symbol = "🌲"
        elif resource == "sheep":
            self.symbol = "🐑"
        elif resource == "clay":
            self.symbol = "🧱"
        elif resource == "rock":
            self.symbol = "🪨"
        elif resource == "desert":
            self.symbol = "🏜️"
            self.dice_number = 7
            self.contains_robber = True

        # Set the frequency of the tile (the dots on the tile)
        self.frequency = (
            5
            if dice_number == 6 or dice_number == 8
            else 4
            if dice_number == 5 or dice_number == 9
            else 3
            if dice_number == 4 or dice_number == 10
            else 2
            if dice_number == 3 or dice_number == 11
            else 1
            if dice_number == 2 or dice_number == 12
            else 0
        )

    def __str__(self):
        # Override the string representation of the tile, for printing to the console
        return f"{self.letter}"

    def __eq__(self, other):
        try:
            if self.letter != other.letter:
                return False
            if self.dice_number != other.dice_number:
                return False
            if self.resource != other.resource:
                return False
            if self.contains_robber != other.contains_robber:
                return False
            return True
        except:
            return False

    def __hash__(self):
        """
        Override the hash function for the tile
        :return: The hash of the tile
        """
        return hash(self.letter + str(self.dice_number))
