import random
import time

from ai_player import ai_player


class ai_random(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="random")

    def initial_placement(self, interface):
        accepted = False
        building = ""
        while accepted is False:

            rand_int = random.randint(0, len(interface.get_buildings_list()) - 1)
            if (
                (
                    interface.get_buildings_list()[
                        list(interface.get_buildings_list().keys())[rand_int]
                    ]["player"]
                    is None
                )
                and not (
                    any(
                        map(
                            str.isdigit,
                            list(interface.get_buildings_list().keys())[rand_int],
                        )
                    )
                )
                and not interface.check_for_nearby_settlements(
                    list(interface.get_buildings_list().keys())[rand_int]
                )
            ):
                accepted = True
                building = list(interface.get_buildings_list().keys())[rand_int]
                interface.place_settlement(self, building)
                potential_roads = []
                for road in interface.get_roads_list():
                    if building in road:
                        potential_roads.append(road)

                accepted_road = False
                while accepted_road is False:
                    rand_int = random.randint(0, len(potential_roads) - 1)
                    if (
                        interface.get_roads_list()[
                            list(interface.get_roads_list().keys())[rand_int]
                        ]["player"]
                        is None
                    ):
                        accepted_road = True
                        interface.place_road(self, potential_roads[rand_int])

        print(f"{self} has placed their initial settlement at {building}")

        return building

    def choose_road_location(self, interface):
        road_endings = []
        total_roads = 0
        for road in interface.get_roads_list():
            if interface.get_roads_list()[road]["player"] == self:
                total_roads += 1
                road_endings.append(road[0])
                road_endings.append(road[1])
        if total_roads == 15:
            return False
        not_accepted = True
        while not_accepted:
            rand_int = random.randint(0, len(interface.get_roads_list()) - 1)
            if (
                interface.get_roads_list()[
                    list(interface.get_roads_list().keys())[rand_int]
                ]["player"]
                is None
            ):
                if (
                    list(interface.get_roads_list().keys())[rand_int][0] in road_endings
                    or list(interface.get_roads_list().keys())[rand_int][1]
                    in road_endings
                ):
                    return list(interface.get_roads_list().keys())[rand_int]

    def choose_placement_location(self, interface, building_type="settlement"):

        settlements_count = 0
        cities_count = 0
        for building in interface.get_buildings_list():
            if interface.get_buildings_list()[building]["player"] == self:
                if interface.get_buildings_list()[building]["building"] == "settlement":
                    settlements_count += 1
                elif interface.get_buildings_list()[building]["building"] == "city":
                    cities_count += 1

        if building_type == "settlement":

            if settlements_count == 5:
                print(f"{self} has no more settlements to place")
                return False

            road_endings = []
            for road in interface.get_roads_list():
                if interface.get_roads_list()[road]["player"] == self:
                    if not interface.check_for_nearby_settlements(road[0]):
                        road_endings.append(road[0])
                    if not interface.check_for_nearby_settlements(road[1]):
                        road_endings.append(road[1])
            if len(road_endings) == 0:
                print(f"{self} has no places they can build settlements")
                return False
            not_accepted = True
            while not_accepted:
                time.sleep(0.1)
                rand_int = random.randint(0, len(road_endings) - 1)
                location = road_endings[rand_int]
                if interface.get_buildings_list()[location][
                    "player"
                ] is None and not interface.check_for_nearby_settlements(location):
                    return location

        elif building_type == "city":
            settlements = []
            for building in interface.get_buildings_list():
                if (
                    interface.get_buildings_list()[building]["player"] == self
                    and interface.get_buildings_list()[building]["building"]
                    == "settlement"
                ):
                    settlements.append(building)
            if len(settlements) == 0:
                return False
            not_accepted = True
            while not_accepted:
                rand_int = random.randint(0, len(settlements) - 1)
                location = settlements[rand_int]
                if (
                    interface.get_buildings_list()[location]["player"] == self
                    and interface.get_buildings_list()[location]["building"]
                    == "settlement"
                ):
                    return location

        else:
            print("Invalid building type")

    def play_development_card(self, interface):

        card = self.development_cards[
            self.development_cards.index(random.choice(self.development_cards))
        ]
        if card == "victory point":
            return
        else:
            print(f"{self} is playing a development card - {card}")
            if card == "soldier":
                if self.development_cards.count("soldier") > self.played_robber_cards:
                    self.robber(interface)
                    self.played_robber_cards += 1

            elif card == "monopoly":
                res_type = random.choice(["wheat", "sheep", "rock", "brick", "wood"])
                for other_player in interface.get_players_list():
                    if other_player != self:
                        while res_type in other_player.resources:
                            interface.return_player_card(other_player, res_type)
                            interface.give_player_card(self, "resource", res_type)
            elif card == "year of plenty":
                for i in range(2):
                    res_type = random.choice(
                        ["wheat", "sheep", "rock", "brick", "wood"]
                    )
                    interface.give_player_card(self, "resource", res_type)
            elif card == "road building":
                for i in range(2):
                    self.choose_road_location(interface)
            if not card == "soldier":
                interface.return_player_card(self, card)

    def robber(self, interface):
        tile_letters = []

        for tile in interface.get_tiles_list():
            if tile.resource != "desert":
                tile_letters.append(tile.letter)
        interface.move_robber(tile_letters[random.randint(0, len(tile_letters) - 1)])

        players_to_steal_from = []
        for key in interface.get_buildings_list():
            value = interface.get_buildings_list()[key]
            if (
                key.find(
                    [
                        tile_
                        for tile_ in interface.get_tiles_list()
                        if tile_.contains_robber
                    ][0].letter
                )
                != -1
            ):
                if (
                    value["player"] is not None
                    and value["player"] not in players_to_steal_from
                    and value["player"] != self
                ):
                    players_to_steal_from.append(value["player"])

        if len(players_to_steal_from) == 0:
            return
        if len(players_to_steal_from) == 1:
            player_to_steal_from = players_to_steal_from[0]
        else:
            player_to_steal_from = players_to_steal_from[
                random.randint(0, len(players_to_steal_from) - 1)
            ]
        interface.steal_from_player(player_to_steal_from, self)

    def robber_discard(self, interface):
        required_length = len(self.resources) // 2
        while len(self.resources) > required_length:
            rand_int = random.randint(0, len(self.resources) - 1)
            interface.return_player_card(self, self.resources[rand_int])

    def turn_actions(self, interface):

        no_place_to_build_settlement = False
        no_place_to_build_city = False
        no_place_to_build_road = False

        while True:

            possible_moves = interface.return_possible_moves(self)
            possible_moves.append("end turn")

            if len(possible_moves) == 0:
                print(f"{self} has no possible moves")
                break

            possible_moves = [random.choice(possible_moves)]

            if "build city" in possible_moves and not no_place_to_build_city:
                location = self.choose_placement_location(interface, "city")
                if location:
                    interface.place_city(self, location)
                    self.log_action("Built city at " + location)
                    self.entire_game_moves.append(
                        f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Built city at "
                        + location
                    )
                else:
                    no_place_to_build_city = True
                continue

            elif (
                "build settlement" in possible_moves
                and not no_place_to_build_settlement
            ):
                location = self.choose_placement_location(interface, "settlement")
                if location:
                    interface.place_settlement(self, location)
                    self.log_action("Built settlement at " + location)
                    self.entire_game_moves.append(
                        f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Built settlement at "
                        + location
                    )
                else:
                    no_place_to_build_settlement = True
                continue

            elif (
                "build road" in possible_moves
                and random.randint(0, 1) == 1
                and not no_place_to_build_road
            ):
                road = self.choose_road_location(interface)
                if road:
                    interface.place_road(self, road)
                    no_place_to_build_city = False
                    no_place_to_build_settlement = False
                    self.log_action("Built road at " + str(road))
                    self.entire_game_moves.append(
                        f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Built road at "
                        + str(road)
                    )
                else:
                    no_place_to_build_road = True
                continue

            elif "trade with bank" in possible_moves:
                interface.trade_with_bank(
                    self,
                    next(
                        card
                        for card in self.resources
                        if self.resources.count(card) >= 4
                    ),
                    random.choice(list(interface.get_resource_deck())),
                )
                self.log_action("Trade with bank - 4:1")
                self.entire_game_moves.append(
                    f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Trade with bank - 4:1"
                )
                continue

            elif (
                "play development card" in possible_moves and random.randint(0, 1) == 1
            ):
                self.play_development_card(interface)
                self.log_action("Played development card")
                self.entire_game_moves.append(
                    f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Played development card"
                )

            elif "buy development card" in possible_moves and random.randint(0, 2) == 1:
                interface.buy_development_card(self)
                self.log_action("Bought development card")
                self.entire_game_moves.append(
                    f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Bought development card"
                )

            elif "end turn" in possible_moves:
                self.log_action("Ended turn")
                self.entire_game_moves.append(
                    f"Turn {interface.turn}, VP {self.calculateVictoryPoints(interface)} - Ended turn"
                )
                break

            break
