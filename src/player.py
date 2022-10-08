import termcolor


class player:

    def __init__(self, number, colour, type='Human'):
        """
        Initialises a player object
        :param number: The player number
        :param colour: The colour of the player
        :param type: Whether the player is human controlled or not
        """
        self.number = number
        self.colour = colour
        self.name = 'Player ' + str(number)
        self.coloured_name = termcolor.colored(self.name, self.colour)
        self.type = type
        self.victory_points = 0
        self.resources = []
        self.development_cards = []
        print(self.coloured_name, 'has joined the game')

    def printHand(self):
        """
        Prints the player's hand
        :return: None
        """
        self.resources.sort()
        print(f"You ({self.coloured_name}) have {len(self.resources)} resource card(s) in your hand.", end ='')
        if len(self.resources) > 0:
            print(' They are:')
        card_count = {}
        for card in self.resources:
            if card in card_count:
                card_count[card] += 1
            else:
                card_count[card] = 1
        self.resources.sort()
        for card in card_count:
            print(f"{card_count[card]} x {card} ", end=' ')
        print('')

    def calculateVictoryPoints(self, board):
        """
        Calculates the player's victory points, from both their settlements/cities and their development cards
        :param board: The board, so that buildings can be checked
        :return: The player's victory points
        """
        self.victory_points = 0
        for building in board.buildings:
            if board.buildings[building] is not None:
                if board.buildings[building].get('player') == self:
                    if board.buildings[building].get('building') == 'settlement':
                        self.victory_points += 1
                    elif board.buildings[building].get('building') == 'city':
                        self.victory_points += 2
        for card in self.development_cards:
            if card == 'victory point':
                self.victory_points += 1
        return self.victory_points
