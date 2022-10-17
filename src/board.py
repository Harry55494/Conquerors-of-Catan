import os
import random

from player import *
from tile import tile


def roll_dice():
    """
    Rolls the dice.
    Statistical distribution of dice rolls is maintained by combining two random numbers between 1 and 6
    :return: Dice roll result
    """
    return random.randint(1, 6) + random.randint(1, 6)


# noinspection DuplicatedCode
class board:
    class setupError(Exception):
        pass

    # Board Setup ---------------------------------------------------------------

    def __init__(self, players: list[player], board_type='default'):
        """
        Initialises the board.
        :param players: The list of players to be added to the board
        :param board_type: The board layout, either the default layout, or a randomised layout
        """

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

        # Buildings map contains a grid reference, the building type, and the player who owns it. Also contains the tile type, so that the resources to
        # give can be calculated
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

    # Setting up Board

    def place_settlement(self, player_: player, type_="settlement"):
        """
        Places a settlement on the board for a player
        :param player_: The player who owns the building
        :param type_: The type of building to place
        :return: The location of the building
        """
        self.print_board(print_letters=True)
        accepted = False
        while not accepted:
            location = input(f"{player_} , where would you like to place your {type_}? "
                             f"\nPlease enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners"
                             f"\n(Single corner numbers increase as you move clockwise around a tile)\n")
            location = location.lower()
            letters = location.split(',')
            letters = [letter.strip() for letter in letters]
            letters.sort()
            location = ','.join(letters)
            if location in self.buildings:
                if self.buildings[location]['player'] is None:
                    self.buildings[location].update({'player': player_, 'building': type_})
                    accepted = True
                    print(f"{player_} has placed a {type_} at {location}")
                else:
                    print("That location is already occupied!")
            else:
                print("That is not a valid location!")
        return location

    def place_road(self, player_: player, requirement=None):
        """
        Places a road on the board for a player
        :param requirement: Optional, a forced location for one end of the road
        :param player_: The player who owns the road
        :return: None
        """
        self.print_board(print_letters=True)
        accepted = False
        while not accepted:
            coordinates = []
            if requirement is not None:
                coordinates.append(requirement)
            while len(coordinates) < 2:
                print(f"{player_} , where would you like to place your road?\n"
                      f"Please enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners")
                print(f"{player_}, you must place your road next to {requirement}")
                location = input(f"Please enter the {len(coordinates) + 1}{'st' if len(coordinates) + 1 == 1 else 'nd'} location\n")
                location = location.lower()
                letters = location.split(',')
                letters = [letter.strip() for letter in letters]
                letters.sort()
                location = ','.join(letters)
                coordinates.append(location)
            if tuple(coordinates) not in self.roads:
                coordinates = coordinates[::-1]
            coordinates = tuple(coordinates)
            if coordinates in self.roads:
                if self.roads[coordinates]['player'] is None:
                    self.roads[coordinates].update({'player': player_})
                    accepted = True
                    print(f"{player_} has placed a road at {coordinates}")
                else:
                    print("That location is already occupied!")

    # Moving Cards --------------------------------------------------------------

    def give_player_card(self, player_: player, card_type: str, card: str, amount=1):
        """
        Gives a player a card from the bank
        :param player_: The player to be given the card
        :param card_type: The card type to be given - resource or development
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :param amount: The amount to be given
        :return: None
        """
        if card_type == 'resource' and not card == 'desert':
            for i in range(amount):
                player_.resources.append(self.resource_deck.pop(self.resource_deck.index(card)))
            print(f'{player_} has been given {amount}x {card} card(s)')
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
            print(f'{player_} has returned a {card}')
            print(f'There are now {len(self.resource_deck)} cards left in the resource deck')
        elif card_type == 'development':
            self.development_card_deck.append(player_.development_cards.pop(player_.development_cards.index(card)))
        else:
            print('Invalid card type')

    def move_robber(self, location):
        for tile_ in self.tiles:
            if tile_.contains_robber:
                tile_.contains_robber = False
            if tile_.letter == location:
                tile_.contains_robber = True

    def initial_placement(self, random_ = False):
        """
        Sets up the board for the game, by allowing players to place their initial settlements and roads, and then giving them the required cards
        :return: None
        """
        print('\n -- Board Setup --\n')
        order = [player_ for player_ in self.players]
        rev_order = order.copy()
        rev_order.reverse()
        order = order + rev_order

        if not random_:

            while len(order) > 0:
                player_ = order.pop(0)
                building = self.place_settlement(player_, 'settlement')
                self.place_road(player_, building)
                if len(order) < len(self.players):
                    # Players receive resources from their second settlement
                    tiles_from_settlement = self.buildings[building]['tiles']
                    for tile_ in tiles_from_settlement:
                        self.give_player_card(player_, 'resource', tile_.resource)

        else:
            while len(order) > 0:
                player_ = order.pop(0)
                accepted = False
                while accepted is False:
                    rand_int = random.randint(0, len(self.buildings) - 1)
                    if self.buildings[list(self.buildings.keys())[rand_int]]['player'] is None:
                        accepted = True
                        building = list(self.buildings.keys())[rand_int]
                        self.buildings[building].update({'player': player_, 'building': 'settlement'})
                        potential_roads = []
                        for road in self.roads:
                            if building in road:
                                potential_roads.append(road)

                        accepted_road = False
                        while accepted_road is False:
                            rand_int = random.randint(0, len(potential_roads) - 1)
                            if self.roads[list(self.roads.keys())[rand_int]]['player'] is None:
                                accepted_road = True
                                self.roads[potential_roads[rand_int]].update({'player': player_})
                                if len(order) < len(self.players):
                                    # Players receive resources from their second settlement
                                    tiles_from_settlement = self.buildings[building]['tiles']
                                    for tile_ in tiles_from_settlement:
                                        self.give_player_card(player_, 'resource', tile_.resource)

    # Processing a Roll ---------------------------------------------------------

    def process_roll(self, roll: int, current_player_: player):
        """
        Processes a roll of the dice and performs the necessary board actions
        :param current_player_: The player who rolled the dice
        :param roll: The number from the dice roll
        :return: None
        """
        if roll == 7:
            print("The robber has been rolled")
            for player_ in self.players:
                if len(player_.resources) >= 7:
                    total_to_discard = len(player_.resources) // 2
                    print(f'{player_} has {len(player_.resources)} resources and must discard half')
                    while total_to_discard > 0:
                        print(f'{player_} has {total_to_discard} resources to discard')
                        player_.printHand()
                        card = input('Which card would you like to discard? ')
                        if card in player_.resources:
                            self.return_player_card(player_, 'resource', card)
                            total_to_discard -= 1
                        else:
                            print('Invalid card')

            self.print_board(print_letters=True)
            print(f"{current_player_}, where would you like to move the robber?")
            accepted = False
            while not accepted:
                location = input("Please enter the letter of the tile you would like to move the robber to\n")
                location = location.lower()
                if any([tile_.letter == location for tile_ in self.tiles]):
                    accepted = True
                    self.move_robber(location)
                else:
                    print("Invalid location")
            new_robber_location = [tile_ for tile_ in self.tiles if tile_.contains_robber][0]
            players_to_steal_from = []
            for key in self.buildings:
                value = self.buildings[key]
                if key.find(new_robber_location.letter) != -1:
                    if value['player'] is not None and value['player'] not in players_to_steal_from and value['player'] != current_player_:
                        players_to_steal_from.append(value['player'])

            if len(players_to_steal_from) > 1:
                print("Please select a player to steal from")
                for i in range(len(players_to_steal_from)):
                    print(f"{i + 1} - {players_to_steal_from[i]}")
                accepted = False
                while not accepted:
                    choice = input("Please enter the number of the player you would like to steal from\n")
                    if choice.isdigit() and int(choice) in range(1, len(players_to_steal_from) + 1):
                        accepted = True
                        player_to_steal_from = players_to_steal_from[int(choice) - 1]
                    else:
                        print("Invalid choice")
            elif len(players_to_steal_from) == 1:
                player_to_steal_from = players_to_steal_from[0]
            else:
                player_to_steal_from = None
                print("No players to steal from")

            if player_to_steal_from is not None:
                print(f"{player_} has stolen from {player_to_steal_from}")
                card = player_to_steal_from.resources.pop(random.randint(0, len(player_to_steal_from.resources) - 1))
                self.give_player_card(current_player_, 'resource', card)

        else:
            for player_ in self.players:
                cards_to_give = {}
                for building in self.buildings:
                    if self.buildings[building].get('building') is not None:
                        tiles = self.buildings[building].get('tiles')
                        for building_tile in tiles:
                            if building_tile.dice_number == roll and not building_tile.contains_robber:
                                if self.buildings[building].get('building') == 'settlement' and self.buildings[building].get('player') == player_:
                                    # print(f'Roll of {roll} has been made and {self.buildings[building].get("player")} has a
                                    # {self.buildings[building].get("building")} on {roll}, so receives 1x {building_tile.tile_type}')
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 1
                                    else:
                                        cards_to_give[building_tile.resource] = 1
                                elif self.buildings[building].get('building') == 'city' and self.buildings[building].get('player') == player_:
                                    # print(f'Roll of {roll} has been made and {self.buildings[building].get("player")} has a
                                    # {self.buildings[building].get("building")} on {roll}, so receives 2x {building_tile.tile_type}')
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 2
                                    else:
                                        cards_to_give[building_tile.resource] = 2
                for card in cards_to_give:
                    self.give_player_card(player_, 'resource', card, cards_to_give[card])

    # Printing the Board -------------------------------------------------------

    def print_board(self, print_letters=False):
        """
        Outputs the board to the console
        :return: None
        """

        os.system('clear')

        # *_tp = *_to_print
        # Shorthand to make the code more readable

        t_tp = []  # Tiles to print
        l_tp = []  # Letters to print
        b_tp = {}  # Buildings to print
        r_tp = {}  # Roads to print

        for tile_ in self.tiles:
            # Dice numbers of 6 and 8 are in red, to keep true to the board, as they are the highest frequency numbers
            if tile_.dice_number < 10:
                t_tp.append([f' {(termcolor.colored(tile_.dice_number, "red") if tile_.dice_number in [6, 8] else tile_.dice_number)}',
                             (tile_.symbol + ' ' if tile_.resource != 'desert' else tile_.symbol)])
            else:
                t_tp.append([f'{(termcolor.colored(tile_.dice_number, "red") if tile_.dice_number in [6, 8] else tile_.dice_number)}',
                             tile_.symbol])

        for tile_ in self.tiles:
            # Prints the letter if requested, then the robber symbol if the tile contains the robber
            l_tp.append(termcolor.colored(tile_.letter, 'white')) if print_letters else l_tp.append('♝') if tile_.contains_robber else l_tp.append(' ')

        for building in self.buildings:
            if self.buildings[building].get('building') is not None:
                b_tp[building] = termcolor.colored(('s' if self.buildings[building].get('building') == 'settlement' else 'C'),
                                                   self.buildings[building].get('player').colour)
            elif building in ['d1', 'f2', 'i1', 'k1', 'n2', 'p1']:
                b_tp[building] = '|'
            else:
                b_tp[building] = ' '

        for road in self.roads:
            if self.roads[road].get('player') is not None:
                r_tp[road] = termcolor.colored(self.roads[road].get('symbol'), self.roads[road].get('player').colour)
            else:
                r_tp[road] = self.roads[road].get('symbol')

        # I am aware this absolutely horrendous to try and read. It started simply as just the outlines of hexagons, and very quickly required a lot of
        # moving parts. However, it works, and I won't need to edit it later on. If I have time, I'll come back and make it more readable.
        lines_to_print = [
            f'                               {b_tp.get("a1")} {r_tp[tuple(["a1", "a2"])] * 5} {b_tp.get("a2")}                               ',
            f'                              {r_tp[tuple(["a,b", "a1"])]}        {r_tp[tuple(["a2", "a,c"])]}                             ',
            f'                             {r_tp[tuple(["a,b", "a1"])]}   {t_tp[0][0]}     {r_tp[tuple(["a2", "a,c"])]}                            ',
            f'                    {b_tp.get("b1")} {r_tp[tuple(["a,b", "b1"])] * 5} {b_tp.get("a,b")}      {l_tp[0]}      {b_tp.get("a,c")} {r_tp[tuple(["a,c", "c1"])] * 5} {b_tp.get("c1")}                    ',
            f'                   {r_tp[tuple(["b1", "b,d"])]}         {r_tp[tuple(["a,b,e", "a,b"])]}    {t_tp[0][1]}   {r_tp[tuple(["a,c", "a,c,e"])]}        {r_tp[tuple(["c1", "c,f"])]}                  ',
            f'                  {r_tp[tuple(["b1", "b,d"])]}    {t_tp[1][0]}     {r_tp[tuple(["a,b,e", "a,b"])]}        {r_tp[tuple(["a,c", "a,c,e"])]}   {t_tp[2][0]}     {r_tp[tuple(["c1", "c,f"])]}                 ',
            f'         {b_tp.get("d2")} {r_tp[tuple(["d2", "b,d"])] * 5} {b_tp.get("b,d")}      {l_tp[1]}      {b_tp.get("a,b,e")} {r_tp[tuple(["a,c,e", "a,b,e"])] * 5} {b_tp.get("a,c,e")}      {l_tp[2]}      {b_tp.get("c,f")} {r_tp[tuple(["c,f", "f1"])] * 5} {b_tp.get("f1")}         ',
            f'        {r_tp[tuple(["d1", "d2"])]}         {r_tp[tuple(["b,d", "b,d,g"])]}   {t_tp[1][1]}     {r_tp[tuple(["b,e,g", "a,b,e"])]}         {r_tp[tuple(["c,e,h", "a,c,e"])]}   {t_tp[2][1]}     {r_tp[tuple(["c,f", "c,f,h"])]}         {r_tp[tuple(["f1", "f2"])]}       ',
            f'       {r_tp[tuple(["d1", "d2"])]}    {t_tp[3][0]}     {r_tp[tuple(["b,d", "b,d,g"])]}        {r_tp[tuple(["b,e,g", "a,b,e"])]}    {t_tp[4][0]}     {r_tp[tuple(["c,e,h", "a,c,e"])]}        {r_tp[tuple(["c,f", "c,f,h"])]}    {t_tp[5][0]}     {r_tp[tuple(["f1", "f2"])]}      ',
            f'      {b_tp.get("d1")}      {l_tp[3]}      {b_tp.get("b,d,g")} {r_tp[tuple(["b,d,g", "b,e,g"])] * 5} {b_tp.get("b,e,g")}      {l_tp[4]}      {b_tp.get("c,e,h")} {r_tp[tuple(["c,f,h", "c,e,h"])] * 5} {b_tp.get("c,f,h")}      {l_tp[5]}      {b_tp.get("f2")}      ',
            f'       {r_tp[tuple(["d,i", "d1"])]}   {t_tp[3][1]}     {r_tp[tuple(["b,d,g", "d,g,i"])]}         {r_tp[tuple(["e,g,j", "b,e,g"])]}   {t_tp[4][1]}    {r_tp[tuple(["c,e,h", "e,h,j"])]}         {r_tp[tuple(["f,h,k", "c,f,h"])]}   {t_tp[5][1]}    {r_tp[tuple(["f2", "f,k"])]}       ',
            f'        {r_tp[tuple(["d,i", "d1"])]}        {r_tp[tuple(["b,d,g", "d,g,i"])]}    {t_tp[6][0]}     {r_tp[tuple(["e,g,j", "b,e,g"])]}        {r_tp[tuple(["c,e,h", "e,h,j"])]}    {t_tp[7][0]}     {r_tp[tuple(["f,h,k", "c,f,h"])]}        {r_tp[tuple(["f2", "f,k"])]}        ',
            f'         {b_tp.get("d,i")} {r_tp[tuple(["d,g,i", "d,i"])] * 5} {b_tp.get("d,g,i")}      {l_tp[6]}      {b_tp.get("e,g,j")} {r_tp[tuple(["e,h,j", "e,g,j"])] * 5} {b_tp.get("e,h,j")}      {l_tp[7]}      {b_tp.get("f,h,k")} {r_tp[tuple(["f,k", "f,h,k"])] * 5} {b_tp.get("f,k")}         ',
            f'        {r_tp[tuple(["i1", "d,i"])]}         {r_tp[tuple(["g,i,l", "d,g,i"])]}   {t_tp[6][1]}    {r_tp[tuple(["e,g,j", "g,j,l"])]}         {r_tp[tuple(["h,j,m", "e,h,j"])]}   {t_tp[7][1]}    {r_tp[tuple(["f,h,k", "h,k,m"])]}         {r_tp[tuple(["f,k", "k1"])]}       ',
            f'       {r_tp[tuple(["i1", "d,i"])]}    {t_tp[8][0]}     {r_tp[tuple(["g,i,l", "d,g,i"])]}        {r_tp[tuple(["e,g,j", "g,j,l"])]}    {t_tp[9][0]}     {r_tp[tuple(["h,j,m", "e,h,j"])]}        {r_tp[tuple(["f,h,k", "h,k,m"])]}    {t_tp[10][0]}     {r_tp[tuple(["f,k", "k1"])]}      ',
            f'      {b_tp.get("i1")}      {l_tp[8]}      {b_tp.get("g,i,l")} {r_tp[tuple(["g,j,l", "g,i,l"])] * 5} {b_tp.get("g,j,l")}      {l_tp[9]}      {b_tp.get("h,j,m")} {r_tp[tuple(["h,k,m", "h,j,m"])] * 5} {b_tp.get("h,k,m")}      {l_tp[10]}      {b_tp.get("k1")}      ',
            f'       {r_tp[tuple(["i,n", "i1"])]}   {t_tp[8][1]}    {r_tp[tuple(["g,i,l", "i,l,n"])]}         {r_tp[tuple(["j,l,o", "g,j,l"])]}   {t_tp[9][1]}     {r_tp[tuple(["h,j,m", "j,m,o"])]}         {r_tp[tuple(["k,m,p", "h,k,m"])]}   {t_tp[10][1]}    {r_tp[tuple(["k1", "k,p"])]}       ',
            f'        {r_tp[tuple(["i,n", "i1"])]}        {r_tp[tuple(["g,i,l", "i,l,n"])]}    {t_tp[11][0]}     {r_tp[tuple(["j,l,o", "g,j,l"])]}        {r_tp[tuple(["h,j,m", "j,m,o"])]}    {t_tp[12][0]}     {r_tp[tuple(["k,m,p", "h,k,m"])]}        {r_tp[tuple(["k1", "k,p"])]}        ',
            f'         {b_tp.get("i,n")} {r_tp[tuple(["i,l,n", "i,n"])] * 5} {b_tp.get("i,l,n")}      {l_tp[11]}      {b_tp.get("j,l,o")} {r_tp[tuple(["j,m,o", "j,l,o"])] * 5} {b_tp.get("j,m,o")}      {l_tp[12]}      {b_tp.get("k,m,p")} {r_tp[tuple(["k,p", "k,m,p"])] * 5} {b_tp.get("k,p")}         ',
            f'        {r_tp[tuple(["n2", "i,n"])]}         {r_tp[tuple(["l,n,q", "i,l,n"])]}   {t_tp[11][1]}    {r_tp[tuple(["j,l,o", "l,o,q"])]}         {r_tp[tuple(["m,o,r", "j,m,o"])]}   {t_tp[12][1]}    {r_tp[tuple(["k,m,p", "m,p,r"])]}         {r_tp[tuple(["k,p", "p1"])]}       ',
            f'       {r_tp[tuple(["n2", "i,n"])]}    {t_tp[13][0]}     {r_tp[tuple(["l,n,q", "i,l,n"])]}        {r_tp[tuple(["j,l,o", "l,o,q"])]}    {t_tp[14][0]}     {r_tp[tuple(["m,o,r", "j,m,o"])]}        {r_tp[tuple(["k,m,p", "m,p,r"])]}    {t_tp[15][0]}     {r_tp[tuple(["k,p", "p1"])]}      ',
            f'      {b_tp.get("n2")}      {l_tp[13]}      {b_tp.get("l,n,q")} {r_tp[tuple(["l,o,q", "l,n,q"])] * 5} {b_tp.get("l,o,q")}      {l_tp[14]}      {b_tp.get("m,o,r")} {r_tp[tuple(["m,p,r", "m,o,r"])] * 5} {b_tp.get("m,p,r")}      {l_tp[15]}      {b_tp.get("p1")}      ',
            f'       {r_tp[tuple(["n1", "n2"])]}   {t_tp[13][1]}    {r_tp[tuple(["l,n,q", "n,q"])]}         {r_tp[tuple(["o,q,s", "l,o,q"])]}   {t_tp[14][1]}     {r_tp[tuple(["m,o,r", "o,r,s"])]}         {r_tp[tuple(["p,r", "m,p,r"])]}   {t_tp[15][1]}    {r_tp[tuple(["p1", "p2"])]}       ',
            f'        {r_tp[tuple(["n1", "n2"])]}        {r_tp[tuple(["l,n,q", "n,q"])]}    {t_tp[16][0]}     {r_tp[tuple(["o,q,s", "l,o,q"])]}        {r_tp[tuple(["m,o,r", "o,r,s"])]}    {t_tp[17][0]}     {r_tp[tuple(["p,r", "m,p,r"])]}        {r_tp[tuple(["p1", "p2"])]}        ',
            f'         {b_tp.get("n1")} {r_tp[tuple(["n,q", "n1"])] * 5} {b_tp.get("n,q")}      {l_tp[16]}      {b_tp.get("o,q,s")} {r_tp[tuple(["o,r,s", "o,q,s"])] * 5} {b_tp.get("o,r,s")}      {l_tp[17]}      {b_tp.get("p,r")} {r_tp[tuple(["p2", "p,r"])] * 5} {b_tp.get("p2")}         ',
            f'                  {r_tp[tuple(["q1", "n,q"])]}   {t_tp[16][1]}    {r_tp[tuple(["o,q,s", "q,s"])]}         {r_tp[tuple(["r,s", "o,r,s"])]}    {t_tp[17][1]}   {r_tp[tuple(["p1", "p2"])]}                  ',
            f'                   {r_tp[tuple(["q1", "n,q"])]}        {r_tp[tuple(["o,q,s", "q,s"])]}    {t_tp[18][0]}     {r_tp[tuple(["r,s", "o,r,s"])]}        {r_tp[tuple(["p1", "p2"])]}                   ',
            f'                    {b_tp.get("q1")} {r_tp[tuple(["q,s", "q1"])] * 5} {b_tp.get("q,s")}      {l_tp[18]}      {b_tp.get("r,s")} {r_tp[tuple(["r1", "r,s"])] * 5} {b_tp.get("r1")}                    ',
            f'                             {r_tp[tuple(["s2", "q,s"])]}   {t_tp[18][1]}    {r_tp[tuple(["r,s", "s1"])]}                             ',
            f'                              {r_tp[tuple(["s2", "q,s"])]}        {r_tp[tuple(["r,s", "s1"])]}                              ',
            f'                               {b_tp.get("s2")} {r_tp[tuple(["s1", "s2"])] * 5} {b_tp.get("s1")}                               ',
        ]

        line_length = 71
        terminal_width = os.get_terminal_size().columns

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
            text = f'{player_} ({player_.type})'.ljust(25)
            print(f'     {text}   |  VP: {player_.victory_points}'.center(terminal_width))
        print('\n')
