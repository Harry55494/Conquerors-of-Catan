import math
import random
import sys
from CONFIG import CONFIG

import logging

from ai_player import *

import time

import copy


class ai_minimax(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="minimax")
        self.rootScores = []

    def evaluate_board(self, interface):
        """
        Heuristic function to evaluate the board state
        :param interface: boardInterface
        :return: The evaluation of the board as an integer
        """

        # NOTES
        # Main Score points should be based on the following:
        # 1. Victory Points - This contains the number of cities and settlements, so no need to calculate this as well
        # 2. Number of roads
        # 3. Number of resource player has access to
        # 4. Number of development cards
        # 5. Position of settlements and cities, based on scarcity of resources

        # Resources of other opponents
        # Resource Scarcity

        # No need to calculate the number of settlements and cities, as this is already calculated in the victory points
        # No need to calculate how many resource cards a player has in their hand, as this would suggest players to horde cards instead of spending

        score = 0

        # Victory Points ------------------------------------------------------

        current_vp = self.calculateVictoryPoints(interface)

        other_players = [
            player for player in interface.get_players_list() if player != self
        ]
        other_players.sort(
            key=lambda x: x.calculateVictoryPoints(interface), reverse=True
        )
        total_other_players_points = sum(
            [player.calculateVictoryPoints(interface) for player in other_players]
        )

        score += current_vp * 10

        if current_vp >= 10:
            return 1000000
        if current_vp == 9:  # Bonus points for being close to winning
            score += 50

        if current_vp > other_players[0].calculateVictoryPoints(interface):
            score += 50
        elif current_vp == other_players[0].calculateVictoryPoints(interface):
            score += 25

        # Number of roads -----------------------------------------------------

        score += interface.count_structure(self, "road") * 3.5

        # Number of resources player has access to -----------------------------
        # This is relative to the number of resources a player would get on a turn if every dice roll was rolled.

        # Higher numbers are less common, so they should be weighted more

        # rarity = board.calculate_resource_rarity()

        resources = []
        resources_has_access_to = []

        # Rating settlements and cities
        for key, item in interface.get_buildings_list().items():
            if interface.get_buildings_list()[key]["player"] is not None:
                if interface.get_buildings_list()[key]["player"].number == self.number:

                    # Rate based on number of resources available
                    if interface.get_buildings_list()[key]["building"] == "settlement":
                        resources.append(
                            item
                            for item in interface.get_buildings_list()[key]["tiles"]
                        )
                        score += 25
                    elif interface.get_buildings_list()[key]["building"] == "city":
                        resources.append(
                            item
                            for item in interface.get_buildings_list()[key]["tiles"]
                        )
                        resources.append(
                            item
                            for item in interface.get_buildings_list()[key]["tiles"]
                        )
                        score += 40

                    # Rate based on frequency of dice roll
                    score += (
                        sum(
                            [
                                tile.frequency
                                for tile in interface.get_buildings_list()[key]["tiles"]
                            ]
                        )
                        * 2
                    )

                    # Rate settlement higher if there are more tiles nearby
                    num_tiles = len(
                        [item for item in interface.get_buildings_list()[key]["tiles"]]
                    )
                    score += num_tiles * 2

                    # Rate higher if there is one of each tile nearby
                    nearby_resources = [
                        item for item in interface.get_buildings_list()[key]["tiles"]
                    ]
                    for resource in nearby_resources:
                        resources_has_access_to.append(resource.resource)

        score += len(resources)

        # Check for longest road
        if interface.get_longest_road()[0] is not None:
            if interface.get_longest_road()[0].number == self.number:
                score += 50
        if interface.get_largest_army()[0] is not None:
            if interface.get_largest_army()[0].number == self.number:
                score += 50

        # Rate higher if there is one of each tile nearby
        score += len(list(set(resources_has_access_to)))

        # Number of development cards ------------------------------------------

        score += len(self.development_cards) if len(self.development_cards) < 5 else 5
        if len(self.development_cards) >= 5:
            score -= max(0, len(self.development_cards) - 5) * 3
        score += self.played_robber_cards * 5

        # Potential to build something

        buildings_cost_list = interface.get_building_cost_list()
        for building in buildings_cost_list:
            if building != "development_card":
                resource_list = buildings_cost_list[building]
                for resource in resource_list:
                    if resource_list[resource] > 0:
                        if resource_list[resource] <= self.resources.count(resource):
                            score += 2

        return score

    def choose_road_location(self, interface):
        """
        Chooses the location of a road to be built
        :param interface:
        :return:
        """

        score_map = {}

        for location in interface.get_potential_road_locations(self):
            interface_copy = copy.deepcopy(interface)
            interface_copy.set_minimax(True)
            player_copy = copy.deepcopy(self)
            interface_copy.place_road(player_copy, location)
            score_map[location] = self.evaluate_board(interface_copy)

        return max(score_map, key=score_map.get)

    def initial_placement(self, interface):

        potential_locations = interface.get_potential_building_locations(
            self, initial_placement=True
        )

        location_score_map = {}
        for location in potential_locations:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            interface_clone.place_settlement(self, location)

            location_score_map[location] = self.evaluate_board(interface_clone)

        best_location = max(location_score_map, key=location_score_map.get)
        interface.place_settlement(self, best_location)

        road_score_map = {}

        for road in [
            road for road in interface.get_roads_list() if best_location in road
        ]:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            interface_clone.place_road(self, road)
            road_score_map[road] = self.evaluate_board(interface_clone)

        best_road = max(road_score_map, key=road_score_map.get)
        interface.place_road(self, best_road)

        return best_location

    def robber(self, interface):
        """
        Decide which player to rob.
        Currently DOES NOT use Minimax or heuristic
        :param interface:
        :return:
        """
        # TODO - Implement this properly
        potential_players = []
        for player in interface.get_players_list():
            if player.number != self.number:
                if len(player.resources) > 0:
                    potential_players.append(player)

        if len(potential_players) == 0:
            return None
        if len(potential_players) == 1:
            return potential_players[0]
        else:
            return max(potential_players, key=lambda x: len(x.resources))

    def robber_discard(self, interface):
        # TODO - Implement this properly
        required_length = len(self.resources) // 2
        while len(self.resources) > required_length:
            interface.return_player_card(
                self, self.resources[random.randint(0, len(self.resources) - 1)]
            )

    # Minimax functions --------------------------------------------------------

    def get_move_combinations(self, interface, player_):
        """
        Returns a list of all possible combinations of moves for the player
        :param interface: The current state of the game
        :return: A list of all possible combinations of moves for the player
        """
        potential_moves = interface.return_possible_moves(player_)
        if not potential_moves:
            return
        # print(potential_moves)

        # Append all combinations of moves to a list
        full_move_list = []
        for move in potential_moves:
            if move == "build settlement":
                for location in interface.get_potential_building_locations(player_):
                    full_move_list.append(["build settlement", location])
            elif move == "build city":
                for location in interface.get_potential_building_locations(
                    player_, "city"
                ):
                    full_move_list.append(["build city", location])
            elif move == "build road":
                for location in interface.get_potential_road_locations(player_):
                    full_move_list.append(["build road", location])
            elif move == "trade with bank":
                resources_can_trade = list(
                    set(
                        [
                            resource
                            for resource in player_.resources
                            if player_.resources.count(resource) >= 4
                        ]
                    )
                )
                for resource in resources_can_trade:
                    for resource_to_get in ["clay", "rock", "sheep", "wheat", "wood"]:
                        if resource_to_get != resource:
                            full_move_list.append([move, resource, resource_to_get])
            elif move == "play development card":
                if self.number == player_.number:
                    # Development cards are private information
                    for card in player_.development_cards:
                        if (
                            card == "soldier"
                            and player_.development_cards.count("soldier")
                            > player_.played_robber_cards
                        ):
                            full_move_list.append([move, card])
                        elif card == "road building":
                            full_move_list.append([move, card])
                        elif card == "year of plenty":
                            for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                                for resource2 in [
                                    "clay",
                                    "rock",
                                    "sheep",
                                    "wheat",
                                    "wood",
                                ]:
                                    full_move_list.append(
                                        [move, card, resource, resource2]
                                    )
                        elif card == "monopoly":
                            for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                                full_move_list.append([move, card, resource])
                else:
                    pass
            else:
                full_move_list.append(
                    [
                        move,
                    ]
                )
        full_move_list.append(["end turn"])
        return full_move_list

    def estimate_opponents_moves(self, interface, player_to_estimate):
        """
        Estimates the moves of an opponent player
        :param interface: The current state of the game
        :param player_to_estimate: The player to estimate the moves of
        :return:
        """

        potential_moves = interface.get_possible_moves(player_to_estimate)

        opp_hand_length = len(player_to_estimate.resources)
        opp_dev_card_length = len(player_to_estimate.development_cards)

        if opp_hand_length >= 3:
            potential_moves.append(["buy development card"])
        if opp_dev_card_length > 0:
            move = "play development card"
            for card in ["soldier", "road building", "year of plenty", "monopoly"]:
                if card == "soldier":
                    potential_moves.append([move, card])
                elif card == "road building":
                    potential_moves.append([move, card])
                elif card == "year of plenty":
                    for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                        for resource2 in ["clay", "rock", "sheep", "wheat", "wood"]:
                            potential_moves.append([move, card, resource, resource2])
                elif card == "monopoly":
                    for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                        potential_moves.append([move, card, resource])
        if opp_hand_length >= 2:
            for position in interface.get_potential_road_locations(player_to_estimate):
                potential_moves.append(["build road", position])
        if opp_hand_length >= 4:
            for position in interface.get_potential_building_locations(
                player_to_estimate
            ):
                potential_moves.append(["build settlement", position])
            for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                for resource2 in ["clay", "rock", "sheep", "wheat", "wood"]:
                    if resource != resource2:
                        potential_moves.append(["trade with bank", resource, resource2])
        if opp_hand_length >= 5:
            for position in interface.get_potential_building_locations(
                player_to_estimate, "city"
            ):
                potential_moves.append(["build city", position])

        return potential_moves

    def better_minimax(self, interface, max_depth, alpha, beta, maximizingPlayer):

        self.log_action(f"Depth: {max_depth}, Maximising: {maximizingPlayer}")

        if maximizingPlayer:
            # It is the Minimax AI's turn
            max_combo = ["move_here", -math.inf]
            potential_moves = self.get_move_combinations(interface, self)
            if not potential_moves:
                max_combo = [["end turn"], self.evaluate_board(interface)]

            else:
                for move in potential_moves:
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(self)

                    if move[0] == "buy development card":
                        interface_clone.buy_development_card(player_clone)
                    elif move[0] == "play development card":
                        if move[1] == "year of plenty":
                            interface_clone.play_development_card(
                                player_clone, move[1], move[2], move[3]
                            )
                        elif move[1] == "monopoly":
                            interface_clone.play_development_card(
                                player_clone, move[1], move[2]
                            )
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
                    elif move[0] == "end turn":
                        pass

                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    else:
                        eval_combo = self.better_minimax(
                            interface_clone, max_depth - 1, alpha, beta, False
                        )
                    max_combo = max(max_combo, eval_combo, key=lambda x: x[1])

                    alpha = max(alpha, max_combo[1])
                    if beta <= alpha:
                        self.log_action(f"Pruning at depth {max_depth}")
                        break

            self.log_action(f"Max combo: {max_combo}")
            return max_combo

        if not maximizingPlayer:
            # It is the opponent's turn
            min_combo = ["move_here", math.inf]
            opposing_player = interface.get_opposing_player(self)
            potential_moves = self.get_move_combinations(interface, opposing_player)
            if not potential_moves:
                min_combo = [["end turn"], self.evaluate_board(interface)]

            else:
                for move in potential_moves:
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(opposing_player)

                    if move[0] == "buy development card":
                        interface_clone.buy_development_card(player_clone)
                    elif move[0] == "play development card":
                        if move[1] == "year of plenty":
                            interface_clone.play_development_card(
                                player_clone, move[1], move[2], move[3]
                            )
                        elif move[1] == "monopoly":
                            interface_clone.play_development_card(
                                player_clone, move[1], move[2]
                            )
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
                    elif move[0] == "end turn":
                        pass

                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    else:
                        eval_combo = self.better_minimax(
                            interface_clone, max_depth - 1, alpha, beta, True
                        )
                    min_combo = min(min_combo, eval_combo, key=lambda x: x[1])

                    beta = min(beta, min_combo[1])
                    if beta <= alpha:
                        self.log_action(f"Pruning at depth {max_depth}")
                        break

                    # TODO - A note on imperfect information
                    # In a regular board game, you cannot see your opponent's hand.
                    # However, you can, in fact, keep an eye on which cards are given and played, as this is public
                    # information based on the dice roll. Given that it would be possible to keep track of this, I
                    # believe that it is fair to allow the minimax player to 'see' the opponents hand.

            self.log_action("Min combo: " + str(min_combo))
            return min_combo

    # noinspection DuplicatedCode
    def turn_actions(self, interface):

        print("Beginning minimax")
        self.log_action("\n\nBeginning minimax search on turn " + str(interface.turn))
        best_move_from_minimax = self.better_minimax(
            interface, CONFIG["minimax_max_depth"], -math.inf, math.inf, True
        )
        best_move_from_minimax = {
            "move": best_move_from_minimax[0],
            "score": best_move_from_minimax[1],
        }
        print("Best move: ", best_move_from_minimax)
        self.log_action(
            "Best move: "
            + str(best_move_from_minimax["move"])
            + " with score "
            + str(best_move_from_minimax["score"])
        )
        self.entire_game_moves.append(
            f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - {best_move_from_minimax}"
        )

        best_move = best_move_from_minimax["move"]

        if best_move[0] == "build road":
            interface.place_road(self, best_move[1])
        elif best_move[0] == "buy development card":
            interface.buy_development_card(self)
        elif best_move[0] == "trade with bank":
            interface.trade_with_bank(self, best_move[1], best_move[2])
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
        elif best_move[0] == "end turn":
            pass
        else:
            print("Error: " + str(best_move))
            sys.exit()
