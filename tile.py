
class tile:

    dice_number = 0
    letter = ''
    tile_type = ''
    symbol = ''
    contains_robber = False

    def __init__(self, dice_number, letter, tile_type):
        """
        Initialises a tile object
        :param dice_number: The number that needs to be rolled to get resources from this tile
        :param letter: The unique letter that identifies this tile, for used in the board dictionary
        :param tile_type: The resource gained from rolling this tile
        """
        self.dice_number = dice_number
        self.tile_type = tile_type
        self.letter = letter

        if tile_type == 'wheat':
            self.symbol = '🌾'
        elif tile_type == 'wood':
            self.symbol = '🌲'
        elif tile_type == 'sheep':
            self.symbol = '🐑'
        elif tile_type == 'clay':
            self.symbol = '🧱'
        elif tile_type == 'rock':
            self.symbol = '🪨'
        elif tile_type == 'desert':
            self.symbol = '🏜️'
            self.dice_number = 7
            self.contains_robber = True
