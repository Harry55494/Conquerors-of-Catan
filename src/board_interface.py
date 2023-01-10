import logging
import sys

from board import *


class boardInterface:
    board: board

    class moveNotValid(Exception):
        def __init__(self, move):
            self.move = move
            self.message = f'The move {move} is not valid'
            super().__init__(self.message)
            sys.exit()

    def __init__(self, players: list[player]):
        """
        Initialises a boardInterface object.
        Object is used to interact with the board object in a standardised way e.g. takes cards from a player
        Acts similarly to a board master
        :param board:
        """
        self.board = board(board_type='default', players=players)
        self.turn_number = 0

        with open('logs/board_actions.log', 'w') as f:
            pass

        self.logger = logging.getLogger('boardInterface')
        self.logger.setLevel(logging.DEBUG)
        file_format = logging.Formatter('[%(asctime)s] %(message)s')
        fh = logging.FileHandler('logs/board_actions.log')
        fh.setFormatter(file_format)
        self.logger.addHandler(fh)
        self.logger.debug("Board Interface created")

    def log_action(self, action):
        self.logger.debug(f"[Turn: {str(self.turn_number).ljust(3)}] {action}")

    # Getters and Setters
    def get_resource_deck(self):
        return self.board.resource_deck

    def get_players_list(self):
        return self.board.players

    def get_tiles_list(self):
        return self.board.tiles

    def get_buildings_list(self):
        return self.board._buildings

    def get_roads_list(self):
        return self.board.roads

    def get_building_cost_list(self):
        return self.board.building_cost_list

    def get_largest_army(self):
        return self.board.largest_army

    def get_longest_road(self):
        return self.board.longest_road

    # Helper Functions

    def print_board(self, print_letters=False) -> None:
        self.board.print_board(print_letters)

    def has_potential_road(self, player_) -> int:
        road_endings = []
        for road in self.board.roads:
            if self.board.roads[road]['player'] == player_:
                road_endings.append(road[0])
                road_endings.append(road[1])
        return len(road_endings) > 0

    def move_robber(self, location):
        for tile_ in self.board.tiles:
            if tile_.contains_robber:
                tile_.contains_robber = False
            if tile_.letter == location:
                tile_.contains_robber = True

    def steal_from_player(self, player_to_steal_from: player, player_to_give_to: player) -> None:
        card = player_to_steal_from.resources.pop(random.randint(0, len(player_to_steal_from.resources) - 1))
        self.give_player_card(player_to_give_to, 'resource', card)

    def count_structure(self, player_, structure):
        count = 0
        if structure == 'road':
            for road in self.get_roads_list():
                if self.get_roads_list()[road]['player'] == player_:
                    count += 1
            return count
        for building in self.get_buildings_list():
            if self.get_buildings_list()[building] == structure:
                count += 1
        return count

    # Moving Cards ----

    def check_for_nearby_settlements(self, position) -> bool:
        """
        Checks if there are any settlements or cities within 1 hex of the given coordinates.
        :param position: The coordinates to check
        :return: True if there are settlements or cities within 1 hex of the given coordinates, False otherwise.
        """
        position_to_check = [position]
        for road, details in self.board.roads.items():
            if position in road:
                position_to_check.append(road[0])
                position_to_check.append(road[1])
        position_to_check = list(set(position_to_check))
        for coord in position_to_check:
            if self.get_buildings_list()[coord]['player'] is not None:
                return True
        return False

    def give_player_card(self, player_: player, card_type: str, card: str, amount=1) -> bool:
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
                try:
                    player_.resources.append(self.board.resource_deck.pop(self.board.resource_deck.index(card)))
                except ValueError:
                    print('Not enough cards in the bank')
            self.log_action(f'{player_.name} was given {amount} {card} from the bank')
        elif card_type == 'development':
            try:
                card_given = self.board.development_card_deck.pop(0)
                player_.development_cards.append(card_given)
                self.log_action(f'{player_.name} was given a {card_given} card from the bank')
                self.log_action(f'{player_.name} now has {len(player_.development_cards)} development cards')
            except IndexError:
                print('Not enough cards in the bank')
                return False
        else:
            print(f'Invalid card type - cannot give player {card}')
            time.sleep(5)

    def return_player_card(self, player_: player, card):
        """
        Returns a card to the bank
        :param player_: The player to take the card from
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :return: None
        """
        if card in ["wheat", "wood", "clay", "sheep", "rock"]:
            self.board.resource_deck.append(player_.resources.pop(player_.resources.index(card)))
            self.log_action(f"{player_.name} returned a {card} card to the bank")
        elif card in ["knight", "victory point", "road building", "year of plenty", "monopoly"]:
            self.board.development_card_deck.append(player_.development_cards.pop(player_.development_cards.index(card)))
            self.log_action(f"{player_.name} returned a {card} card to the bank")
        else:
            print(f'Invalid card type - cannot return {card} from player')
            time.sleep(5)

    # Moves -------------------------------------------------------------------------------------------------------------

    def return_possible_moves(self, player_: player) -> list[str]:
        """
        Returns a list of possible moves for a given player
        :param player_: The player to check
        :return: A list of possible moves
        """
        moves = []
        if len(player_.development_cards) > 0:
            moves.append('play_development_card')
        return moves

    def place_settlement(self, player_, location):
        if self.count_structure(player_, 'settlement') >= 5:
            print('You cannot build any more settlements')
            return False

        print(f'{player_.name} is placing a settlement')
        if self.get_buildings_list()[location]['player'] is not None:
            raise self.moveNotValid("Settlement already placed at location")
        for resource, amount in self.board.building_cost_list.get('settlement').items():
            for j in range(amount):
                self.return_player_card(player_, resource)
        self.board._buildings[location].update({'player': player_, 'building': 'settlement'})
        self.log_action(f'{player_.name} placed a settlement at {location}')
        return True

    def place_city(self, player_, location):
        if self.count_structure(player_, 'city') >= 4:
            print('You cannot build any more cities')
            return False
        print(f'{player_.name} is placing a city')
        if self.get_buildings_list()[location]['player'] is not player_:
            raise self.moveNotValid("Cannot upgrade a settlement that is not yours")
        if self.get_buildings_list()[location]['building'] != 'settlement':
            raise self.moveNotValid("Cannot upgrade a building that is not a settlement")
        for resource, amount in self.board.building_cost_list.get('city').items():
            for j in range(amount):
                self.return_player_card(player_, resource)
        self.board._buildings[location].update({'player': player_, 'building': 'city'})
        self.log_action(f'{player_.name} placed a city at {location}')
        return True

    def place_road(self, player_, location):
        if self.count_structure(player_, 'road') >= 15:
            print("You cannot build any more roads")
            return False
        try:
            self.board.roads[location].update({'player': player_})
            for resource, amount in self.board.building_cost_list.get('road').items():
                for i in range(amount):
                    self.return_player_card(player_, resource)
            self.log_action(f'{player_.name} placed a road at {location}')
            return True
        except KeyError:
            raise self.moveNotValid("A road cannot be placed at this location")

    def buy_development_card(self, player_) -> bool:
        if player_.count_cards('resources')['wheat'] >= 1 and player_.count_cards('resources')['sheep'] >= 1 and \
                player_.count_cards('resources')['rock'] >= 1:
            self.return_player_card(player_, 'wheat')
            self.return_player_card(player_, 'sheep')
            self.return_player_card(player_, 'rock')
            self.give_player_card(player_, 'development', 'development_card')
            self.log_action(f'{player_} bought a development card')
            return True
        else:
            return False

    def trade_with_bank(self, player_, give, get):
        """
        Allows a player to trade with the bank
        :param player_: The player trading
        :param give: The resource to be given
        :param get: The resource to be received
        :return: None
        """
        if player_.count_cards('resources')[give] >= 4:
            self.log_action(f'{player_.name} is trading 4x {give} for 1x {get}')
            for i in range(4):
                self.return_player_card(player_, give)
            self.give_player_card(player_, 'resource', get)
        else:
            print('Not enough resources to trade')

    def play_development_card(self, player_, card_to_play, *args):
        """
        Allows the player to play a development card
        :param player_: The player playing the card
        :param card_to_play: The card to be played
        :return:
        """
        card = card_to_play
        if card == 'soldier':
            player_.robber()
        elif card == 'monopoly':
            res_type = args[0]
            for other_player in self.get_players_list():
                if other_player != self:
                    while res_type in other_player.resources:
                        self.return_player_card(other_player, res_type)
                        self.give_player_card(player_, 'resource', res_type)
        elif card == 'year of plenty':
            for i in range(2):
                res_type = args[i]
                self.give_player_card(player_, 'resource', res_type)
        elif card == 'road building':
            for i in range(2):
                self.place_road(player_, player_.choose_road_location())
        self.return_player_card(player_, card_to_play)

    # Turn Actions and Processing a Roll ---------------------------------------------------------

    def process_roll(self, roll: int, current_player: player):
        """
        Processes a roll of the dice and performs the necessary board actions
        :param current_player: The player who rolled the dice
        :param roll: The number from the dice roll
        :return: None
        """
        if roll == 7:
            print("The robber has been rolled")
            for player_ in self.get_players_list():
                if len(player_.resources) >= 7:
                    player_.robber_discard(self)
            current_player.robber(self)

        else:
            for player_ in self.get_players_list():
                cards_to_give = {}
                for building in self.get_buildings_list():
                    if self.get_buildings_list()[building].get('building') is not None:
                        tiles = self.get_buildings_list()[building].get('tiles')
                        for building_tile in tiles:
                            if building_tile.dice_number == roll and not building_tile.contains_robber:
                                if self.get_buildings_list()[building].get('building') == 'settlement' and self.get_buildings_list()[building].get(
                                        'player') == player_:
                                    # print(f'Roll of {roll} has been made and {self._buildings[building].get("player")} has a
                                    # {self._buildings[building].get("building")} on {roll}, so receives 1x {building_tile.tile_type}')
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 1
                                    else:
                                        cards_to_give[building_tile.resource] = 1
                                elif self.get_buildings_list()[building].get('building') == 'city' and self.get_buildings_list()[building].get(
                                        'player') == player_:
                                    # print(f'Roll of {roll} has been made and {self._buildings[building].get("player")} has a
                                    # {self._buildings[building].get("building")} on {roll}, so receives 2x {building_tile.tile_type}')
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 2
                                    else:
                                        cards_to_give[building_tile.resource] = 2
                for card in cards_to_give:
                    self.give_player_card(player_, 'resource', card, cards_to_give[card])

    # Initial Placement --------

    def initial_placement(self):
        """
        Sets up the board for the game, by allowing players to place their initial settlements and roads, and then giving them the required cards
        Random placement is not true random - it will only place a settlement on a corner of a tile that will produce two or three resources, to help to avoid softlocks
        :return: None
        """
        print('\n -- Board Setup --\n')
        order = [player_ for player_ in self.board.players]
        rev_order = order.copy()
        rev_order.reverse()
        order = order + rev_order

        while len(order) > 0:
            player_ = order.pop(0)
            print(f'{player_} is placing settlement number {2 - order.count(player_)}')

            for resource in self.get_building_cost_list()['settlement']:
                self.give_player_card(player_, 'resource', resource, self.get_building_cost_list()['settlement'][resource])
            for resource in self.get_building_cost_list()['road']:
                self.give_player_card(player_, 'resource', resource, self.get_building_cost_list()['road'][resource])

            location = player_.initial_placement(self)
            if len(order) < len(self.board.players):
                # Players receive resources from their second settlement
                tiles_from_settlement = self.get_buildings_list()[location]['tiles']
                for tile_ in tiles_from_settlement:
                    if not tile_.contains_robber:
                        self.give_player_card(player_, 'resource', tile_.resource)
