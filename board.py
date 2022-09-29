import os
import random

from player import *
from tile import tile


def roll_dice():
    # Statistical distribution of dice rolls is maintained by combining two random numbers between 1 and 6
    return random.randint(1, 6) + random.randint(1, 6)


# noinspection DuplicatedCode
class board:

    class setupError(Exception):
        pass

    # Board Setup ---------------------------------------------------------------

    def __init__(self, players: list[player] = None, board_type='default'):
        """
        Initialises the board
        :param players: The list of players to be added to the board
        :param board_type: The board layout, either the default layout, or a randomised layout
        """
        if players is None:
            self.players = []
        self.players = players

        # Player Checking
        if len(self.players) < 2:
            raise self.setupError('There must be at least 2 players')
        player_nums = [player_.number for player_ in self.players]
        player_colours = [player_.colour for player_ in self.players]
        if len(player_nums) != len(set(player_nums)):
            raise self.setupError('Player numbers must be unique')
        if len(player_colours) != len(set(player_colours)):
            raise self.setupError('Player colours must be unique')

        self.resource_deck = []
        self.development_card_deck = []
        self.tiles = [tile(9, 'a', 'wheat'),
                      tile(12, 'b', 'sheep'), tile(10, 'c', 'sheep'),
                      tile(11, 'd', 'wood'), tile(5, 'e', 'clay'), tile(8, 'f', 'wheat'),
                      tile(6, 'g', 'rock'), tile(4, 'h', 'wood'),
                      tile(4, 'i', 'clay'), tile(11, 'j', 'wheat'), tile(3, 'k', 'rock'),
                      tile(3, 'l', 'wood'), tile(9, 'm', 'sheep'),
                      tile(7, 'n', 'desert'), tile(10, 'o', 'sheep'), tile(6, 'p', 'wood'),
                      tile(8, 'q', 'clay'), tile(2, 'r', 'wheat'),
                      tile(5, 's', 'rock')]

        # Buildings map contains a grid reference, the building type, and the player who owns it. Also contains the tile type, so that the resources to give can be calculated
        self.buildings = {
            'a1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a']]},
            'a2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a']]},
            'b1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['b']]},
            'a,b': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a', 'b']]},
            'a,c': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a', 'c']]},
            'c1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['c']]},
            'd2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['d']]},
            'b,d': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['b', 'd']]},
            'a,b,e': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a', 'b', 'c']]},
            'a,c,e': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['a', 'c', 'e']]},
            'c,f': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['c', 'f']]},
            'f1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['f']]},
            'd1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['d']]},
            'b,d,g': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['b', 'd', 'g']]},
            'b,e,g': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['b', 'e', 'g']]},
            'c,e,h': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['c', 'e', 'h']]},
            'c,f,h': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['c', 'f', 'h']]},
            'f2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['f']]},
            'd,i': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['d', 'i']]},
            'd,g,i': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['d', 'g', 'i']]},
            'e,g,j': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['e', 'g', 'j']]},
            'e,h,j': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['e', 'h', 'j']]},
            'f,h,k': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['f', 'h', 'k']]},
            'f,k': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['f', 'k']]},
            'i1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['i']]},
            'g,i,l': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['g', 'i', 'l']]},
            'g,j,l': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['g', 'j', 'l']]},
            'h,j,m': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['h', 'j', 'm']]},
            'h,k,m': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['h', 'k', 'm']]},
            'k1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['k']]},
            'i,n': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['i', 'n']]},
            'i,l,n': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['i', 'l', 'n']]},
            'j,l,o': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['j', 'l', 'o']]},
            'j,m,o': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['j', 'm', 'o']]},
            'k,m,p': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['k', 'm', 'p']]},
            'k,p': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['k', 'p']]},
            'n2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['n']]},
            'l,n,q': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['l', 'n', 'q']]},
            'l,o,q': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['l', 'o', 'q']]},
            'm,o,r': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['m', 'o', 'r']]},
            'm,p,r': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['m', 'p', 'r']]},
            'p1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['p']]},
            'n1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['n']]},
            'n,q': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['n', 'q']]},
            'o,q,s': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['o', 'q', 's']]},
            'o,r,s': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['o', 'r', 's']]},
            'p,r': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['p', 'r']]},
            'p2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['p']]},
            'q1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['q']]},
            'q,s': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['q', 's']]},
            'r,s': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['r', 's']]},
            'r1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['r']]},
            's2': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['s']]},
            's1': {'player': None, 'building': None, 'tiles': [tile_ for tile_ in self.tiles if tile_.letter in ['s']]}
        }

        # Roads map contains the start and end reference, which player owns the road and the symbol that needs to be printed to form the hexagons correctly
        self.roads = {
            # Hex a
            tuple(['a1', 'a2']): {'player': None, 'symbol': r'-'},
            tuple(['a2', 'a,c']): {'player': None, 'symbol': r'\ '},
            tuple(['a,c', 'a,c,e']): {'player': None, 'symbol': r'/ '},
            tuple(['a,c,e', 'a,b,e']): {'player': None, 'symbol': r'-'},
            tuple(['a,b,e', 'a,b']): {'player': None, 'symbol': r'\ '},
            tuple(['a,b', 'a1']): {'player': None, 'symbol': r'/ '},
            # Hex b
            tuple(['a,b', 'b1']): {'player': None, 'symbol': r'-'},
            tuple(['b1', 'b,d']): {'player': None, 'symbol': r'/'},
            tuple(['b,d', 'b,d,g']): {'player': None, 'symbol': r'\ '},
            tuple(['b,d,g', 'b,e,g']): {'player': None, 'symbol': r'-'},
            tuple(['b,e,g', 'a,b,e']): {'player': None, 'symbol': r'/'},
            # Hex c
            tuple(['a,c', 'c1']): {'player': None, 'symbol': r'-'},
            tuple(['c1', 'c,f']): {'player': None, 'symbol': r'\ '},
            tuple(['c,f', 'c,f,h']): {'player': None, 'symbol': r'/'},
            tuple(['c,f,h', 'c,e,h']): {'player': None, 'symbol': r'-'},
            tuple(['c,e,h', 'a,c,e']): {'player': None, 'symbol': r'\ '},
            # Hex d
            tuple(['b,d,g', 'd,g,i']): {'player': None, 'symbol': r'/'},
            tuple(['d,g,i', 'd,i']): {'player': None, 'symbol': r'-'},
            tuple(['d,i', 'd1']): {'player': None, 'symbol': r'\ '},
            tuple(['d1', 'd2']): {'player': None, 'symbol': r'/'},
            tuple(['d2', 'b,d']): {'player': None, 'symbol': r'-'},
            # Hex e
            tuple(['c,e,h', 'e,h,j']): {'player': None, 'symbol': r'/'},
            tuple(['e,h,j', 'e,g,j']): {'player': None, 'symbol': r'-'},
            tuple(['e,g,j', 'b,e,g']): {'player': None, 'symbol': r'\ '},
            # Hex f
            tuple(['c,f', 'f1']): {'player': None, 'symbol': r'-'},
            tuple(['f1', 'f2']): {'player': None, 'symbol': r'\ '},
            tuple(['f2', 'f,k']): {'player': None, 'symbol': r'/'},
            tuple(['f,k', 'f,h,k']): {'player': None, 'symbol': r'-'},
            tuple(['f,h,k', 'c,f,h']): {'player': None, 'symbol': r'\ '},
            # Hex g
            tuple(['e,g,j', 'g,j,l']): {'player': None, 'symbol': r'/'},
            tuple(['g,j,l', 'g,i,l']): {'player': None, 'symbol': r'-'},
            tuple(['g,i,l', 'd,g,i']): {'player': None, 'symbol': r'\ '},
            # Hex h
            tuple(['f,h,k', 'h,k,m']): {'player': None, 'symbol': r'/'},
            tuple(['h,k,m', 'h,j,m']): {'player': None, 'symbol': r'-'},
            tuple(['h,j,m', 'e,h,j']): {'player': None, 'symbol': r'\ '},
            # Hex i
            tuple(['g,i,l', 'i,l,n']): {'player': None, 'symbol': r'/'},
            tuple(['i,l,n', 'i,n']): {'player': None, 'symbol': r'-'},
            tuple(['i,n', 'i1']): {'player': None, 'symbol': r'\ '},
            tuple(['i1', 'd,i']): {'player': None, 'symbol': r'/'},
            # Hex j
            tuple(['h,j,m', 'j,m,o']): {'player': None, 'symbol': r'/'},
            tuple(['j,m,o', 'j,l,o']): {'player': None, 'symbol': r'-'},
            tuple(['j,l,o', 'g,j,l']): {'player': None, 'symbol': r'\ '},
            # Hex k
            tuple(['f,k', 'k1']): {'player': None, 'symbol': r'\ '},
            tuple(['k1', 'k,p']): {'player': None, 'symbol': r'/'},
            tuple(['k,p', 'k,m,p']): {'player': None, 'symbol': r'-'},
            tuple(['k,m,p', 'h,k,m']): {'player': None, 'symbol': r'\ '},
            # Hex l
            tuple(['j,l,o', 'l,o,q']): {'player': None, 'symbol': r'/'},
            tuple(['l,o,q', 'l,n,q']): {'player': None, 'symbol': r'-'},
            tuple(['l,n,q', 'i,l,n']): {'player': None, 'symbol': r'\ '},
            # Hex m
            tuple(['k,m,p', 'm,p,r']): {'player': None, 'symbol': r'/'},
            tuple(['m,p,r', 'm,o,r']): {'player': None, 'symbol': r'-'},
            tuple(['m,o,r', 'j,m,o']): {'player': None, 'symbol': r'\ '},
            # Hex n
            tuple(['l,n,q', 'n,q']): {'player': None, 'symbol': r'/'},
            tuple(['n,q', 'n1']): {'player': None, 'symbol': r'-'},
            tuple(['n1', 'n2']): {'player': None, 'symbol': r'\ '},
            tuple(['n2', 'i,n']): {'player': None, 'symbol': r'/'},
            # Hex o
            tuple(['m,o,r', 'o,r,s']): {'player': None, 'symbol': r'/'},
            tuple(['o,r,s', 'o,q,s']): {'player': None, 'symbol': r'-'},
            tuple(['o,q,s', 'l,o,q']): {'player': None, 'symbol': r'\ '},
            # Hex p
            tuple(['k,p', 'p1']): {'player': None, 'symbol': r'\ '},
            tuple(['p1', 'p2']): {'player': None, 'symbol': r'/'},
            tuple(['p2', 'p,r']): {'player': None, 'symbol': r'-'},
            tuple(['p,r', 'm,p,r']): {'player': None, 'symbol': r'\ '},
            # Hex q
            tuple(['o,q,s', 'q,s']): {'player': None, 'symbol': r'/'},
            tuple(['q,s', 'q1']): {'player': None, 'symbol': r'-'},
            tuple(['q1', 'n,q']): {'player': None, 'symbol': r'\ '},
            # Hex r
            tuple(['p,r', 'r1']): {'player': None, 'symbol': r'/'},
            tuple(['r1', 'r,s']): {'player': None, 'symbol': r'-'},
            tuple(['r,s', 'o,r,s']): {'player': None, 'symbol': r'\ '},
            # Hex s
            tuple(['r,s', 's1']): {'player': None, 'symbol': r'/'},
            tuple(['s1', 's2']): {'player': None, 'symbol': r'-'},
            tuple(['s2', 'q,s']): {'player': None, 'symbol': r'\ '},
        }

        # Create the tiles and board
        if board_type != 'default':

            # If the layout is random, form the tiles from the possible options in the correct order
            self.tiles = []
            potential_tiles = ['wood', 'wood', 'wood', 'wood', 'sheep', 'sheep', 'sheep', 'sheep', 'wheat', 'wheat', 'wheat', 'wheat', 'clay', 'clay', 'clay',
                               'rock', 'rock', 'rock', 'rock', 'desert']
            number_order = [9, 12, 10, 11, 5, 8, 6, 4, 4, 11, 3, 3, 9, 7, 10, 6, 8, 2, 5]
            letter_order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            i = 0
            while len(self.tiles) < 19:
                tile_type = potential_tiles.pop(random.randint(0, len(potential_tiles) - 1))
                if tile_type == 'desert':
                    # Desert tile_ must always have the number 7
                    self.tiles.append(tile(7, (letter_order.pop(0)), tile_type))
                    number_order.pop(number_order.index(7))
                else:
                    self.tiles.append(tile(number_order[i], (letter_order.pop(0)), tile_type))
                    i += 1

        # Add the required cards to their decks

        for i in range(19):
            self.resource_deck.append('wheat')
            self.resource_deck.append('wood')
            self.resource_deck.append('sheep')
            self.resource_deck.append('clay')
            self.resource_deck.append('rock')

        for i in range(14):
            self.development_card_deck.append('soldier')

        for i in range(2):
            self.development_card_deck.append('monopoly')
            self.development_card_deck.append('year of plenty')
            self.development_card_deck.append('road building')

        for i in range(5):
            self.development_card_deck.append('victory point')

        # Shuffle and Sort Decks
        self.resource_deck.sort()
        self.development_card_deck = random.sample(self.development_card_deck, len(self.development_card_deck))

    # Moving Cards --------------------------------------------------------------

    def give_player_card(self, player_, card_type, card, amount=1):
        """
        Gives a player a card from the bank
        :param player_: The player to be given the card
        :param card_type: The card type to be given - resource or development
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :param amount: The amount to be given
        :return: None
        """
        if card_type == 'resource':
            for i in range(amount):
                player_.resources.append(self.resource_deck.pop(self.resource_deck.index(card)))
            print(f'{player_.coloured_name} has been given {amount}x {card} card(s)')
        elif card_type == 'development':
            player_.development_cards.append(self.development_card_deck.pop(self.development_card_deck.index(card)))
        else:
            print('Invalid card type')

    def return_player_card(self, player_: player, card_type, card):
        """
        Returns a card to the bank
        :param player_: The player to take the card from
        :param card_type: The card type to be taken - resource or development
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :return: None
        """
        if card_type == 'resource':
            self.resource_deck.append(player_.resources.pop(player_.resources.index(card)))
            print(f'{player_.coloured_name} has returned a {card}')
            print(f'There are now {len(self.resource_deck)} cards left in the resource deck')
        elif card_type == 'development':
            self.development_card_deck.append(player_.development_cards.pop(player_.development_cards.index(card)))
        else:
            print('Invalid card type')

    # Processing a Roll ---------------------------------------------------------

    def process_roll(self, roll):
        """
        Processes a roll of the dice and performs the necessary board actions
        :param roll: The number from the dice roll
        :return: None
        """
        if roll == 7:
            print("The robber has been rolled")
            for player_ in self.players:
                if len(player_.resources) >= 7:
                    total_to_discard = len(player_.resources) // 2
                    print(f'{player_.coloured_name} has {len(player_.resources)} resources and must discard half')
                    while total_to_discard > 0:
                        print(f'{player_.coloured_name} has {total_to_discard} resources to discard')
                        player_.printHand()
                        card = input('Which card would you like to discard? ')
                        if card in player_.resources:
                            self.return_player_card(player_, 'resource', card)
                            total_to_discard -= 1
                        else:
                            print('Invalid card')
        else:
            for player_ in self.players:
                cards_to_give = {}
                for building in self.buildings:
                    if self.buildings[building].get('building') is not None:
                        tiles = self.buildings[building].get('tiles')
                        for building_tile in tiles:
                            if building_tile.dice_number == roll:
                                if self.buildings[building].get('building') == 'settlement' and self.buildings[building].get('player') == player_:
                                    # print(f'Roll of {roll} has been made and {self.buildings[building].get("player").coloured_name} has a {self.buildings[building].get("building")} on {roll}, so receives 1x {building_tile.tile_type}')
                                    if building_tile.tile_type in cards_to_give:
                                        cards_to_give[building_tile.tile_type] += 1
                                    else:
                                        cards_to_give[building_tile.tile_type] = 1
                                elif self.buildings[building].get('building') == 'city' and self.buildings[building].get('player') == player_:
                                    # print(f'Roll of {roll} has been made and {self.buildings[building].get("player").coloured_name} has a {self.buildings[building].get("building")} on {roll}, so receives 2x {building_tile.tile_type}')
                                    if building_tile.tile_type in cards_to_give:
                                        cards_to_give[building_tile.tile_type] += 2
                                    else:
                                        cards_to_give[building_tile.tile_type] = 2
                for card in cards_to_give:
                    self.give_player_card(player_, 'resource', card, cards_to_give[card])

    # Printing the Board -------------------------------------------------------

    def print_board(self):
        """
        Outputs the board to the console
        :return: None
        """

        tiles_to_print = []
        buildings_to_print = {}
        roads_to_print = {}
        terminal_width = os.get_terminal_size().columns

        for tile_ in self.tiles:
            if tile_.dice_number < 10:
                tiles_to_print.append([f' {termcolor.colored(tile_.dice_number, ("red" if tile_.dice_number in [6, 8] else "white"))}',
                                       (tile_.symbol + ' ' if tile_.tile_type != 'desert' else tile_.symbol)])
            else:
                tiles_to_print.append([f'{termcolor.colored(tile_.dice_number, ("red" if tile_.dice_number in [6, 8] else "white"))}', tile_.symbol])

        for building in self.buildings:
            if self.buildings[building].get('building') is not None:
                buildings_to_print[building] = termcolor.colored(('s' if self.buildings[building].get('building') == 'settlement' else 'C'),
                                                                 self.buildings[building].get('player').colour)
            elif building in ['d1', 'f2', 'i1', 'k1', 'n2', 'p1']:
                buildings_to_print[building] = ' '
            else:
                buildings_to_print[building] = ' '

        for road in self.roads:
            if self.roads[road].get('player') is not None:
                roads_to_print[road] = termcolor.colored(self.roads[road].get('symbol'), self.roads[road].get('player').colour)
            else:
                roads_to_print[road] = self.roads[road].get('symbol')

        # I am aware this absolutely horrendous to try and read. It started simply as just the outlines of hexagons, and very quickly required a lot of moving parts.
        # However, it works, and I won't need to edit it later on. If I have time, I'll come back and make it more readable.
        lines_to_print = [
            f'                               {buildings_to_print.get("a1")} {roads_to_print[tuple(["a1", "a2"])] * 5} {buildings_to_print.get("a2")}                               ',
            f'                              {roads_to_print[tuple(["a,b", "a1"])]}        {roads_to_print[tuple(["a2", "a,c"])]}                             ',
            f'                             {roads_to_print[tuple(["a,b", "a1"])]}   {tiles_to_print[0][0]}     {roads_to_print[tuple(["a2", "a,c"])]}                            ',
            f'                    {buildings_to_print.get("b1")} {roads_to_print[tuple(["a,b", "b1"])] * 5} {buildings_to_print.get("a,b")}             {buildings_to_print.get("a,c")} {roads_to_print[tuple(["a,c", "c1"])] * 5} {buildings_to_print.get("c1")}                    ',
            f'                   {roads_to_print[tuple(["b1", "b,d"])]}         {roads_to_print[tuple(["a,b,e", "a,b"])]}    {tiles_to_print[0][1]}   {roads_to_print[tuple(["a,c", "a,c,e"])]}        {roads_to_print[tuple(["c1", "c,f"])]}                  ',
            f'                  {roads_to_print[tuple(["b1", "b,d"])]}    {tiles_to_print[1][0]}     {roads_to_print[tuple(["a,b,e", "a,b"])]}        {roads_to_print[tuple(["a,c", "a,c,e"])]}   {tiles_to_print[2][0]}     {roads_to_print[tuple(["c1", "c,f"])]}                 ',
            f'         {buildings_to_print.get("d2")} {roads_to_print[tuple(["d2", "b,d"])] * 5} {buildings_to_print.get("b,d")}             {buildings_to_print.get("a,b,e")} {roads_to_print[tuple(["a,c,e", "a,b,e"])] * 5} {buildings_to_print.get("a,c,e")}             {buildings_to_print.get("c,f")} {roads_to_print[tuple(["c,f", "f1"])] * 5} {buildings_to_print.get("f1")}         ',
            f'        {roads_to_print[tuple(["d1", "d2"])]}         {roads_to_print[tuple(["b,d", "b,d,g"])]}   {tiles_to_print[1][1]}     {roads_to_print[tuple(["b,e,g", "a,b,e"])]}         {roads_to_print[tuple(["c,e,h", "a,c,e"])]}   {tiles_to_print[2][1]}     {roads_to_print[tuple(["c,f", "c,f,h"])]}         {roads_to_print[tuple(["f1", "f2"])]}       ',
            f'       {roads_to_print[tuple(["d1", "d2"])]}    {tiles_to_print[3][0]}     {roads_to_print[tuple(["b,d", "b,d,g"])]}        {roads_to_print[tuple(["b,e,g", "a,b,e"])]}    {tiles_to_print[4][0]}     {roads_to_print[tuple(["c,e,h", "a,c,e"])]}        {roads_to_print[tuple(["c,f", "c,f,h"])]}    {tiles_to_print[5][0]}     {roads_to_print[tuple(["f1", "f2"])]}      ',
            f'      {buildings_to_print.get("d1")}             {buildings_to_print.get("b,d,g")} {roads_to_print[tuple(["b,d,g", "b,e,g"])] * 5} {buildings_to_print.get("b,e,g")}             {buildings_to_print.get("c,e,h")} {roads_to_print[tuple(["c,f,h", "c,e,h"])] * 5} {buildings_to_print.get("c,f,h")}             {buildings_to_print.get("f2")}      ',
            f'       {roads_to_print[tuple(["d,i", "d1"])]}   {tiles_to_print[3][1]}     {roads_to_print[tuple(["b,d,g", "d,g,i"])]}         {roads_to_print[tuple(["e,g,j", "b,e,g"])]}   {tiles_to_print[4][1]}    {roads_to_print[tuple(["c,e,h", "e,h,j"])]}         {roads_to_print[tuple(["f,h,k", "c,f,h"])]}   {tiles_to_print[5][1]}    {roads_to_print[tuple(["f2", "f,k"])]}       ',
            f'        {roads_to_print[tuple(["d,i", "d1"])]}        {roads_to_print[tuple(["b,d,g", "d,g,i"])]}    {tiles_to_print[6][0]}     {roads_to_print[tuple(["e,g,j", "b,e,g"])]}        {roads_to_print[tuple(["c,e,h", "e,h,j"])]}    {tiles_to_print[7][0]}     {roads_to_print[tuple(["f,h,k", "c,f,h"])]}        {roads_to_print[tuple(["f2", "f,k"])]}        ',
            f'         {buildings_to_print.get("d,i")} {roads_to_print[tuple(["d,g,i", "d,i"])] * 5} {buildings_to_print.get("d,g,i")}             {buildings_to_print.get("e,g,j")} {roads_to_print[tuple(["e,h,j", "e,g,j"])] * 5} {buildings_to_print.get("e,h,j")}             {buildings_to_print.get("f,h,k")} {roads_to_print[tuple(["f,k", "f,h,k"])] * 5} {buildings_to_print.get("f,k")}         ',
            f'        {roads_to_print[tuple(["i1", "d,i"])]}         {roads_to_print[tuple(["g,i,l", "d,g,i"])]}   {tiles_to_print[6][1]}    {roads_to_print[tuple(["e,g,j", "g,j,l"])]}         {roads_to_print[tuple(["h,j,m", "e,h,j"])]}   {tiles_to_print[7][1]}    {roads_to_print[tuple(["f,h,k", "h,k,m"])]}         {roads_to_print[tuple(["f,k", "k1"])]}       ',
            f'       {roads_to_print[tuple(["i1", "d,i"])]}    {tiles_to_print[8][0]}     {roads_to_print[tuple(["g,i,l", "d,g,i"])]}        {roads_to_print[tuple(["e,g,j", "g,j,l"])]}    {tiles_to_print[9][0]}     {roads_to_print[tuple(["h,j,m", "e,h,j"])]}        {roads_to_print[tuple(["f,h,k", "h,k,m"])]}    {tiles_to_print[10][0]}     {roads_to_print[tuple(["f,k", "k1"])]}      ',
            f'      {buildings_to_print.get("i1")}             {buildings_to_print.get("g,i,l")} {roads_to_print[tuple(["g,j,l", "g,i,l"])] * 5} {buildings_to_print.get("g,j,l")}             {buildings_to_print.get("h,j,m")} {roads_to_print[tuple(["h,k,m", "h,j,m"])] * 5} {buildings_to_print.get("h,k,m")}             {buildings_to_print.get("k1")}      ',
            f'       {roads_to_print[tuple(["i,n", "i1"])]}   {tiles_to_print[8][1]}    {roads_to_print[tuple(["g,i,l", "i,l,n"])]}         {roads_to_print[tuple(["j,l,o", "g,j,l"])]}   {tiles_to_print[9][1]}     {roads_to_print[tuple(["h,j,m", "j,m,o"])]}         {roads_to_print[tuple(["k,m,p", "h,k,m"])]}   {tiles_to_print[10][1]}    {roads_to_print[tuple(["k1", "k,p"])]}       ',
            f'        {roads_to_print[tuple(["i,n", "i1"])]}        {roads_to_print[tuple(["g,i,l", "i,l,n"])]}    {tiles_to_print[11][0]}     {roads_to_print[tuple(["j,l,o", "g,j,l"])]}        {roads_to_print[tuple(["h,j,m", "j,m,o"])]}    {tiles_to_print[12][0]}     {roads_to_print[tuple(["k,m,p", "h,k,m"])]}        {roads_to_print[tuple(["k1", "k,p"])]}        ',
            f'         {buildings_to_print.get("i,n")} {roads_to_print[tuple(["i,l,n", "i,n"])] * 5} {buildings_to_print.get("i,l,n")}             {buildings_to_print.get("j,l,o")} {roads_to_print[tuple(["j,m,o", "j,l,o"])] * 5} {buildings_to_print.get("j,m,o")}             {buildings_to_print.get("k,m,p")} {roads_to_print[tuple(["k,p", "k,m,p"])] * 5} {buildings_to_print.get("k,p")}         ',
            f'        {roads_to_print[tuple(["n2", "i,n"])]}         {roads_to_print[tuple(["l,n,q", "i,l,n"])]}   {tiles_to_print[11][1]}    {roads_to_print[tuple(["j,l,o", "l,o,q"])]}         {roads_to_print[tuple(["m,o,r", "j,m,o"])]}    {tiles_to_print[12][1]}   {roads_to_print[tuple(["k,m,p", "m,p,r"])]}         {roads_to_print[tuple(["k,p", "p1"])]}       ',
            f'       {roads_to_print[tuple(["n2", "i,n"])]}    {tiles_to_print[13][0]}     {roads_to_print[tuple(["l,n,q", "i,l,n"])]}        {roads_to_print[tuple(["j,l,o", "l,o,q"])]}    {tiles_to_print[14][0]}     {roads_to_print[tuple(["m,o,r", "j,m,o"])]}        {roads_to_print[tuple(["k,m,p", "m,p,r"])]}    {tiles_to_print[15][0]}     {roads_to_print[tuple(["k,p", "p1"])]}      ',
            f'      {buildings_to_print.get("n2")}             {buildings_to_print.get("l,n,q")} {roads_to_print[tuple(["l,o,q", "l,n,q"])] * 5} {buildings_to_print.get("l,o,q")}             {buildings_to_print.get("m,o,r")} {roads_to_print[tuple(["m,p,r", "m,o,r"])] * 5} {buildings_to_print.get("m,p,r")}             {buildings_to_print.get("p1")}      ',
            f'       {roads_to_print[tuple(["n1", "n2"])]}   {tiles_to_print[13][1]}    {roads_to_print[tuple(["l,n,q", "n,q"])]}         {roads_to_print[tuple(["o,q,s", "l,o,q"])]}   {tiles_to_print[14][1]}     {roads_to_print[tuple(["m,o,r", "o,r,s"])]}         {roads_to_print[tuple(["p,r", "m,p,r"])]}   {tiles_to_print[15][1]}    {roads_to_print[tuple(["p1", "p2"])]}       ',
            f'        {roads_to_print[tuple(["n1", "n2"])]}        {roads_to_print[tuple(["l,n,q", "n,q"])]}    {tiles_to_print[16][0]}     {roads_to_print[tuple(["o,q,s", "l,o,q"])]}        {roads_to_print[tuple(["m,o,r", "o,r,s"])]}    {tiles_to_print[17][0]}     {roads_to_print[tuple(["p,r", "m,p,r"])]}        {roads_to_print[tuple(["p1", "p2"])]}        ',
            f'         {buildings_to_print.get("n1")} {roads_to_print[tuple(["n,q", "n1"])] * 5} {buildings_to_print.get("n,q")}             {buildings_to_print.get("o,q,s")} {roads_to_print[tuple(["o,r,s", "o,q,s"])] * 5} {buildings_to_print.get("o,r,s")}             {buildings_to_print.get("p,r")} {roads_to_print[tuple(["p2", "p,r"])] * 5} {buildings_to_print.get("p2")}         ',
            f'                  {roads_to_print[tuple(["q1", "n,q"])]}   {tiles_to_print[16][1]}    {roads_to_print[tuple(["o,q,s", "q,s"])]}         {roads_to_print[tuple(["r,s", "o,r,s"])]}    {tiles_to_print[17][1]}   {roads_to_print[tuple(["p1", "p2"])]}                  ',
            f'                   {roads_to_print[tuple(["q1", "n,q"])]}        {roads_to_print[tuple(["o,q,s", "q,s"])]}    {tiles_to_print[18][0]}     {roads_to_print[tuple(["r,s", "o,r,s"])]}        {roads_to_print[tuple(["p1", "p2"])]}                   ',
            f'                    {buildings_to_print.get("q1")} {roads_to_print[tuple(["q,s", "q1"])] * 5} {buildings_to_print.get("q,s")}             {buildings_to_print.get("r,s")} {roads_to_print[tuple(["r1", "r,s"])] * 5} {buildings_to_print.get("r1")}                    ',
            f'                             {roads_to_print[tuple(["s2", "q,s"])]}   {tiles_to_print[18][1]}    {roads_to_print[tuple(["r,s", "s1"])]}                             ',
            f'                              {roads_to_print[tuple(["s2", "q,s"])]}        {roads_to_print[tuple(["r,s", "s1"])]}                              ',
            f'                               {buildings_to_print.get("s2")} {roads_to_print[tuple(["s1", "s2"])] * 5} {buildings_to_print.get("s1")}                               ',

        ]

        line_length = 71
        print('\n')
        print("Conquerors of Catan".center(terminal_width))
        print("\n")
        print(f" {' ' * (int(terminal_width / 2 - 40))}{'-' * (line_length + 8)}")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        for line in lines_to_print:
            print(f"{' ' * int(terminal_width / 2 - 40)}|    {line}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f" {' ' * (int(terminal_width / 2 - 40))}{'-' * (line_length + 8)}")
        print("\n")
        print(f'🌾 🌲 🐑 🧱 🪨    ❔        '.center(terminal_width), end='')
        print(f'Bank has {len(self.resource_deck)} resource cards and {len(self.development_card_deck)} development cards          '.center(terminal_width))
        for player_ in self.players:
            text = f'{player_.coloured_name} ({player_.type})'.ljust(25)
            print(f'     {text}   |  VP: {player_.victory_points}'.center(terminal_width))
