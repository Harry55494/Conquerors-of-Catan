"""
AI Minimax Player
Contains the logic for the minimax AI player to play the game

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

import math
from datetime import datetime, timedelta
from src.longest_road import *

from src.ai_player import *

import time

import copy


# Minimax timeout exception, to be raised if the minimax algorithm takes too long
# Is caught by the minimax algorithm, and the best move found so far is returned
class MiniMaxTimeoutException(Exception):
    pass


class ai_minimax(ai_player):
    def __init__(
        self,
        number,
        colour,
        time_limit=CONFIG["minimax_time_limit"],
        max_depth=CONFIG["minimax_max_depth"],
        epsilon_pruning_level=CONFIG["epsilon_pruning_level"],
    ) -> None:
        """
        Constructor for the minimax AI player
        :param number: The player number
        :param colour: The player colour
        :param time_limit: The time limit for the minimax algorithm to run for, defaults to CONFIG["minimax_time_limit"]
        :param max_depth: The maximum depth for the minimax algorithm to search to, defaults to CONFIG["minimax_max_depth"]\
        :param epsilon_pruning_level: Whether to use epsilon pruning, defaults to CONFIG["epsilon_pruning"]
        """
        # Call the parent constructor
        super().__init__(number=number, colour=colour, strategy="minimax")
        # Log the creation of the player
        self.log(
            "Minimax player created with time limit of "
            + str(time_limit)
            + " seconds and max depth of "
            + str(max_depth)
            + " levels, epsilon pruning is set to level "
            + str(epsilon_pruning_level)
        )
        # Set the time limit and max depth, and initialise the root score map
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.root_score_map = []
        self.temp_score_variation_map = [0, {}]
        self.start_time = None
        self.epsilon_pruning = epsilon_pruning_level

    def perform_minimax_move(self, player_clone, interface_clone, move):
        """
        Contains the logic for performing a move within a minimax search
        Performs a move within a minimax search, for a specific player
        Acts as a simple interpreter for the move, and calls the appropriate function on the interface
        :param move: The move to be performed
        :param player_clone: The player object to perform the move from
        :param interface_clone: The interface object to perform the move on
        :return: The interface object after the move has been performed
        """
        if move[0] == "buy development card":
            interface_clone.buy_development_card(player_clone)
        elif move[0] == "play development card":
            if move[1] == "year of plenty":
                interface_clone.play_development_card(
                    player_clone, move[1], move[2], move[3]
                )
            elif move[1] == "monopoly":
                interface_clone.play_development_card(player_clone, move[1], move[2])
            else:
                interface_clone.play_development_card(player_clone, move[1])
        elif move[0] == "build road":
            interface_clone.place_road(player_clone, move[1])
        elif move[0] == "build settlement":
            interface_clone.place_settlement(player_clone, move[1])
        elif move[0] == "build city":
            interface_clone.place_city(player_clone, move[1])
        elif move[0] == "trade with bank":
            interface_clone.trade_with_bank(player_clone, move[1], move[2])
        elif move[0] == "trade with port":
            interface_clone.trade_with_port(player_clone, move[1], move[2])
        elif move[0] == "trade with player":
            # Cannot suppose that the other player will trade with us, so don't trade if this is the case
            # We will assume that the opposing player always trades with us
            # TODO Currently does this actually trade?
            if move[1] == self.number:
                interface_clone.trade_with_player(
                    player_clone, move[2], move[3], move[4]
                )
        elif move[0] == "end turn":
            pass
        else:
            # If the move is not recognised, raise an error
            raise NotImplementedError(
                "perform_minimax_move does not know how to perform " + str(move)
            )
        return interface_clone

    def evaluate_board(self, interface) -> int:
        """
        Heuristic function to evaluate the board state
        Most of this is self-explanatory
        See README for more details of how the heuristic is calculated
        :param interface: board_interface
        :return: The evaluation of the board as an integer
        """

        # The score variation map is a map of the reasons for the score variation, and the amount of the variation
        # Useful for debugging
        score_variation_map = {}
        score = 0

        def update_score(amount, reason) -> None:
            """
            Updates the score and score variation map
            :param amount: The amount to update the score by
            :param reason: The reason for the score update
            :return:
            """
            nonlocal score
            nonlocal score_variation_map
            score += amount
            score_variation_map[reason] = amount

        # GET VARIABLES TO SAVE TIME

        buildings_list = interface.get_buildings_list()

        # Victory Points Scoring ------------------------------------------------------

        current_vp = self.calculateVictoryPoints(
            interface, buildings_list=buildings_list
        )

        other_players = [
            player
            for player in interface.get_players_list()
            if player.number != self.number
        ]

        other_players.sort(
            key=lambda x: x.calculateVictoryPoints(
                interface, buildings_list=buildings_list
            ),
            reverse=True,
        )

        # Score based on victory points
        update_score(current_vp * 10, "victory points")

        update_score(
            -self.development_cards.count("Victory Point") * 5,
            "Penalise relying on VP cards",
        )

        target_score = CONFIG["target_score"]

        # Score based on being close to, or actually, winning
        if current_vp >= target_score:
            return 1000000
        if current_vp == target_score - 1:  # Bonus points for being close to winning
            update_score(1000, "close to winning")

        if current_vp > other_players[0].calculateVictoryPoints(
            interface, buildings_list=buildings_list
        ):
            update_score(50, "leading")
        elif current_vp == other_players[0].calculateVictoryPoints(
            interface, buildings_list=buildings_list
        ):
            update_score(25, "tied for first")

        # Number of roads -----------------------------------------------------

        update_score(-interface.count_structure(self, "road") * 1.5, "roads")

        # Number of resources player has access to -----------------------------
        # This is relative to the number of resources a player would get on a turn if every dice roll was rolled.

        # Higher numbers are less common, so they should be weighted more

        # rarity = board.calculate_resource_rarity()

        resources = []
        resources_has_access_to = []
        settlements_count = 0
        cities_count = 0
        roll_map = {}

        # Rating settlements and cities
        for key, item in buildings_list.items():
            if buildings_list[key]["player"] is not None:
                if buildings_list[key]["player"].number == self.number:

                    # Rate based on number of resources available

                    building_type = buildings_list[key]["building"]

                    if building_type == "settlement":
                        resources.append(item for item in buildings_list[key]["tiles"])
                        if settlements_count >= 2:
                            update_score(500, "settlement at " + str(key))
                        else:
                            settlements_count += 1
                    elif building_type == "city":
                        resources.append(item for item in buildings_list[key]["tiles"])
                        resources.append(item for item in buildings_list[key]["tiles"])
                        cities_count += 1
                        update_score(1000, "city at " + str(key))

                    # Rate based on frequency of dice roll for each resource
                    update_score(
                        (
                            sum(
                                [
                                    tile.frequency
                                    for tile in buildings_list[key]["tiles"]
                                ]
                            )
                            * 2
                        ),
                        "tiles and frequency of dice roll at " + str(key),
                    )

                    for tile in buildings_list[key]["tiles"]:
                        multiplier = 1 if building_type == "settlement" else 2
                        if tile.resource not in roll_map:
                            roll_map[tile.resource] = multiplier * max(
                                1, tile.frequency
                            )
                        else:
                            roll_map[tile.resource] = multiplier * max(
                                roll_map[tile.resource], tile.frequency
                            )

                    # Rate settlement higher if there are more tiles nearby
                    num_tiles = len([item for item in buildings_list[key]["tiles"]])
                    update_score(
                        num_tiles, "number of tiles nearby to building" + str(key)
                    )

                    # Rate higher if there is one of each tile nearby
                    nearby_resources = [item for item in buildings_list[key]["tiles"]]
                    for resource in nearby_resources:
                        resources_has_access_to.append(resource.resource)

        update_score(len(resources), "total amount of resources")

        update_score(
            int(0.5 * max(len(self.resources) - 7, 0)),
            "Penalise having too many resources",
        )

        # Check for ports
        for port in interface.get_ports_list():
            if interface.get_ports_list()[port] is not None:
                if interface.get_ports_list()[port]["player"] is not None:
                    if interface.get_ports_list()[port]["player"].number == self.number:

                        # Rate based on whether the port is a 3:1 port or a 2:1 port
                        # and whether the player has access to the resource, and if so whether it is a city or settlement
                        if interface.get_ports_list()[port]["symbol"] == "3:1":
                            # Resource = any
                            if cities_count >= 1:
                                update_score(
                                    (4 * max(roll_map.values())),
                                    "3:1 port and building on "
                                    + str(max(roll_map.values())),
                                )
                        else:
                            if (
                                interface.get_ports_list()[port]["resource"]
                                in resources_has_access_to
                            ):
                                update_score(
                                    (
                                        2
                                        * roll_map[
                                            interface.get_ports_list()[port]["resource"]
                                        ]
                                    ),
                                    "2:1 port and building on "
                                    + str(
                                        roll_map[
                                            interface.get_ports_list()[port]["resource"]
                                        ]
                                    ),
                                )

        has_longest_road = False

        # Check for longest road
        if interface.get_longest_road()[0] is not None:
            if interface.get_longest_road()[0].number == self.number:
                update_score(25, "longest road")
                has_longest_road = True
        if interface.get_largest_army()[0] is not None:
            if interface.get_largest_army()[0].number == self.number:
                update_score(25, "largest army")

        # Check for how long the longest road is

        player_roads = []
        for road in interface.get_roads_list():
            if interface.get_roads_list()[road]["player"] is not None:
                if interface.get_roads_list()[road]["player"] == self:
                    player_roads.append(road)

        if player_roads:
            # Prefer nicely spaced settlements (2 roads between each, not more)
            # TODO Do this better
            if settlements_count + cities_count / len(player_roads) <= 1:
                update_score(25, "Nicely Spaced Settlements")

        clusters = return_clusters(player_roads)
        if clusters:
            longest_cluster = max(clusters, key=len)
            max_cluster = len(find_longest_route(longest_cluster)) - 1
            update_score(
                max_cluster * (2 if not has_longest_road else 1),
                "longest continuous road",
            )

        # Rate higher if there is one of each tile nearby
        update_score(
            len(list(set(resources_has_access_to))) * 3,
            "amount of each resource nearby",
        )

        # Number of development cards ------------------------------------------

        # score += len(self.development_cards) if len(self.development_cards) < 5 else 5
        if len(self.development_cards) >= 2:
            update_score(
                -max(0, len(self.development_cards) - 2) * 10,
                "amount of development cards",
            )
        update_score(self.played_robber_cards * 3, "played robber cards")

        # Potential to build something (only applies at max depth 0)
        buildings_cost_list = interface.get_building_cost_list()
        for building in buildings_cost_list:
            if building != "development card" and building != "road":
                resource_list = buildings_cost_list[building]
                for resource in resource_list:
                    if resource_list[resource] > 0:
                        if resource_list[resource] <= self.resources.count(resource):
                            if CONFIG["minimax_max_depth"] == 0:
                                update_score(
                                    10, "has all " + resource + " to build " + building
                                )

        """
        # Score based on robber location
        # If the robber is on a tile that the player has access to, then the player should be penalised
        # If the robber is on a tile that the player does not have access to, then the player should be rewarded
        # The higher the number of resources on the tile, the more the player should be rewarded
        # The lower the number of resources on the tile, the more the player should be penalised

        robber_tile = interface.get_robber_location()
        for building in interface.get_buildings_list().values():
            if building["player"] is not None:
                for tile in building["tiles"]:
                    if robber_tile == tile:
                        score += -25 if building["player"].number == self.number else 25
                    else:
                        score += tile.frequency if building["player"].number == self.number else -tile.frequency"""

        # Overwrite score with temp score if it is better, as this is the score that will be used for the minimax algorithm
        if score > self.temp_score_variation_map[0]:
            self.temp_score_variation_map = [score, score_variation_map]

        return score

    def choose_road_location(self, interface) -> tuple[int, int]:
        """
        Chooses the location of a road to be built
        :param interface:
        :return:
        """

        score_map = {}

        self.log("Choosing road location")

        # Iterate through all potential road locations and evaluate the board at each location
        for location in interface.get_potential_road_locations(self):
            interface_copy = copy.deepcopy(interface)
            interface_copy.set_minimax(True)
            player_copy = copy.deepcopy(self)
            interface_copy.place_road(player_copy, location)
            # Save the score of the board at this location
            score_map[location] = self.evaluate_board(interface_copy)

        self.log("Potential Roads Score Map: " + str(score_map))

        # Return the location with the highest score
        return max(score_map, key=score_map.get)

    def initial_placement(self, interface) -> None:
        """
        Chooses the location of a settlement and road to be built
        :param interface: Interface object
        :return: None
        """

        # Get all potential locations for the settlement
        potential_locations = interface.get_potential_building_locations(
            self, initial_placement=True
        )

        # Iterate through all potential locations and evaluate the board at each location
        location_score_map = {}
        for location in potential_locations:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            interface_clone.place_settlement(self, location)
            # Save the score of the board at this location
            location_score_map[location] = self.evaluate_board(interface_clone)

        # Return the location with the highest score
        best_location = max(location_score_map, key=location_score_map.get)
        interface.place_settlement(self, best_location, True)

        # Get all potential locations for the road
        # Cannot use the above method as this is the first road placed and the player has no roads
        road_score_map = {}

        for road in [
            road for road in interface.get_roads_list() if best_location in road
        ]:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            interface_clone.place_road(self, road)
            road_score_map[road] = self.evaluate_board(interface_clone)

        # Return the road with the highest score and place it
        best_road = max(road_score_map, key=road_score_map.get)
        interface.place_road(self, best_road)

        return best_location

    def robber(self, interface) -> None:
        """
        Decide which player to rob and where to move the robber
        :param interface:
        :return: None
        """

        # Get all potential locations for the robber
        potential_locations = [
            tile for tile in interface.get_tiles_list() if tile.resource != "desert"
        ]

        # Iterate through all potential locations and evaluate the board at each location
        location_score_map = {}
        for location in potential_locations:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            interface_clone.move_robber(location)
            # Save the score of the board at this location
            location_score_map[location] = self.evaluate_board(interface_clone)

        # Move the robber to the location with the highest score
        location = max(location_score_map, key=location_score_map.get)
        interface.move_robber(location)

        # Get all players that have resources
        potential_players = []
        for player in interface.get_players_list():
            if player.number != self.number:
                if len(player.resources) > 0:
                    potential_players.append(player)

        # If there are no players with resources, return
        if len(potential_players) == 0:
            return None
        # If there is only one player with resources, steal from them
        if len(potential_players) == 1:
            interface.steal_from_player(self, potential_players[0])
        # If there are multiple players with resources, steal from the player with the most resources
        else:
            interface.steal_from_player(
                self, max(potential_players, key=lambda x: len(x.resources))
            )

    def robber_discard(self, interface) -> None:
        """
        Discard half of the players resources
        :param interface: Interface object
        :return: None
        """
        # Discard half of the players resources
        # Does this by evaluating the board at each possible discard and choosing the discard that results in the best board
        required_length = len(self.resources) // 2
        while len(self.resources) > required_length:
            could_discard = list(set(self.resources))
            scores = {}
            # Evaluate the board at each possible discard
            for card in could_discard:
                clone = copy.deepcopy(self)
                clone.resources.remove(card)
                scores[card] = clone.evaluate_board(interface)

            # Discard the card that results in the best board, and loop again
            interface.return_player_card(
                self, self.resources[self.resources.index(min(scores, key=scores.get))]
            )

    def offer_trade(self, interface) -> None:
        """
        Use the minimax algorithm to decide which trade to offer
        :param interface: Interface object
        :return: None
        """
        trades = [
            move
            for move in interface.get_move_combinations(self)
            if move[0] == "trade with player"
        ]
        scores = {}
        # Evaluate the board at each possible trade
        for trade in trades:
            clone = copy.deepcopy(self)
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            clone.resources.extend(trade[2])
            clone.resources.remove(trade[1])
            scores[trade] = clone.evaluate_board(interface_clone)
        best_trade = max(scores, key=scores.get)
        interface.offer_trade(self, best_trade[1], best_trade[2], best_trade[3])

    def respond_to_trade(self, interface, original_player, receiving, giving) -> bool:
        """
        Evaluate the trade and decide whether to accept or reject
        :param interface: Interface object
        :param original_player: The player who initiated the trade
        :param receiving: What the player is receiving
        :param giving: What the player is giving
        :return: Whether to accept or reject the trade
        """

        # Evaluate the board at each possible response
        scores = {}
        for response in [True, False]:
            clone = copy.deepcopy(self)
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            if response:
                clone.resources.extend(receiving)
                for card in giving:
                    clone.resources.remove(card)
            scores[response] = clone.evaluate_board(interface_clone)

        # Return the response that results in the best board
        return min(scores, key=scores.get)

    # Minimax functions --------------------------------------------------------

    def get_move_combinations(self, interface, current_player) -> list | bool:
        """
        Returns a list of all possible combinations of moves for the player
        Also performs Epsilon Pruning if set by the MiniMax AI
        :param interface: The current state of the game
        :param current_player: The player whose turn it is
        :return: A list of all possible combinations of moves for the player
        """

        # Get all possible moves for the player
        potential_moves = interface.return_possible_moves(current_player)
        if not potential_moves:
            return False
        # print(potential_moves)

        # Append all combinations of moves to a list
        full_move_list = []
        for move in potential_moves:

            # Append settlement locations
            if move == "build settlement":
                for location in interface.get_potential_building_locations(
                    current_player
                ):
                    full_move_list.append(["build settlement", location])

            # Append city locations
            elif move == "build city":
                for location in interface.get_potential_building_locations(
                    current_player, "city"
                ):
                    full_move_list.append(["build city", location])

            # Append road locations
            elif move == "build road":
                local_moves = []
                for location in interface.get_potential_road_locations(current_player):
                    local_moves.append(["build road", location])

                if self.epsilon_pruning >= 2:
                    scores = []
                    for move in local_moves:
                        clone = copy.deepcopy(current_player)
                        interface_clone = copy.deepcopy(interface)
                        interface_clone.set_minimax(True)
                        self.perform_minimax_move(clone, interface_clone, move)
                        scores.append([move, self.evaluate_board(interface_clone)])
                    local_moves = [max(scores, key=lambda x: x[1])[0]]
                full_move_list.extend(local_moves)

            # Append trade with bank moves
            elif move == "trade with bank":
                local_moves = []
                resources_can_trade = list(
                    set(
                        [
                            resource
                            for resource in current_player.resources
                            if current_player.resources.count(resource) >= 4
                        ]
                    )
                )
                for resource in resources_can_trade:
                    for resource_to_get in ["clay", "rock", "sheep", "wheat", "wood"]:
                        if resource_to_get != resource:
                            local_moves.append([move, resource, resource_to_get])

                if self.epsilon_pruning >= 1:
                    scores = []
                    for trade in local_moves:
                        clone = copy.deepcopy(current_player)
                        interface_clone = copy.deepcopy(interface)
                        interface_clone.set_minimax(True)
                        clone.resources.extend(trade[2])
                        for i in range(4):
                            clone.resources.remove(trade[1])
                        scores.append([trade, self.evaluate_board(interface_clone)])
                    local_moves = [max(scores, key=lambda x: x[1])[0]]

                full_move_list.extend(local_moves)

            # Append trade with port moves
            elif move == "trade with port":
                local_moves = []
                port_resources = get_port_combinations(interface, current_player)
                # Add all possible trades to the list to receive
                for resource in port_resources:
                    for resource_to_get in ["clay", "rock", "sheep", "wheat", "wood"]:
                        if resource_to_get != resource:
                            local_moves.append([move, resource, resource_to_get])

                if self.epsilon_pruning >= 1:
                    scores = []
                    for trade in local_moves:
                        clone = copy.deepcopy(current_player)
                        interface_clone = copy.deepcopy(interface)
                        interface_clone.set_minimax(True)
                        clone.resources.extend(trade[2])
                        clone.resources.remove(trade[1])
                        scores.append([trade, self.evaluate_board(interface_clone)])
                    local_moves = [max(scores, key=lambda x: x[1])[0]]

                full_move_list.extend(local_moves)

            # Append trade with player moves
            # can look at the other players resources to not offer trades that are impossible
            elif move == "trade with player":
                local_moves = []
                for other_player in [
                    player
                    for player in interface.get_players_list()
                    if player != current_player
                ]:
                    for resource in list(set(current_player.resources)):
                        for resource_to_get in list(set(other_player.resources)):
                            if resource_to_get != resource:
                                local_moves.append(
                                    [
                                        move,
                                        current_player,
                                        other_player,
                                        resource,
                                        resource_to_get,
                                    ]
                                )
                if not local_moves:
                    continue
                if self.epsilon_pruning >= 1:
                    # reduce list to only the best trade, using the perform_minimax_move to get the interface object, and the evaluate_board function to rank them
                    scores = []
                    for trade in local_moves:
                        clone = copy.deepcopy(current_player)
                        interface_clone = copy.deepcopy(interface)
                        interface_clone.set_minimax(True)
                        clone.resources.extend(trade[4])
                        clone.resources.remove(trade[3])
                        scores.append([trade, self.evaluate_board(interface_clone)])
                    local_moves = [max(scores, key=lambda x: x[1])[0]]
                full_move_list.extend(local_moves)

            # Append development card moves
            elif move == "play development card":
                if self == current_player:
                    for card in current_player.development_cards:
                        move = "play development card"
                        if (
                            card == "soldier"
                            and current_player.development_cards.count("soldier")
                            > current_player.played_robber_cards
                        ):
                            full_move_list.append([move, card])
                        elif card == "road building":
                            full_move_list.append([move, card])

                        # Year of Plenty with all possible combinations of resources
                        elif card == "year of plenty":
                            local_moves = []
                            for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                                for resource2 in [
                                    "clay",
                                    "rock",
                                    "sheep",
                                    "wheat",
                                    "wood",
                                ]:
                                    local_moves.append(
                                        [move, card, resource, resource2]
                                    )

                            if self.epsilon_pruning >= 1:
                                scores = []
                                for move in local_moves:
                                    clone = copy.deepcopy(current_player)
                                    interface_clone = copy.deepcopy(interface)
                                    interface_clone.set_minimax(True)
                                    self.perform_minimax_move(
                                        clone, interface_clone, move
                                    )
                                    scores.append(
                                        [move, self.evaluate_board(interface_clone)]
                                    )
                                local_moves = [max(scores, key=lambda x: x[1])[0]]
                            full_move_list.extend(local_moves)

                        # Monopoly with all possible resources
                        elif card == "monopoly":
                            local_moves = []
                            for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                                local_moves.append([move, card, resource])

                            if self.epsilon_pruning >= 1:
                                scores = []
                                for move in local_moves:
                                    clone = copy.deepcopy(current_player)
                                    interface_clone = copy.deepcopy(interface)
                                    interface_clone.set_minimax(True)
                                    self.perform_minimax_move(
                                        clone, interface_clone, move
                                    )
                                    scores.append(
                                        [move, self.evaluate_board(interface_clone)]
                                    )
                                local_moves = [max(scores, key=lambda x: x[1])[0]]
                            full_move_list.extend(local_moves)
                else:
                    pass

            # Else just append the move
            else:
                full_move_list.append(
                    [
                        move,
                    ]
                )

        # If there are no moves, return a list containing 'end turn'
        if not full_move_list:
            full_move_list = [["end turn"]]

        # Remove duplicates. Can happen if player has multiple development cards of the same type
        return_list = []
        for move in full_move_list:
            if move not in return_list:
                return_list.append(move)

        # Sort the list.
        # List is sorted so that 'build' comes before 'trade' in the list of possible moves, so that in the event of a
        # MiniMaxTimeOutException, the player will build before trading
        try:
            return_list.sort(key=lambda x: x[0])
        except:
            print("RETURN LIST")
            print(return_list)
            sys.exit()

        return return_list

    def minimax(self, interface, max_depth, alpha, beta, current_player) -> list:
        """
        Recursive Minimax algorithm
        Slightly based on my previous CE213 assignment
        NOTE: Maximum depth is the starting depth, and the score is increased. Imagine Maximum depth as the top of the
        tree, and the score is decremented to 0 each layer
        :param interface: The current state of the game
        :param max_depth: The maximum depth of the tree.
        :param alpha: The alpha value
        :param beta: The beta value
        :param current_player: The current player
        :return: A list pair containing the best move and the score of that move
        """

        # Check that the depth is correctly set
        if (
            max_depth == CONFIG["minimax_max_depth"]
            and self.number != current_player.number
        ):
            raise Exception("Cannot start minimax on opponent's turn")

        # Check if the time limit has been reached, and if so, return a MiniMaxTimeoutException
        if self.start_time + timedelta(seconds=self.time_limit) < datetime.now():
            # Recursively return if limit is reached
            self.log("Time limit reached")
            raise MiniMaxTimeoutException

        # Log the current depth
        self.log(f"Depth: {max_depth}, Maximising: {current_player.name}")

        # Check if the depth is at the maximum depth, and if so set the variables
        if max_depth == self.max_depth:
            self.root_score_map = []
            self.log("Resetting root_score_map")
            self.temp_score_variation_map = [0, {}]
            print(
                "There are "
                + str(len(self.get_move_combinations(interface, current_player)))
                + " possible moves at the top level"
            )

        if current_player.number == self.number:
            # It is the Minimax AI's turn
            max_combo = ["move_here", -math.inf]
            # Get all possible moves for this player
            potential_moves = self.get_move_combinations(
                interface, current_player
            )  # This line was changed from self to current_player
            # self.log(f"Potential moves: {potential_moves}")
            # If there are no moves, return the end turn move
            if not potential_moves:
                self.root_score_map.append(
                    [["end turn"], self.evaluate_board(interface)]
                )
                max_combo = [["end turn"], self.evaluate_board(interface)]

            # Else, for each move, perform the move and recursively call minimax
            else:
                for move in potential_moves:
                    # Create a clone of the interface and player so that the original is not modified
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(self)

                    # Perform the move
                    interface_clone = self.perform_minimax_move(
                        player_clone, interface_clone, move
                    )

                    # If the depth is at 0, evaluate the board and add the move and score to the list
                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    # Else, recursively call minimax with the new interface and player
                    else:
                        eval_combo = self.minimax(
                            interface_clone,
                            max_depth - 1,
                            alpha,
                            beta,
                            interface.get_next_player(current_player),
                        )
                    # If the depth is at the maximum depth (the top layer), add the move and score to the list as
                    # these are the immediate moves that can be made and need to be evaluated
                    if max_depth == self.max_depth:
                        self.root_score_map.append([move, eval_combo[1]])
                    max_combo = max(max_combo, eval_combo, key=lambda x: x[1])

                    # Perform alpha-beta pruning to speed up the algorithm
                    alpha = max(alpha, max_combo[1])
                    if beta <= alpha:
                        self.log(f"Pruning at depth {max_depth}")
                        break

            # If the depth is at the maximum depth, return the best move
            self.log(f"Max combo: {max_combo}")
            return max_combo

        else:
            # It is the opponent's turn
            # Perform the same as above, but with the opponent's player, and return the minimum score
            min_combo = ["move_here", math.inf]
            opposing_player = current_player  # THIS LINE WAS CHANGED FROM interface.get_next_player(current_player) TO current_player

            # Get all possible moves for this player
            potential_moves = self.get_move_combinations(interface, opposing_player)
            if not potential_moves:
                min_combo = [["end turn"], self.evaluate_board(interface)]

            else:
                # Else, for each move, perform the move and recursively call minimax
                for move in potential_moves:
                    # Create a clone of the interface and player so that the original is not modified
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(opposing_player)

                    interface_clone = self.perform_minimax_move(
                        player_clone, interface_clone, move
                    )

                    # If the depth is at 0, evaluate the board and add the move and score to the list
                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    else:
                        eval_combo = self.minimax(
                            interface_clone, max_depth - 1, alpha, beta, opposing_player
                        )

                    # If the depth is at the maximum depth (the top layer), add the move and score to the list as
                    min_combo = min(min_combo, eval_combo, key=lambda x: x[1])

                    # Perform alpha-beta pruning to speed up the algorithm
                    beta = min(beta, min_combo[1])
                    if beta <= alpha:
                        self.log(f"Pruning at depth {max_depth}")
                        break

                    # TODO - A note on imperfect information
                    # In a regular board game, you cannot see your opponent's hand.
                    # However, you can, in fact, keep an eye on which cards are given and played, as this is public
                    # information based on the dice roll. Given that it would be possible to keep track of this, I
                    # believe that it is fair to allow the minimax player to 'see' the opponents hand.

            # If the depth is at the maximum depth, return the best move
            self.log("Min combo: " + str(min_combo))
            return min_combo

    # noinspection DuplicatedCode
    def turn_actions(self, interface) -> None:
        """
        This function is called at the start of the player's turn. It is responsible for calling the minimax algorithm
        :param interface: The interface object
        :return: The move to be made
        """

        print("Beginning minimax")
        # Log that the minimax search has begun
        self.log(
            "\n\n$!\n\nBeginning minimax search on turn " + str(interface.turn_number)
        )
        self.log("Top level moves: " + str(self.get_move_combinations(interface, self)))
        # Set the start time
        self.start_time = datetime.now()
        self.log("Start time: " + str(self.start_time))
        # Run the minimax algorithm
        try:
            self.minimax(interface, self.max_depth, -math.inf, math.inf, self)
        # If the minimax algorithm times out, find the best move from the moves that have been evaluated
        except MiniMaxTimeoutException as e:
            self.log("MiniMaxTimeoutException: " + str(e))
            print("MiniMaxTimeoutException: " + str(e))
            time.sleep(1)
            if not self.root_score_map:
                # Not sure whether I like this? Potentially should search for other items
                print("No moves found, ending turn")
                time.sleep(5)
                raise endOfTurnException
        self.log("Root score map: " + str(self.root_score_map))
        # Find the best move from the moves that have been evaluated
        best_move_from_minimax = max(self.root_score_map, key=lambda x: x[1])
        best_move_from_minimax = {
            "move": best_move_from_minimax[0],
            "score": best_move_from_minimax[1],
        }
        # Print and log the best move
        print("Best move: ", best_move_from_minimax)
        self.log(
            "Best move: "
            + str(best_move_from_minimax["move"])
            + " with score "
            + str(best_move_from_minimax["score"])
        )
        # Log reasoning, which is the score variation map
        # Useful for debugging
        self.log("Reasoning: " + str(self.temp_score_variation_map))
        self.entire_game_moves.append(
            f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - {best_move_from_minimax}"
        )

        # Perform the best move
        best_move = best_move_from_minimax["move"]

        # Best move logic
        # Very similar to the logic in the minimax function but with a few differences

        if best_move[0] == "build road":
            interface.place_road(self, best_move[1])
        elif best_move[0] == "buy development card":
            interface.buy_development_card(self)
        elif best_move[0] == "trade with bank":
            interface.trade_with_bank(self, best_move[1], best_move[2])
        elif best_move[0] == "trade with port":
            interface.trade_with_port(self, best_move[1], best_move[2])
        elif best_move[0] == "build settlement":
            interface.place_settlement(self, best_move[1])
        elif best_move[0] == "build city":
            interface.place_city(self, best_move[1])
        elif best_move[0] == "play development card":
            if best_move[1] == "year of plenty":
                interface.play_development_card(
                    self, best_move[1], best_move[2], best_move[3]
                )
            elif best_move[1] == "monopoly":
                interface.play_development_card(self, best_move[1], best_move[2])
            else:
                interface.play_development_card(self, best_move[1])

        # Raise an exception to end the turn
        elif best_move[0] == "end turn":
            raise endOfTurnException
        else:
            print("Error: " + str(best_move))
            sys.exit()
