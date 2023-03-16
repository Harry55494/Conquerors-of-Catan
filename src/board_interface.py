from src.board import *

import logging


# Static Methods for finding the longest road

# Using AI to write an AI program is ironic haha
# CHATGPT HAS WRITTEN THIS CODE ------------------------------------------------


def find_longest_route(paths):
    # create a dictionary to store the adjacency list of the graph
    adj_list = {}
    for path in paths:
        a, b = path
        if a not in adj_list:
            adj_list[a] = set()
        if b not in adj_list:
            adj_list[b] = set()
        adj_list[a].add(b)
        adj_list[b].add(a)

    # initialize variables for tracking the longest route and current path
    longest_route = []
    current_path = []

    # recursively find the longest route starting from the first node
    find_route_from_node(
        list(adj_list.keys())[0], adj_list, set(), set(), longest_route, current_path
    )

    return longest_route


def find_route_from_node(
    node, adj_list, visited, used_paths, longest_route, current_path
):
    visited.add(node)
    current_path.append(node)

    # check if the current path is longer than the longest route so far
    if len(current_path) > len(longest_route):
        longest_route[:] = current_path

    # recursively explore all unexplored neighbors of the node
    unexplored_neighbors = [
        neighbor for neighbor in adj_list[node] if neighbor not in visited
    ]
    if len(unexplored_neighbors) == 1:
        # if there is only one unexplored neighbor, continue exploring that path
        find_route_from_node(
            unexplored_neighbors[0],
            adj_list,
            visited,
            used_paths,
            longest_route,
            current_path,
        )
    elif len(unexplored_neighbors) > 1:
        # if there are multiple unexplored neighbors, mark this as a fork in the road
        for neighbor in unexplored_neighbors:
            path = frozenset([node, neighbor])
            if path not in used_paths:
                used_paths.add(path)
                find_route_from_node(
                    neighbor,
                    adj_list,
                    visited.copy(),
                    used_paths.copy(),
                    longest_route,
                    current_path.copy(),
                )
                used_paths.remove(path)

    # remove the current node from the visited set and current path
    visited.remove(node)
    current_path.pop()


# END OF CHATGPT'S CODE -------------------------------------------------------


def return_clusters(set):
    clusters = []
    for road in set:
        for cluster in clusters:
            for node in cluster:
                if road[0] in node or road[1] in node:
                    cluster.extend([road])
                    break
        else:
            if road not in [item for sublist in clusters for item in sublist]:
                clusters.append([road])

    return clusters


class board_interface:
    board: board

    class moveNotValid(Exception):
        def __init__(self, move):
            self.move = move
            self.message = f"The move {move} is not valid"
            super().__init__(self.message)
            raise self

    def __init__(self, players: list[player]):
        """
        Initialises a board_interface object.
        Object is used to interact with the board object in a standardised way e.g. takes cards from a player
        Acts similarly to a board master
        :param players: A list of players
        """
        self.minimax_mode = False
        self.setup_mode = False
        self.board = board(board_type="default", players=players)
        self.turn_number = 0

        with open("logs/board_actions.log", "w") as f:
            pass

        self.logger = logging.getLogger("board_interface")
        self.logger.setLevel(logging.DEBUG)
        file_format = logging.Formatter("[%(asctime)s] %(message)s")
        fh = logging.FileHandler("logs/board_actions.log")
        fh.setFormatter(file_format)
        self.logger.addHandler(fh)
        self.logger.debug("Board Interface created")

    def log_action(self, action):
        self.logger.debug(f"[Turn: {str(self.turn_number).ljust(3)}] {action}")

    def set_minimax(self, state):
        self.minimax_mode = state

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
        return self.board._roads

    def get_ports_list(self):
        return self.board._ports

    def get_building_cost_list(self):
        return self.board.building_cost_list

    def get_largest_army(self):
        return self.board.largest_army

    def get_longest_road(self):
        return self.board.longest_road

    def get_robber_location(self):
        for tile in self.board.tiles:
            if tile.contains_robber:
                return tile.letter

    def get_opposing_player(self, player_):
        if len(self.board.players) != 2:
            raise Exception("Cannot get opposing player if there are not 2 players")
        for player in self.board.players:
            if player != player_:
                return player

    def get_next_player(self, current_player):
        if current_player.number == self.board.players[-1].number:
            # print("Returning first player")
            return self.board.players[0]
        else:
            # find player with matching number
            current_player_number = current_player.number
            for player in self.board.players:
                if player.number == current_player_number + 1:
                    return player
        print(self.get_players_list())
        for player in self.get_players_list():
            print(player.number)
        raise Exception("Could not find next player")

    # Helper Functions

    def print_board(self, print_letters=False) -> None:
        self.board.print_board(print_letters)

    def has_potential_road(self, player_) -> int:
        road_endings = []
        for road in self.board._roads:
            if self.board._roads[road]["player"] == player_:
                road_endings.append(road[0])
                road_endings.append(road[1])
        return len(road_endings) > 0

    def move_robber(self, location):
        for tile_ in self.board.tiles:
            if tile_.contains_robber:
                tile_.contains_robber = False
            if tile_.letter == location:
                tile_.contains_robber = True

    def steal_from_player(
        self, player_to_steal_from: player, player_to_give_to: player
    ) -> None:
        if len(player_to_steal_from.resources) > 0:
            card = player_to_steal_from.resources.pop(
                random.randint(0, len(player_to_steal_from.resources) - 1)
            )
            self.give_player_card(player_to_give_to, "resource", card)
        else:
            print(f"{player_to_steal_from.name} has no cards to steal")

    def count_structure(self, player_, structure):
        count = 0
        if structure == "road":
            for road in self.get_roads_list():
                if self.get_roads_list()[road]["player"] is not None:
                    if self.get_roads_list()[road]["player"].number == player_.number:
                        count += 1
            return count
        for building in self.get_buildings_list():
            if self.get_buildings_list()[building]["player"] is not None:
                if (
                    self.get_buildings_list()[building]["player"].number
                    == player_.number
                ):
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
        for road, details in self.board._roads.items():
            if position in road:
                position_to_check.append(road[0])
                position_to_check.append(road[1])
        position_to_check = list(set(position_to_check))
        for coord in position_to_check:
            if self.get_buildings_list()[coord]["player"] is not None:
                return True
        return False

    def give_player_card(
        self, player_: player, card_type: str, card: str, amount=1
    ) -> bool:
        """
        Gives a player a card from the bank
        :param player_: The player to be given the card
        :param card_type: The card type to be given - resource or development
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :param amount: The amount to be given
        :return: None
        """
        if card_type == "resource" and not card == "desert":
            for i in range(amount):
                try:
                    player_.resources.append(
                        self.board.resource_deck.pop(
                            self.board.resource_deck.index(card)
                        )
                    )
                except ValueError:
                    if not self.minimax_mode:
                        print("Not enough cards in the bank")
            if not self.minimax_mode:
                self.log_action(
                    f"{player_.name} was given {amount} {card} from the bank"
                )
        elif card_type == "development":
            try:
                card_given = self.board.development_card_deck.pop(0)
                player_.development_cards.append(card_given)
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_.name} was given a {card_given} card from the bank"
                    )
                    self.log_action(
                        f"{player_.name} now has {len(player_.development_cards)} development cards"
                    )
            except IndexError:
                if not self.minimax_mode:
                    print("Not enough cards in the bank")
                return False
        else:
            print(f"Invalid card type - cannot give player {card}")
            time.sleep(5)

    def return_player_card(self, player_: player, card):
        """
        Returns a card to the bank
        :param player_: The player to take the card from
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :return: None
        """
        if card in ["wheat", "wood", "clay", "sheep", "rock"]:
            self.board.resource_deck.append(
                player_.resources.pop(player_.resources.index(card))
            )
            if not self.minimax_mode:
                self.log_action(f"{player_.name} returned a {card} card to the bank")
        elif card in [
            "knight",
            "victory point",
            "road building",
            "year of plenty",
            "monopoly",
        ]:
            self.board.development_card_deck.append(
                player_.development_cards.pop(player_.development_cards.index(card))
            )
            if not self.minimax_mode:
                self.log_action(f"{player_.name} returned a {card} card to the bank")
        else:
            print(f"Invalid card type - cannot return {card} from player")
            time.sleep(5)

    def get_potential_building_locations(
        self, player_, building="settlement", initial_placement=False
    ):
        """
        Returns a list of potential locations for a building to be placed
        :param interface:
        :param building:
        :return:
        """
        list = []
        if building == "settlement":
            if initial_placement:
                for key, item in self.get_buildings_list().items():
                    if not self.get_buildings_list()[key]["building"]:
                        if not self.check_for_nearby_settlements(key):
                            list.append(key)
            else:
                for road in self.get_roads_list():
                    if self.get_roads_list()[road]["player"] is not None:
                        if (
                            self.get_roads_list()[road]["player"].number
                            == player_.number
                        ):
                            if not self.check_for_nearby_settlements(road[0]):
                                list.append(road[0])
                            if not self.check_for_nearby_settlements(road[1]):
                                list.append(road[1])

        else:
            for key, item in self.get_buildings_list().items():
                if self.get_buildings_list()[key]["player"] is not None:
                    if (
                        self.get_buildings_list()[key]["player"].number
                        == player_.number
                        and self.get_buildings_list()[key]["building"] == "settlement"
                    ):
                        list.append(key)
            if len(list) == 0:
                sys.exit("No settlements to upgrade")

        return list

    def get_potential_road_locations(self, player_):
        road_endings = []
        for road in self.get_roads_list():
            if self.get_roads_list()[road]["player"] is not None:
                if self.get_roads_list()[road]["player"].number == player_.number:
                    if road[0] not in road_endings:
                        road_endings.append(road[0])
                    if road[1] not in road_endings:
                        road_endings.append(road[1])

        list_ = []

        for road in self.get_roads_list():
            for road_ending in road_endings:
                if road_ending in road:
                    if not self.get_roads_list()[road]["player"]:
                        list_.append(road)

        return list_

    def update_special_cards(self):
        """
        Checks whether players need to be given the largest army or longest road cards
        :return: None
        """

        # Check for largest army

        for player_ in self.get_players_list():
            if (player_.played_robber_cards > self.get_largest_army()[1]) and (
                player_.played_robber_cards >= 3
            ):
                self.board.largest_army = [player_, player_.played_robber_cards]
                if not self.minimax_mode:
                    print(
                        f"{player_} has the largest army with {player_.played_robber_cards} soldiers"
                    )
                    self.log_action(
                        f"{player_} has the largest army with {player_.played_robber_cards} soldiers"
                    )

        # Check for longest road

        for player_ in self.get_players_list():

            player_roads = []
            for road in self.get_roads_list():
                if self.get_roads_list()[road]["player"] is not None:
                    if self.get_roads_list()[road]["player"].number == player_.number:
                        player_roads.append(road)

            clusters = return_clusters(player_roads)
            if not any(len(cluster) >= 5 for cluster in clusters):
                continue

            current_longest_road = self.get_longest_road()

            # get longest cluster
            longest_cluster = max(clusters, key=len)

            max_cluster = len(find_longest_route(longest_cluster)) - 1
            if max_cluster > current_longest_road[1] and max_cluster >= 5:
                self.board.longest_road = [player_, max_cluster]
                if not self.minimax_mode:
                    print(
                        f"{player_} has a road of length {max_cluster} and has been given the longest road card"
                    )
                    self.log_action(
                        f"{player_.name} has a road of length {max_cluster} and has been given the longest road card"
                    )

    # Moves -------------------------------------------------------------------------------------------------------------

    def return_possible_moves(self, player_: player) -> list[str]:
        """
        Returns a list of possible moves for a given player
        :param player_: The player to check
        :return: A list of possible moves
        """
        hand = player_.count_cards("resources")
        buildings_count = {"settlements": 0, "cities": 0}
        for building in self.get_buildings_list():
            if self.get_buildings_list()[building]["player"] is not None:
                if (
                    self.get_buildings_list()[building]["player"].number
                    == player_.number
                ):
                    if self.get_buildings_list()[building]["building"] == "settlement":
                        buildings_count["settlements"] += 1
                    elif self.get_buildings_list()[building]["building"] == "city":
                        buildings_count["cities"] += 1
        moves = []
        # Check if the player can trade with the bank
        for card in hand:
            if hand[card] >= 4:
                moves.append("trade with bank")

        for port in self.get_ports_list():
            if self.get_ports_list()[port] is not None:
                if self.get_ports_list()[port]["player"] is not None:
                    if self.get_ports_list()[port]["player"].number == player_.number:
                        type_ = self.get_ports_list()[port]["symbol"]
                        player_resources = player_.count_cards("resources")
                        port_resource = self.get_ports_list()[port]["resource"]
                        highest_resource = max(player_resources.values())
                        if ("2" in type_ and player_resources[port_resource] >= 2) or (
                            "3" in type_ and highest_resource >= 3
                        ):
                            moves.append("trade with port")

        # Check if player can build a city
        if (
            hand["wheat"] >= 2
            and hand["rock"] >= 3
            and 0 < buildings_count["settlements"] < 4
        ):
            moves.append("build city")

        # Check if player can build a settlement
        if (
            hand["wheat"] >= 1
            and hand["sheep"] >= 1
            and hand["wood"] >= 1
            and hand["clay"] >= 1
            and buildings_count["settlements"] < 5
        ):
            moves.append("build settlement")

        # Check if player can build a road
        if (
            hand["wood"] >= 1
            and hand["clay"] >= 1
            and self.has_potential_road(player_)
            and self.count_structure(player_, "road") < 15
        ):
            moves.append("build road")

        # Check if player can buy a development card
        if hand["sheep"] >= 1 and hand["rock"] >= 1 and hand["wheat"] >= 1:
            moves.append("buy development card")

        # Check if the player can play a development card
        if len(player_.development_cards) > 0 and len(
            player_.development_cards
        ) > player_.development_cards.count("victory point"):
            moves.append("play development card")

        return moves

    def place_settlement(self, player_, location, setup=False):
        if self.count_structure(player_, "settlement") >= 5:
            print("You cannot build any more settlements")
            return False

        if not self.minimax_mode and not setup:
            print(f"{player_.name} is placing a settlement")
        if self.get_buildings_list()[location]["player"] is not None:
            raise self.moveNotValid("Settlement already placed at location")
        if not self.setup_mode:
            for resource, amount in self.board.building_cost_list.get(
                "settlement"
            ).items():
                for j in range(amount):
                    self.return_player_card(player_, resource)
        self.board._buildings[location].update(
            {"player": player_, "building": "settlement"}
        )
        if not self.minimax_mode:
            self.log_action(f"{player_.name} placed a settlement at {location}")

        # check for ports

        for entry in self.get_ports_list().keys():
            if self.get_ports_list()[entry] is not None:
                if location in entry:
                    self.board._ports[entry].update({"player": player_})
                    if not self.minimax_mode:
                        self.log_action(f"{player_.name} has claimed a port at {entry}")

        return True

    def place_city(self, player_, location):
        if self.count_structure(player_, "city") >= 4:
            print("You cannot build any more cities")
            return False
        if not self.minimax_mode:
            print(f"{player_.name} is placing a city")
        if self.get_buildings_list()[location]["player"].number != player_.number:
            raise self.moveNotValid("Cannot upgrade a settlement that is not yours")
        if self.get_buildings_list()[location]["building"] != "settlement":
            raise self.moveNotValid(
                "Cannot upgrade a building that is not a settlement"
            )
        for resource, amount in self.board.building_cost_list.get("city").items():
            for j in range(amount):
                self.return_player_card(player_, resource)
        self.board._buildings[location].update({"player": player_, "building": "city"})
        if not self.minimax_mode:
            self.log_action(f"{player_.name} placed a city at {location}")
        return True

    def place_road(self, player_, location, free_from_dev_card=False):
        if self.count_structure(player_, "road") >= 15:
            if isinstance(player_, ai_player):
                print("You cannot build any more _roads")
            return False
        try:
            self.board._roads[location].update({"player": player_})
            if not self.setup_mode:
                for resource, amount in self.board.building_cost_list.get(
                    "road"
                ).items():
                    if not self.minimax_mode and not free_from_dev_card:
                        for i in range(amount):
                            self.return_player_card(player_, resource)
            if not self.minimax_mode:
                self.log_action(
                    f'{player_.name} placed a road at {location} {"(free from development card)" if free_from_dev_card else ""}'
                )
            self.update_special_cards()
            return True
        except KeyError:
            raise self.moveNotValid("A road cannot be placed at this location")

    def buy_development_card(self, player_) -> bool:
        if (
            player_.count_cards("resources")["wheat"] >= 1
            and player_.count_cards("resources")["sheep"] >= 1
            and player_.count_cards("resources")["rock"] >= 1
        ):
            self.return_player_card(player_, "wheat")
            self.return_player_card(player_, "sheep")
            self.return_player_card(player_, "rock")
            self.give_player_card(player_, "development", "development_card")
            if not self.minimax_mode:
                self.log_action(f"{player_.name} bought a development card")
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
        if player_.count_cards("resources")[give] >= 4:
            if not self.minimax_mode:
                self.log_action(f"{player_.name} is trading 4x {give} for 1x {get}")
            for i in range(4):
                self.return_player_card(player_, give)
            self.give_player_card(player_, "resource", get)
        else:
            if not self.minimax_mode:
                print("Not enough resources to trade")

    def trade_with_port(self, player_, give, get):
        """
        Allows a player to trade with a port
        :param player_: The player trading
        :param give: The resource to be given
        :param get: The resource to be received
        :return:
        """
        if not self.minimax_mode:
            self.log_action(
                f"{player_.name} is attempting to use a port to trade {give} for {get}"
            )

        for port in self.get_ports_list():
            if self.get_ports_list()[port] is not None:
                if self.get_ports_list()[port]["player"] is not None:
                    if self.get_ports_list()[port]["player"].number == player_.number:
                        port_resource = self.get_ports_list()[port]["resource"]
                        if port_resource == give:
                            if player_.resources.count(give) >= 2:
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.give_player_card(player_, "resource", get)
                                if not self.minimax_mode:
                                    self.log_action(
                                        f"{player_.name} has used a port to trade 2x {give} for 1x {get}"
                                    )
                                return
                        elif port_resource == "any":
                            if player_.resources.count(give) >= 3:
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.give_player_card(player_, "resource", get)
                                if not self.minimax_mode:
                                    self.log_action(
                                        f"{player_.name} has used a port to trade 3x {give} for 1x {get}"
                                    )
                                return
        self.log_action(f"{player_.name} does not have enough resources to trade")

    def trade_with_player(
        self, original_player, player_to_trade_with, resource_to_give, resource_to_get
    ):
        """
        Allows a player to trade with another player
        Trades are always 1:1
        :param original_player:
        :param player_to_trade_with:
        :param resource_to_give:
        :param resource_to_get:
        :return:
        """
        if not self.minimax_mode:
            print(
                f"{original_player.name} is offering to trade with {player_to_trade_with.name} - {resource_to_give} for {resource_to_get}"
            )
        if (
            original_player.count_cards("resources")[resource_to_give] >= 1
            and player_to_trade_with.count_cards("resources")[resource_to_get] >= 1
        ):
            result = player_to_trade_with.respond_to_trade(
                original_player, resource_to_give, resource_to_get
            )
            if result:
                self.return_player_card(original_player, resource_to_give)
                self.return_player_card(player_to_trade_with, resource_to_get)
                self.give_player_card(original_player, "resource", resource_to_get)
                self.give_player_card(
                    player_to_trade_with, "resource", resource_to_give
                )
                if not self.minimax_mode:
                    self.log_action(
                        f"{original_player.name} traded {resource_to_give} for {resource_to_get} with {player_to_trade_with.name}"
                    )
            else:
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_to_trade_with.name} refused to trade with {original_player.name}"
                    )
        else:
            if not self.minimax_mode:
                print("Not enough resources to trade")

    def play_development_card(self, player_, card_to_play, *args):
        """
        Allows the player to play a development card
        :param player_: The player playing the card
        :param card_to_play: The card to be played
        :return:
        """
        self.log_action(f"{player_.name} is playing a {card_to_play}")
        card = card_to_play
        if card == "soldier":
            if player_.development_cards.count("soldier") > player_.played_robber_cards:
                player_.robber(self)
                player_.played_robber_cards += 1
        elif card == "monopoly":
            res_type = args[0]
            for other_player in self.get_players_list():
                if other_player != player_:
                    while res_type in other_player.resources:
                        self.return_player_card(other_player, res_type)
                        self.give_player_card(player_, "resource", res_type)
        elif card == "year of plenty":
            for i in range(2):
                res_type = args[i]
                self.give_player_card(player_, "resource", res_type)
        elif card == "road building":
            for i in range(2):
                self.place_road(
                    player_, player_.choose_road_location(self), free_from_dev_card=True
                )
        if card != "soldier":
            self.return_player_card(player_, card)

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
            if not isinstance(current_player, ai_player):
                time.sleep(3)

        else:
            for player_ in self.get_players_list():
                cards_to_give = {}
                for building in self.get_buildings_list():
                    if self.get_buildings_list()[building].get("building") is not None:
                        tiles = self.get_buildings_list()[building].get("tiles")
                        for building_tile in tiles:
                            if (
                                building_tile.dice_number == roll
                                and not building_tile.contains_robber
                            ):
                                if (
                                    self.get_buildings_list()[building].get("building")
                                    == "settlement"
                                    and self.get_buildings_list()[building].get(
                                        "player"
                                    )
                                    == player_
                                ):
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 1
                                    else:
                                        cards_to_give[building_tile.resource] = 1
                                elif (
                                    self.get_buildings_list()[building].get("building")
                                    == "city"
                                    and self.get_buildings_list()[building].get(
                                        "player"
                                    )
                                    == player_
                                ):
                                    if building_tile.resource in cards_to_give:
                                        cards_to_give[building_tile.resource] += 2
                                    else:
                                        cards_to_give[building_tile.resource] = 2
                for card in cards_to_give:
                    self.give_player_card(
                        player_, "resource", card, cards_to_give[card]
                    )

    # Initial Placement --------

    def initial_placement(self):
        """
        Sets up the board for the game, by allowing players to place their initial settlements and _roads, and then giving them the required cards
        Random placement is not true random - it will only place a settlement on a corner of a tile that will produce two or three resources, to help to avoid softlocks
        :return: None
        """
        print("\n -- Board Setup --\n")
        self.log_action("Board Setup")
        self.setup_mode = True
        order = [player_ for player_ in self.get_players_list()]
        rev_order = order.copy()
        rev_order.reverse()
        order = order + rev_order

        while len(order) > 0:
            player_ = order.pop(0)
            print(f"{player_} is placing settlement number {2 - order.count(player_)}")

            location = player_.initial_placement(self)
            print(f"{player_} has placed their settlement at {location}")
            if len(order) < len(self.board.players):
                # Players receive resources from their second settlement
                tiles_from_settlement = self.get_buildings_list()[location]["tiles"]
                for tile_ in tiles_from_settlement:
                    if not tile_.contains_robber:
                        self.give_player_card(player_, "resource", tile_.resource)
        self.setup_mode = False
        self.log_action("Board Setup Complete")
