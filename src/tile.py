
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

        if resource == 'wheat':
            self.symbol = '🌾'
        elif resource == 'wood':
            self.symbol = '🌲'
        elif resource == 'sheep':
            self.symbol = '🐑'
        elif resource == 'clay':
            self.symbol = '🧱'
        elif resource == 'rock':
            self.symbol = '🪨'
        elif resource == 'desert':
            self.symbol = '🏜️'
            self.dice_number = 7
            self.contains_robber = True

    def __str__(self):
        return f'{self.letter}'
