import random
import sys

from ai_player import ai_player

import time

import copy


class ai_minimax(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="minimax")

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

        score += interface.count_structure(self, "road") * 2

        # Number of resources player has access to -----------------------------
        # This is relative to the number of resources a player would get on a turn if every dice roll was rolled.

        # Higher numbers are less common, so they should be weighted more

        # rarity = board.calculate_resource_rarity()

        resources = []
        resources_has_access_to = []

        # Rating settlements and cities
        for key, item in interface.get_buildings_list().items():
            if interface.get_buildings_list()[key]["player"] == self:

                # Rate based on number of resources available
                if interface.get_buildings_list()[key]["building"] == "settlement":
                    resources.append(
                        item for item in interface.get_buildings_list()[key]["tiles"]
                    )
                    score += 10
                elif interface.get_buildings_list()[key]["building"] == "city":
                    resources.append(
                        item for item in interface.get_buildings_list()[key]["tiles"]
                    )
                    resources.append(
                        item for item in interface.get_buildings_list()[key]["tiles"]
                    )
                    score += 25

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

        # Rate higher if there is one of each tile nearby
        score += len(list(set(resources_has_access_to)))

        # Number of development cards ------------------------------------------

        score += len(self.development_cards) * 2
        if len(self.development_cards) >= 5:
            score -= max(0, len(self.development_cards) - 5) * 3
        score += self.played_robber_cards * 3

        # Potential to build something

        buildings_cost_list = interface.get_building_cost_list()
        for building in buildings_cost_list:
            if building != "development_card":
                resource_list = buildings_cost_list[building]
                for resource in resource_list:
                    if resource_list[resource] > 0:
                        if resource_list[resource] <= self.resources.count(resource):
                            score += 5

        return score

    def get_potential_building_locations(
        self, interface, building="settlement", initial_placement=False
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
                for key, item in interface.get_buildings_list().items():
                    if not interface.get_buildings_list()[key]["building"]:
                        if not interface.check_for_nearby_settlements(key):
                            list.append(key)
            else:
                for road in interface.get_roads_list():
                    if interface.get_roads_list()[road]["player"] == self:
                        if not interface.check_for_nearby_settlements(road[0]):
                            list.append(road[0])
                        if not interface.check_for_nearby_settlements(road[1]):
                            list.append(road[1])

        else:
            for key, item in interface.get_buildings_list().items():
                if (
                    interface.get_buildings_list()[key]["player"] == self
                    and interface.get_buildings_list()[key]["building"] == "settlement"
                ):
                    list.append(key)

        return list

    def get_potential_road_locations(self, interface):
        road_endings = []
        print(self)
        for road in interface.get_roads_list():
            if interface.get_roads_list()[road]["player"] is not None:
                if interface.get_roads_list()[road]["player"].number == self.number:
                    print("Road: ", road)
                    if road[0] not in road_endings:
                        road_endings.append(road[0])
                    if road[1] not in road_endings:
                        road_endings.append(road[1])

        print("Road endings: ", road_endings)

        list_ = []

        for road in interface.get_roads_list():
            for road_ending in road_endings:
                if road_ending in road:
                    if not interface.get_roads_list()[road]["player"]:
                        list_.append(road)

        print("List: ", list_)

        return list_

    def choose_road_location(self, interface):
        """
        Chooses the location of a road to be built
        :param interface:
        :return:
        """

        score_map = {}

        self.get_potential_road_locations(interface)

        for location in self.get_potential_road_locations(interface):
            interface_copy = copy.deepcopy(interface)
            interface_copy.set_minimax(True)
            player_copy = copy.deepcopy(self)
            interface_copy.place_road(player_copy, location)
            score_map[location] = self.evaluate_board(interface_copy)

        print("Score Map:" + str(score_map))

        return max(score_map, key=score_map.get)

    def initial_placement(self, interface):

        potential_locations = self.get_potential_building_locations(
            interface, initial_placement=True
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

        while len(self.resources) > 7:
            interface.return_player_card(
                self, self.resources[random.randint(0, len(self.resources) - 1)]
            )

        pass

    def minimax(self, interface, depth, max_depth):
        pass

    # noinspection DuplicatedCode
    def turn_actions(self, interface):

        potential_moves = interface.return_possible_moves(self)
        if not potential_moves:
            return
        print(potential_moves)

        # Append all combinations of moves to a list
        full_move_list = []
        for move in potential_moves:
            if move == "build settlement":
                for location in self.get_potential_building_locations(interface):
                    full_move_list.append(["build settlement", location])
            elif move == "build city":
                for location in self.get_potential_building_locations(
                    interface, "city"
                ):
                    full_move_list.append(["build city", location])
            elif move == "build road":
                for location in self.get_potential_road_locations(interface):
                    full_move_list.append(["build road", location])
            elif move == "trade with bank":
                resources_can_trade = list(
                    set(
                        [
                            resource
                            for resource in self.resources
                            if self.resources.count(resource) >= 4
                        ]
                    )
                )
                for resource in resources_can_trade:
                    for resource_to_get in ["clay", "rock", "sheep", "wheat", "wood"]:
                        if resource_to_get != resource:
                            full_move_list.append([move, resource, resource_to_get])
            elif move == "play development card":
                for card in self.development_cards:
                    if card == "soldier":
                        full_move_list.append([move, card])
                    elif card == "road building":
                        full_move_list.append([move, card])
                    elif card == "year of plenty":
                        for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                            for resource2 in ["clay", "rock", "sheep", "wheat", "wood"]:
                                full_move_list.append([move, card, resource, resource2])
                    elif card == "monopoly":
                        for resource in ["clay", "rock", "sheep", "wheat", "wood"]:
                            full_move_list.append([move, card, resource])
            else:
                full_move_list.append(
                    [
                        move,
                    ]
                )
        full_move_list.append(["end turn"])

        move_score_map = {}

        for move in full_move_list:
            interface_clone = copy.deepcopy(interface)
            interface_clone.set_minimax(True)
            self_clone = copy.deepcopy(self)

            if move[0] == "buy development card":
                interface_clone.buy_development_card(self_clone)
            elif move[0] == "play development card":
                if move[1] == "year of plenty":
                    interface_clone.play_development_card(
                        self_clone, move[1], move[2], move[3]
                    )
                elif move[1] == "monopoly":
                    interface_clone.play_development_card(self_clone, move[1], move[2])
                else:
                    interface_clone.play_development_card(self_clone, move[1])
            elif move[0] == "build road":
                interface_clone.place_road(self_clone, move[1])
            elif move[0] == "build settlement":
                interface_clone.place_settlement(self_clone, move[1])
            elif move[0] == "build city":
                interface_clone.build_city(self_clone, move[1])
            elif move[0] == "trade with bank":
                interface_clone.trade_with_bank(self_clone, move[1], move[2])
            elif move[0] == "end turn":
                pass

            move_score_map[str(move)] = {
                "score": self_clone.evaluate_board(interface_clone),
                "move": move,
            }

        print("\nMove score map: ")
        for move in move_score_map:
            print(move, move_score_map[move])
        for move in move_score_map:
            if move == "place settlement":
                time.sleep(10)
        best_move = max(move_score_map, key=lambda x: move_score_map[x]["score"])
        print("\nBest move: " + str(best_move))

        best_move = move_score_map[best_move]["move"]

        if best_move[0] == "build road":
            interface.place_road(self, best_move[1])
        elif best_move[0] == "buy development card":
            interface.buy_development_card(self)
        elif best_move[0] == "trade with bank":
            interface.trade_with_bank(self, best_move[1], best_move[2])
        elif best_move[0] == "build settlement":
            interface.place_settlement(self, best_move[1])
        elif best_move[0] == "build city":
            interface.build_city(self, best_move[1])
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
            sys.exit()
