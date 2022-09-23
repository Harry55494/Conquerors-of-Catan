import os
import random

import termcolor

from tile import tile

def roll_dice():
    # Statistical distribution of dice rolls is maintained by combining two random numbers between 1 and 6
    return random.randint(1, 6) + random.randint(1, 6)

# noinspection DuplicatedCode
class board:

    # Board Setup ---------------------------------------------------------------

    def __init__(self, players=None, board_type ='default'):
        if players is None:
            self.players = []
        self.players = players
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

        # Create the tiles and board
        if board_type != 'default':

            # If the layout is random, form the tiles from the possible options in the correct order
            self.tiles = []
            potential_tiles = ['wood', 'wood', 'wood', 'wood', 'sheep', 'sheep', 'sheep', 'sheep', 'wheat', 'wheat', 'wheat', 'wheat', 'clay', 'clay', 'clay', 'rock', 'rock', 'rock', 'rock', 'desert']
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

        for i in range(0, 19):
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
        if card_type == 'resource':
            for i in range(amount):
                player_.resources.append(self.resource_deck.pop(self.resource_deck.index(card)))  # This line
            print(f'{player_.coloured_name} has been given {amount}x {card} card(s)')
        elif card_type == 'development':
            player_.development_cards.append(self.development_card_deck.pop(self.development_card_deck.index(card)))
        else:
            print('Invalid card type')

    def return_player_card(self, player, card_type, card):
        if card_type == 'resource':
            self.resource_deck.append(player.resources.pop(player.resources.index(card)))
            print(f'{player.coloured_name} has returned a {card}')
            print(f'There are now {len(self.resource_deck)} cards left in the resource deck')
        elif card_type == 'development':
            self.development_card_deck.append(player.development_cards.pop(player.development_cards.index(card)))
        else:
            print('Invalid card type')

    # Processing a Roll ---------------------------------------------------------

    def process_roll(self, roll):
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
            for player in self.players:
                cards_to_give = {}
                for building in self.buildings:
                    if self.buildings[building].get('building') is not None:
                        tiles = self.buildings[building].get('tiles')
                        for building_tile in tiles:
                            if building_tile.dice_number == roll:
                                if self.buildings[building].get('building') == 'settlement' and self.buildings[building].get('player') == player:
                                    #print(f'Roll of {roll} has been made and {self.buildings[building].get("player").coloured_name} has a {self.buildings[building].get("building")} on {roll}, so receives 1x {building_tile.tile_type}')
                                    if building_tile.tile_type in cards_to_give:
                                        cards_to_give[building_tile.tile_type] += 1
                                    else:
                                        cards_to_give[building_tile.tile_type] = 1
                                elif self.buildings[building].get('building') == 'city' and self.buildings[building].get('player') == player:
                                    #print(f'Roll of {roll} has been made and {self.buildings[building].get("player").coloured_name} has a {self.buildings[building].get("building")} on {roll}, so receives 2x {building_tile.tile_type}')
                                    if building_tile.tile_type in cards_to_give:
                                        cards_to_give[building_tile.tile_type] += 2
                                    else:
                                        cards_to_give[building_tile.tile_type] = 2
                for card in cards_to_give:
                    self.give_player_card(player, 'resource', card, cards_to_give[card])


    # Printing the Board -------------------------------------------------------

    def print_board(self):
        # Outputs the board to the console

        tiles_to_print = []
        buildings_to_print = {}
        terminal_width = os.get_terminal_size().columns

        for tile in self.tiles:
            if tile.dice_number < 10:
                tiles_to_print.append([f' {termcolor.colored(tile.dice_number, ("red" if tile.dice_number in [6, 8] else "white"))}',(tile.symbol + ' ' if tile.tile_type != 'desert' else tile.symbol)])
            else:
                tiles_to_print.append([f'{termcolor.colored(tile.dice_number, ("red" if tile.dice_number in [6, 8] else "white"))}',tile.symbol])

        for building in self.buildings:
            if self.buildings[building].get('building') is not None:
                buildings_to_print[building] = termcolor.colored(('s' if self.buildings[building].get('building') == 'settlement' else 'C'), self.buildings[building].get('player').colour)
            elif building in ['d1', 'f2', 'i1', 'k1', 'n2', 'p1']:
                buildings_to_print[building] = '|'
            else:
                buildings_to_print[building] = ' '

        lines_to_print = [
            f'                              {buildings_to_print.get("a1")} ------- {buildings_to_print.get("a2")}                              ',
            f'                              /         \                              ',
            f'                             /    {tiles_to_print[0][0]}     \                             ',
            f'                   {buildings_to_print.get("b1")} ------- {buildings_to_print.get("a,b")}           {buildings_to_print.get("a,c")} ------- {buildings_to_print.get("c1")}                   ',
            f'                   /         \     {tiles_to_print[0][1]}   /         \                   ',
            f'                  /    {tiles_to_print[1][0]}     \         /    {tiles_to_print[2][0]}     \                  ',
            f'        {buildings_to_print.get("d2")} ------- {buildings_to_print.get("b,d")}           {buildings_to_print.get("a,b,e")} ------- {buildings_to_print.get("a,c,e")}           {buildings_to_print.get("c,f")} ------- {buildings_to_print.get("f1")}        ',
            f'        /         \    {tiles_to_print[1][1]}     /         \    {tiles_to_print[2][1]}     /         \        ',
            f'       /    {tiles_to_print[3][0]}     \         /    {tiles_to_print[4][0]}     \         /    {tiles_to_print[5][0]}     \       ',
            f'      {buildings_to_print.get("d1")}            {buildings_to_print.get("b,d,g")} ------- {buildings_to_print.get("b,e,g")}           {buildings_to_print.get("c,e,h")} ------- {buildings_to_print.get("c,f,h")}            {buildings_to_print.get("f2")}      ',
            f'       \    {tiles_to_print[3][1]}     /         \    {tiles_to_print[4][1]}    /         \    {tiles_to_print[5][1]}    /       ',
            f'        \         /    {tiles_to_print[6][0]}     \         /    {tiles_to_print[7][0]}     \         /        ',
            f'        {buildings_to_print.get("d,i")} ------- {buildings_to_print.get("d,g,i")}           {buildings_to_print.get("e,g,j")} ------- {buildings_to_print.get("e,h,j")}           {buildings_to_print.get("f,h,k")} ------- {buildings_to_print.get("f,k")}        ',
            f'        /         \    {tiles_to_print[6][1]}    /         \    {tiles_to_print[7][1]}    /         \        ',
            f'       /    {tiles_to_print[8][0]}     \         /    {tiles_to_print[9][0]}     \         /    {tiles_to_print[10][0]}     \       ',
            f'      {buildings_to_print.get("i1")}            {buildings_to_print.get("g,i,l")} ------- {buildings_to_print.get("g,j,l")}           {buildings_to_print.get("h,j,m")} ------- {buildings_to_print.get("h,k,m")}            {buildings_to_print.get("k1")}      ',
            f'       \    {tiles_to_print[8][1]}    /         \    {tiles_to_print[9][1]}     /         \    {tiles_to_print[10][1]}    /       ',
            f'        \         /    {tiles_to_print[11][0]}     \         /    {tiles_to_print[12][0]}     \         /        ',
            f'        {buildings_to_print.get("i,n")} ------- {buildings_to_print.get("i,l,n")}           {buildings_to_print.get("j,l,o")} ------- {buildings_to_print.get("j,m,o")}           {buildings_to_print.get("k,m,p")} ------- {buildings_to_print.get("k,p")}        ',
            f'        /         \    {tiles_to_print[11][1]}    /         \     {tiles_to_print[12][1]}   /         \        ',
            f'       /    {tiles_to_print[13][0]}     \         /    {tiles_to_print[14][0]}     \         /    {tiles_to_print[15][0]}     \       ',
            f'      {buildings_to_print.get("n2")}            {buildings_to_print.get("l,n,q")} ------- {buildings_to_print.get("l,o,q")}           {buildings_to_print.get("m,o,r")} ------- {buildings_to_print.get("m,p,r")}            {buildings_to_print.get("p1")}      ',
            f'       \    {tiles_to_print[13][1]}    /         \    {tiles_to_print[14][1]}     /         \    {tiles_to_print[15][1]}    /       ',
            f'        \         /    {tiles_to_print[16][0]}     \         /    {tiles_to_print[17][0]}     \         /        ',
            f'        {buildings_to_print.get("n1")} ------- {buildings_to_print.get("n,q")}           {buildings_to_print.get("o,q,s")} ------- {buildings_to_print.get("o,r,s")}           {buildings_to_print.get("p,r")} ------- {buildings_to_print.get("p2")}        ',
            f'                  \    {tiles_to_print[16][1]}    /         \     {tiles_to_print[17][1]}   /                  ',
            f'                   \         /    {tiles_to_print[18][0]}     \         /                   ',
            f'                   {buildings_to_print.get("q1")} ------- {buildings_to_print.get("q,s")}           {buildings_to_print.get("r,s")} ------- {buildings_to_print.get("r1")}                   ',
            f'                             \    {tiles_to_print[18][1]}    /                             ',
            f'                              \         /                              ',
            f'                              {buildings_to_print.get("s2")} ------- {buildings_to_print.get("s1")}                              ',

        ]

        line_length = len(lines_to_print[1])
        print('\n')
        print("Conquerors of Catan".center(terminal_width))
        print("\n")
        print(f" {' ' * (int(terminal_width / 2 - 40))}{'-' * (line_length+8)}")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        for line in lines_to_print:
            print(f"{' ' * int(terminal_width / 2 - 40)}|    {line}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f"{' ' * int(terminal_width / 2 - 40)}|    {' ' * line_length}    |")
        print(f" {' ' * (int(terminal_width / 2 - 40))}{'-' * (line_length+8)}")
        print("\n")
        print(f'🌾 🌲 🐑 🧱 🪨    ❔        '.center(terminal_width), end='')
        print(f'Bank has {len(self.resource_deck)} resource cards and {len(self.development_card_deck)} development cards          '.center(terminal_width))
        for player in self.players:
            text = f'{player.coloured_name} ({player.type})'.ljust(25)
            print(f'     {text}  |  VP: {player.victory_points}'.center(terminal_width))

