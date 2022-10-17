from player import *

class ai_player(player):

    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, type='AI')
