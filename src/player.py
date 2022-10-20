import termcolor


class player:

    def __init__(self, number, colour, human_or_ai='Human'):
        """
        Initialises a player object
        :param number: The player number
        :param colour: The colour of the player
        :param human_or_ai: Whether the player is human controlled or not
        """
        self.number = number
        self.colour = colour
        self.name = 'Player ' + str(number)
        self.coloured_name = termcolor.colored(self.name, self.colour)
        self.human_or_ai = human_or_ai
        self.victory_points = 0
        self.resources = []
        self.development_cards = []
        print(self.coloured_name, 'has joined the game')

    # override print function
    def __str__(self):
        return self.coloured_name

    def printHand(self, type_ = 'resources'):
        """
        Prints the player's hand of either resource cards or development cards
        :return: None
        """
        if type_ in ['resource', 'resources']:
            list_to_print = self.resources
        else:
            list_to_print = self.development_cards
        list_to_print.sort()
        print(f"You ({self.coloured_name}) have {len(list_to_print)} {type_} card(s) in your hand.", end ='')
        if len(list_to_print) > 0:
            print(' They are:')
        card_count = {}
        for card in list_to_print:
            if card in card_count:
                card_count[card] += 1
            else:
                card_count[card] = 1
        for card in card_count:
            print(f"{card_count[card]} x {card} ", end=' ')
        print('')
        self.resources.sort()
        self.development_cards.sort()

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
