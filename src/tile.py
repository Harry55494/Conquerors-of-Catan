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
        return f"{self.letter}"
