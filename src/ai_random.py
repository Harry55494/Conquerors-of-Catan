"""
Random AI player
Makes random moves
All methods are overwritten from the parent class

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

import random
import time

from src.ai_player import *


class ai_random(ai_player):
    def __init__(self, number, colour):
        """
        Initialise the player
        :param number: The player number
        :param colour: The player colour
        """
        # Call the parent class constructor
        super().__init__(number=number, colour=colour, strategy="random")

    def initial_placement(self, interface) -> str:
        """
        Place the initial settlements and roads
        :param interface: The interface object
        :return: The building that was placed
        """
        accepted = False
        building = ""
        while accepted is False:
            # Choose a random building and make sure it is not already owned, and can be built next to
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
                # Build the settlement
                accepted = True
                building = list(interface.get_buildings_list().keys())[rand_int]
                interface.place_settlement(self, building, True)
                # Find the roads near the settlement
                potential_roads = []
                for road in interface.get_roads_list():
                    if building in road:
                        potential_roads.append(road)

                accepted_road = False
                while accepted_road is False:
                    # Pick a random road and make sure it is not already owned
                    rand_int = random.randint(0, len(potential_roads) - 1)
                    if (
                        interface.get_roads_list()[
                            list(interface.get_roads_list().keys())[rand_int]
                        ]["player"]
                        is None
                    ):
                        # Build the road
                        accepted_road = True
                        interface.place_road(self, potential_roads[rand_int])

        return building

    def choose_road_location(self, interface) -> str:
        """
        Choose a road location
        :param interface: The interface object
        :return: The road that was placed
        """
        # Get a list of all the roads that are owned by the player to know where they can build
        road_endings = []
        total_roads = 0
        for road in interface.get_roads_list():
            if interface.get_roads_list()[road]["player"] == self:
                total_roads += 1
                road_endings.append(road[0])
                road_endings.append(road[1])

        # If the player has no roads left to place, return False
        if total_roads == 15:
            return False
        not_accepted = True
        # Loop until accepted
        while not_accepted:
            # Choose a random road from all possible roads and make sure it is not already owned
            rand_int = random.randint(0, len(interface.get_roads_list()) - 1)
            if (
                interface.get_roads_list()[
                    list(interface.get_roads_list().keys())[rand_int]
                ]["player"]
                is None
            ):
                # Check if the road is connected to a road that the player owns
                if (
                    list(interface.get_roads_list().keys())[rand_int][0] in road_endings
                    or list(interface.get_roads_list().keys())[rand_int][1]
                    in road_endings
                ):
                    # Return the chosen road
                    return list(interface.get_roads_list().keys())[rand_int]

    def choose_placement_location(
        self, interface, building_type="settlement"
    ) -> str | bool:
        """
        Choose a placement location
        :param interface: The interface object
        :param building_type: The type of building to place
        :return: The building that was placed
        """

        # Check if the player has any settlements or cities left to place by counting the number of settlements and cities
        settlements_count = 0
        cities_count = 0
        for building in interface.get_buildings_list():
            if interface.get_buildings_list()[building]["player"] == self:
                if interface.get_buildings_list()[building]["building"] == "settlement":
                    settlements_count += 1
                elif interface.get_buildings_list()[building]["building"] == "city":
                    cities_count += 1

        if building_type == "settlement":

            # If the player has no settlements left to place, return False
            if settlements_count == 5:
                print(f"{self} has no more settlements to place")
                return False

            # Get a list of all the roads endings (junctions) that are owned by the player to know where they can build a settlement
            road_endings = []
            for road in interface.get_roads_list():
                if interface.get_roads_list()[road]["player"] == self:
                    if not interface.check_for_nearby_settlements(road[0]):
                        road_endings.append(road[0])
                    if not interface.check_for_nearby_settlements(road[1]):
                        road_endings.append(road[1])

            # If the player has no places they can build settlements, return False
            if len(road_endings) == 0:
                print(f"{self} has no places they can build settlements")
                return False

            # Wait until a valid location is found
            not_accepted = True
            while not_accepted:
                time.sleep(0.1)
                # Pick a random road ending and make sure it is not already owned, and can be built next to
                rand_int = random.randint(0, len(road_endings) - 1)
                location = road_endings[rand_int]
                if interface.get_buildings_list()[location][
                    "player"
                ] is None and not interface.check_for_nearby_settlements(location):
                    # Return the chosen location
                    return location

        elif building_type == "city":
            settlements = []

            # Find all the settlements that the player owns
            for building in interface.get_buildings_list():
                if (
                    interface.get_buildings_list()[building]["player"] == self
                    and interface.get_buildings_list()[building]["building"]
                    == "settlement"
                ):
                    settlements.append(building)

            # If the player has no settlements to upgrade, return False
            if len(settlements) == 0:
                return False

            # Wait until a valid location is found
            not_accepted = True
            while not_accepted:
                # Pick a random settlement and make sure it is owned by the player
                rand_int = random.randint(0, len(settlements) - 1)
                location = settlements[rand_int]
                if (
                    interface.get_buildings_list()[location]["player"] == self
                    and interface.get_buildings_list()[location]["building"]
                    == "settlement"
                ):
                    # Return the chosen location
                    return location

        else:
            print("Invalid building type")

    def offer_trade(self, interface) -> None:
        """
        Offer a trade
        :param interface: Interface object
        :return: None
        """
        # Choose a random player to trade with
        players = interface.get_players()
        players.remove(self)
        player = random.choice(players)

        # Choose a random resource to give
        giving = random.choice(list(interface.get_resources(self).keys()))

        # Choose a random resource to receive
        receiving = random.choice(list(interface.get_resources(player).keys()))

        # Offer the trade
        interface.offer_trade(self, player, giving, receiving)

    def respond_to_trade(self, interface, original_player, receiving, giving) -> bool:
        """
        Respond to a trade
        :param original_player: Original player
        :param receiving: The resource being received
        :param giving: The resource being given
        :return: True if accepted, False if rejected
        """
        return random.uniform(0, 1) > 0.5

    def play_development_card(self, interface) -> None:
        """
        Play a development card
        :param interface: Interface object
        :return: None
        """
        # Choose a random development card
        card = self.development_cards[
            self.development_cards.index(random.choice(self.development_cards))
        ]
        # If a victory point card is chosen, return
        if card == "victory point":
            return
        else:
            # Play the chosen card
            print(f"{self} is playing a development card - {card}")

            # Play a soldier card
            if card == "soldier":
                interface.play_development_card(self, "soldier")

            # Play a monopoly card, choosing a random resource type
            elif card == "monopoly":
                res_type = random.choice(["wheat", "sheep", "rock", "clay", "wood"])
                interface.play_development_card(self, "monopoly", res_type)

            # Play a year of plenty card, choosing two random resource types
            elif card == "year of plenty":
                res = []
                for i in range(2):
                    res.append(
                        random.choice(["wheat", "sheep", "rock", "clay", "wood"])
                    )
                interface.play_development_card(self, "year of plenty", res[0], res[1])

            # Play a road building card, choosing two random road locations
            elif card == "road building":
                interface.play_development_card(self, "road building")

    def robber(self, interface) -> None:
        """
        Move the robber and steal a resource from a player
        :param interface: Interface object
        :return: None
        """
        tile_letters = []

        # Get a list of all the tiles that are not desert tiles and choose a random one
        for tile in interface.get_tiles_list():
            if tile.resource != "desert":
                tile_letters.append(tile.letter)
        interface.move_robber(tile_letters[random.randint(0, len(tile_letters) - 1)])

        # Get a list of all the players that can be stolen from
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
                # If the building is a settlement, add the player to the list of players to steal from
                if (
                    value["player"] is not None
                    and value["player"] not in players_to_steal_from
                    and value["player"] != self
                ):
                    players_to_steal_from.append(value["player"])

        # If there are no players to steal from, return
        if len(players_to_steal_from) == 0:
            return
        # If there is only one player to steal from, steal from them
        if len(players_to_steal_from) == 1:
            player_to_steal_from = players_to_steal_from[0]
        # If there are multiple players to steal from, choose a random one
        else:
            player_to_steal_from = players_to_steal_from[
                random.randint(0, len(players_to_steal_from) - 1)
            ]
        # Steal a random resource from the chosen player
        interface.steal_from_player(player_to_steal_from, self)

    def robber_discard(self, interface) -> None:
        """
        Discard half of the player's resources
        :param interface: Interface object
        :return: None
        """
        # Randomly discard half of the player's resources
        required_length = len(self.resources) // 2
        while len(self.resources) > required_length:
            rand_int = random.randint(0, len(self.resources) - 1)
            interface.return_player_card(self, self.resources[rand_int])

    def turn_actions(self, interface) -> None:
        """
        Perform the player's turn actions
        :param interface: Interface object
        :return: None
        """

        # Variables used so that the player doesn't try to build a settlement, city or road if they can't and have already tried
        no_place_to_build_settlement = False
        no_place_to_build_city = False
        no_place_to_build_road = False

        while True:

            # Get possible moves
            possible_moves = interface.return_possible_moves(self)
            self.log(
                "Round "
                + str(interface.turn_number)
                + " Possible moves: "
                + str(possible_moves)
            )

            # If there are no possible moves, break
            if len(possible_moves) == 0:
                print(f"{self} has no possible moves")
                break

            # Choose a random move and log it
            chosen_move = [random.choice(possible_moves)]
            self.log(
                "Round "
                + str(interface.turn_number)
                + " Chosen move: "
                + str(chosen_move)
            )

            # If the chosen move is to build a city, build a city
            if "build city" in chosen_move and not no_place_to_build_city:
                # Choose a random settlement to upgrade to a city
                location = self.choose_placement_location(interface, "city")
                # Perform the upgrade
                if location:
                    interface.place_city(self, location)
                    self.log("Built city at " + location)
                    self.entire_game_moves.append(
                        f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Built city at "
                        + location
                    )
                else:
                    no_place_to_build_city = True
                continue

            # If the chosen move is to build a settlement, build a settlement
            elif "build settlement" in chosen_move and not no_place_to_build_settlement:
                # Choose a random location to build a settlement
                location = self.choose_placement_location(interface, "settlement")
                # Perform the build
                if location:
                    interface.place_settlement(self, location)
                    self.log("Built settlement at " + location)
                    self.entire_game_moves.append(
                        f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Built settlement at "
                        + location
                    )
                else:
                    no_place_to_build_settlement = True
                continue

            # If the chosen move is to build a road, build a road
            elif (
                "build road" in chosen_move
                and random.randint(0, 1) == 1
                and not no_place_to_build_road
            ):
                # Choose a random location to build a road
                road = self.choose_road_location(interface)
                # Perform the build
                if road:
                    interface.place_road(self, road)
                    no_place_to_build_city = False
                    no_place_to_build_settlement = False
                    # Log the build
                    self.log("Built road at " + str(road))
                    self.entire_game_moves.append(
                        f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Built road at "
                        + str(road)
                    )
                else:
                    no_place_to_build_road = True
                continue

            # If the chosen move is to trade with the bank, trade with the bank
            elif "trade with bank" in chosen_move:
                # Choose a random card that the player has at least 4 of
                interface.trade_with_bank(
                    self,
                    next(
                        card
                        for card in self.resources
                        if self.resources.count(card) >= 4
                    ),
                    # Choose a random card from the resource deck
                    random.choice(list(interface.get_resource_deck())),
                )
                # Log the trade
                self.log("Trade with bank - 4:1")
                self.entire_game_moves.append(
                    f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Trade with bank - 4:1"
                )
                continue

            # If the chosen move is to trade with a port, trade with a port
            elif "trade with port" in chosen_move:
                port_resources = get_port_combinations(interface, self)
                # If there are no resources to trade with the port, log it
                if len(port_resources) == 0:
                    self.log("No resources to trade with port - how did this happen?")
                else:
                    # Choose a random resource to trade with the port from the previously generated list
                    interface.trade_with_port(
                        self,
                        random.choice(port_resources),
                        random.choice(list(interface.get_resource_deck())),
                    )

            # Choose a random development card to play
            elif "play development card" in chosen_move and random.randint(0, 1) == 1:
                self.play_development_card(interface)
                self.log("Played development card")
                self.entire_game_moves.append(
                    f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Played development card"
                )

            # Choose to buy a random development card
            elif "buy development card" in chosen_move and random.randint(0, 2) == 1:
                interface.buy_development_card(self)
                self.log("Bought development card")
                self.entire_game_moves.append(
                    f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Bought development card"
                )

            # Choose to end the turn and raise an exception to end the turn
            elif "end turn" in chosen_move:
                self.log("Ended turn")
                self.entire_game_moves.append(
                    f"Turn {interface.turn_number}, VP {self.calculateVictoryPoints(interface)} - Ended turn"
                )
                raise endOfTurnException

            break
