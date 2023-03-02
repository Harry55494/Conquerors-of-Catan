import math
import random
from datetime import datetime, timedelta

from src.ai_player import *

import time

import copy


class MiniMaxTimeoutException(Exception):
    pass


def perform_minimax_move(player_clone, interface_clone, move):
    """
    Contains the logic for performing a move within a minimax search
    Performs a move within a minimax search, for a specific player
    :param player_clone:
    :param interface_clone:
    :return:
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
    elif move[0] == "end turn":
        pass
    return interface_clone


class ai_minimax(ai_player):
    def __init__(
        self,
        number,
        colour,
        time_limit=CONFIG["minimax_time_limit"],
        max_depth=CONFIG["minimax_max_depth"],
    ):
        super().__init__(number=number, colour=colour, strategy="minimax")
        self.log(
            "Minimax player created with time limit of "
            + str(time_limit)
            + " seconds and max depth of "
            + str(max_depth)
            + " levels"
        )
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.root_score_map = []
        self.start_time = None

    def evaluate_board(self, interface):
        """
        Heuristic function to evaluate the board state
        See README for more details of how the heuristic is calculated
        :param interface: board_interface
        :return: The evaluation of the board as an integer
        """

        score = 0

        # Victory Points ------------------------------------------------------

        current_vp = self.calculateVictoryPoints(interface)

        other_players = [
            player
            for player in interface.get_players_list()
            if player != self  # need to change this?
        ]
        other_players.sort(
            key=lambda x: x.calculateVictoryPoints(interface), reverse=True
        )

        score += current_vp * 10

        target_score = CONFIG["target_score"]

        if current_vp >= target_score:
            return 1000000
        if current_vp == target_score - 1:  # Bonus points for being close to winning
            score += 1000

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
        settlements_count = 0

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
                        if settlements_count >= 2:
                            score += 35
                        else:
                            settlements_count += 1
                    elif interface.get_buildings_list()[key]["building"] == "city":
                        resources.append(
                            item
                            for item in interface.get_buildings_list()[key]["tiles"]
                        )
                        resources.append(
                            item
                            for item in interface.get_buildings_list()[key]["tiles"]
                        )
                        score += 100

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

        # score += len(self.development_cards) if len(self.development_cards) < 5 else 5
        if len(self.development_cards) >= 2:
            score -= max(0, len(self.development_cards) - 2) * 10
        score += self.played_robber_cards * 3

        # Potential to build something

        buildings_cost_list = interface.get_building_cost_list()
        for building in buildings_cost_list:
            if building != "development_card":
                resource_list = buildings_cost_list[building]
                for resource in resource_list:
                    if resource_list[resource] > 0:
                        if resource_list[resource] <= self.resources.count(resource):
                            if CONFIG["minimax_max_depth"] == 0:
                                score += 2
                            else:
                                score += 0

        return score

    def choose_road_location(self, interface):
        """
        Chooses the location of a road to be built
        :param interface:
        :return:
        """

        score_map = {}

        self.log("Choosing road location")

        for location in interface.get_potential_road_locations(self):
            interface_copy = copy.deepcopy(interface)
            interface_copy.set_minimax(True)
            player_copy = copy.deepcopy(self)
            interface_copy.place_road(player_copy, location)
            score_map[location] = self.evaluate_board(interface_copy)

        self.log("Potential Roads Score Map: " + str(score_map))

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
            elif move == "end turn":
                pass
            else:
                full_move_list.append(
                    [
                        move,
                    ]
                )
        if not full_move_list:
            full_move_list = [["end turn"]]

        # List is sorted so that 'build' comes before 'trade' in the list of possible moves, so that in the event of a
        # MiniMaxTimeOutException, the player will build before trading
        full_move_list.sort(key=lambda x: x[0])

        return full_move_list

    def minimax(self, interface, max_depth, alpha, beta, current_player):

        if (
            max_depth == CONFIG["minimax_max_depth"]
            and self.number != current_player.number
        ):
            raise Exception("Cannot start minimax on opponent's turn")

        if self.start_time + timedelta(seconds=self.time_limit) < datetime.now():
            # Recursively return if limit is reached
            self.log("Time limit reached")
            raise MiniMaxTimeoutException

        self.log(f"Depth: {max_depth}, Maximising: {current_player.name}")
        if max_depth == self.max_depth:
            self.root_score_map = []

        if current_player.number == self.number:
            # It is the Minimax AI's turn
            max_combo = ["move_here", -math.inf]
            potential_moves = self.get_move_combinations(
                interface, current_player
            )  # This line was changed from self to current_player
            self.log(f"Potential moves: {potential_moves}")
            if not potential_moves:
                self.root_score_map.append(
                    [["end turn"], self.evaluate_board(interface)]
                )
                max_combo = [["end turn"], self.evaluate_board(interface)]

            else:
                for move in potential_moves:
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(self)

                    interface_clone = perform_minimax_move(
                        player_clone, interface_clone, move
                    )

                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    else:
                        eval_combo = self.minimax(
                            interface_clone,
                            max_depth - 1,
                            alpha,
                            beta,
                            interface.get_next_player(current_player),
                        )
                    if max_depth == self.max_depth:
                        self.root_score_map.append([move, eval_combo[1]])
                    max_combo = max(max_combo, eval_combo, key=lambda x: x[1])

                    alpha = max(alpha, max_combo[1])
                    if beta <= alpha:
                        self.log(f"Pruning at depth {max_depth}")
                        break

            self.log(f"Max combo: {max_combo}")
            return max_combo

        else:
            # It is the opponent's turn
            min_combo = ["move_here", math.inf]
            opposing_player = interface.get_next_player(current_player)
            potential_moves = self.get_move_combinations(interface, opposing_player)
            if not potential_moves:
                min_combo = [["end turn"], self.evaluate_board(interface)]

            else:
                for move in potential_moves:
                    interface_clone = copy.deepcopy(interface)
                    interface_clone.set_minimax(True)
                    player_clone = copy.deepcopy(opposing_player)

                    interface_clone = perform_minimax_move(
                        player_clone, interface_clone, move
                    )

                    if max_depth == 0:
                        eval_combo = [move, self.evaluate_board(interface_clone)]
                    else:
                        eval_combo = self.minimax(
                            interface_clone, max_depth - 1, alpha, beta, opposing_player
                        )
                    min_combo = min(min_combo, eval_combo, key=lambda x: x[1])

                    beta = min(beta, min_combo[1])
                    if beta <= alpha:
                        self.log(f"Pruning at depth {max_depth}")
                        break

                    # TODO - A note on imperfect information
                    # In a regular board game, you cannot see your opponent's hand.
                    # However, you can, in fact, keep an eye on which cards are given and played, as this is public
                    # information based on the dice roll. Given that it would be possible to keep track of this, I
                    # believe that it is fair to allow the minimax player to 'see' the opponents hand.

            self.log("Min combo: " + str(min_combo))
            return min_combo

    # noinspection DuplicatedCode
    def turn_actions(self, interface):

        print("Beginning minimax")
        self.log("\n\n\n\nBeginning minimax search on turn " + str(interface.turn))
        self.start_time = datetime.now()
        self.log("Start time: " + str(self.start_time))
        try:
            self.minimax(interface, self.max_depth, -math.inf, math.inf, self)
        except MiniMaxTimeoutException as e:
            self.log("MiniMaxTimeoutException: " + str(e))
            print("MiniMaxTimeoutException: " + str(e))
            time.sleep(1)
            if not self.root_score_map:
                return None
        self.log("Root score map: " + str(self.root_score_map))
        best_move_from_minimax = max(self.root_score_map, key=lambda x: x[1])
        best_move_from_minimax = {
            "move": best_move_from_minimax[0],
            "score": best_move_from_minimax[1],
        }
        print("Best move: ", best_move_from_minimax)
        self.log(
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
            raise endOfTurnException
        else:
            print("Error: " + str(best_move))
            sys.exit()
