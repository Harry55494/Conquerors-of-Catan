"""
Board Interface Class
Used to interact with the board object in a standardised way e.g. takes cards from a player
Prevents direct manipulation of the board object, and discrepancies between different implementations of the player actions

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

from src.board import *

import logging


class board_interface:
    board: board

    # Define moveNotValid Exception
    # Used to raise an error when a move is not valid
    class moveNotValid(Exception):
        def __init__(self, move: str):
            self.move = move
            self.message = f"The move {move} is not valid"
            super().__init__(self.message)
            raise self

    def __init__(self, players: list[player], game_number: list[int] = [0, 0]):
        """
        Initialises a board_interface object.
        Object is used to interact with the board object in a standardised way e.g. takes cards from a player
        Acts similarly to a board master
        :param players: A list of players
        """
        # Initialise board

        # Minimax mode is used to prevent the board from printing to the console
        self.minimax_mode = False

        # Setup mode is used to allow the placing of settlements and roads without the need for resources
        self.setup_mode = False

        # Define the board object
        self.board = board(board_type=CONFIG["board_layout"], players=players)
        self.turn_number = 0
        self.board.game_number = game_number

        self.all_players_ai = all(isinstance(player, ai_player) for player in players)
        self.board.all_players_ai = self.all_players_ai

        # Clear log file
        with open("logs/board_actions.log", "w") as f:
            pass

        # Setup logger, including formatting and file handler
        self.logger = logging.getLogger("board_interface" + str(game_number[0]))
        self.logger.setLevel(logging.DEBUG)
        file_format = logging.Formatter("[%(asctime)s] %(message)s")
        fh = logging.FileHandler("logs/board_actions.log")
        fh.setFormatter(file_format)
        self.logger.addHandler(fh)
        self.logger.debug("Board Interface created")

    def __eq__(self, other):
        """
        Checks if two board_interface objects are equal
        :param other: The other board_interface object
        :return: True if equal, false otherwise
        """
        players1 = self.board.players
        players2 = other.board.players
        if len(players1) != len(players2):
            print("Different number of players")
            return False
        players1.sort(key=lambda x: x.number)
        players2.sort(key=lambda x: x.number)
        for p1, p2 in zip(players1, players2):
            if p1 != p2:
                print("Players not equal")
                return False
            if p1.resources != p2.resources:
                print("Resources not equal")
                return False
            if p1.development_cards != p2.development_cards:
                print("Development cards not equal")
                return False
        for t1, t2 in zip(self.board.tiles, other.board.tiles):
            if t1 != t2:
                print("Tiles not equal")
                return False
        if self.board.resource_deck != other.board.resource_deck:
            print("Resource deck not equal")
            return False
        if self.board.development_card_deck != other.board.development_card_deck:
            print("Development deck not equal")
            return False
        for b1, b2 in zip(
            self.board._buildings.items(), other.board._buildings.items()
        ):
            for s1, s2 in zip(b1[1], b2[1]):
                if s1 != s2:
                    print("Buildings not equal")
                    return False
        return True

    def __deepcopy__(self, memodict={}):
        """
        Deep copies the board_interface object
        :param memodict: The memo dictionary
        :return: The deep copy
        """
        obj = pickle.loads(pickle.dumps(self, -1))
        obj.logger = logging.getLogger(
            "board_interface" + str(self.board.game_number[0])
        )
        return obj

    def log_action(self, action: str):
        """
        Logs an action to the file
        :param action: The action to log
        :return: None
        """
        self.logger.debug(f"[Turn: {str(self.turn_number).ljust(3)}] {action}")

    def set_minimax(self, state: bool):
        """
        Sets the minimax mode
        :param state: Set to true of false
        :return:
        """
        self.minimax_mode = state

    # Getters and Setters
    # Used to get and set the state of the board

    def get_resource_deck(self) -> list:
        """
        Gets the resource deck
        :return: The resource deck
        """
        return self.board.resource_deck

    def get_players_list(self) -> list[player]:
        """
        Gets the list of players
        :return: The list of players
        """
        return self.board.players

    def get_tiles_list(self) -> list[tile]:
        """
        Gets the list of tiles
        :return: The list of tiles
        """
        return self.board.tiles

    def get_buildings_list(self) -> dict:
        """
        Gets the dict of buildings
        This is a private variable, so this is the only method to access it
        :return: The dict of buildings
        """
        return self.board._buildings

    def get_roads_list(self) -> dict:
        """
        Gets the dict of roads
        Again, this is a private variable, so this is the only method to access it
        :return: The dict of roads
        """
        return self.board._roads

    def get_ports_list(self) -> dict:
        """
        Gets the dict of ports
        Again, this is a private variable, so this is the only method to access it
        :return: The dict of ports
        """
        return self.board._ports

    def get_building_cost_list(self) -> list:
        """
        Gets the list of building costs
        :return: The building cost list
        """
        return self.board.building_cost_list

    def get_largest_army(self) -> list:
        """
        Gets the largest army list
        :return: The largest army list
        """
        return self.board.largest_army

    def get_longest_road(self) -> list:
        """
        Gets the longest road list
        :return: The longest road list
        """
        return self.board.longest_road

    def get_robber_location(self) -> str:
        """
        Gets the location of the robber by searching through the tiles
        :return: The letter of the tile containing the robber
        """
        for tile in self.board.tiles:
            if tile.contains_robber:
                return tile.letter

    def get_next_player(self, current_player) -> player:
        """
        Gets the next player in the list of players
        Used by Minimax to get the next player
        Uses player numbers, so could be improved for when players are not in order
        :param current_player: The current player
        :return: The next player
        """
        if current_player.number == self.board.players[-1].number:
            # print("Returning first player")
            return self.board.players[0]
        else:
            # Find the player with matching number
            current_player_number = current_player.number
            for position, player in enumerate(self.board.players):
                if player.number == current_player_number:
                    return self.board.players[position + 1]

        # If the player is not found, raise an exception. This should never happen
        print(self.get_players_list())
        for player in self.get_players_list():
            print(player.number)
        raise Exception("Could not find next player")

    # Helper Functions

    def print_board(self, print_letters=False) -> None:
        """
        Calls the print_board function of the board object
        :param print_letters: Whether to print the letters on the board for placing settlements
        :return: None
        """
        self.board.print_board(print_letters)

    def has_potential_road(self, player_) -> bool:
        """
        Checks if the player has any potential places they can build a road
        :param player_: The player to check
        :return: Whether the number of potential roads is greater than 0
        """
        road_endings = []
        for road in self.board._roads:
            if self.board._roads[road]["player"] == player_:
                road_endings.append(road[0])
                road_endings.append(road[1])
        return len(road_endings) > 0

    def move_robber(self, location) -> None:
        """
        Moves the robber to the specified location
        :param location: The location to move the robber to
        :return: None
        """
        for tile_ in self.board.tiles:
            if tile_.contains_robber:
                tile_.contains_robber = False
            if tile_.letter == location:
                tile_.contains_robber = True

    def steal_from_player(
        self, player_to_steal_from: player, player_to_give_to: player
    ) -> None:
        """
        Steals a random card from one player and gives it to another
        Used when a player rolls a 7
        :param player_to_steal_from: The player to steal from
        :param player_to_give_to: The player to give the card to
        :return: None
        """
        if len(player_to_steal_from.resources) > 0:
            # Remove and give the card within the function
            card = player_to_steal_from.resources.pop(
                random.randint(0, len(player_to_steal_from.resources) - 1)
            )
            player_to_give_to.resources.append(card)
            self.log_action(
                f"{player_to_give_to.name} stole a {card} from {player_to_steal_from.name}"
            )
        else:
            # If the player has no cards, print a message
            # Shouldn't technically happen, but just in case
            print(f"{player_to_steal_from.name} has no cards to steal")
            self.log_action(f"{player_to_steal_from.name} has no cards to steal")

    def count_structure(self, player_, structure) -> int:
        """
        Counts the number of a certain structure a player has
        :param player_: The player to check
        :param structure: The structure to count
        :return: The number of that structure that the player has
        """
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

    def get_distance_between_nodes(self, node1, node2) -> int:
        """
        Returns the distance between two nodes using Dijkstra's algorithm
        :param node1: The first node
        :param node2: The second node
        :return: The distance between the two nodes
        """
        # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

        # Initialize the distances to be infinite
        nodes = self.board._buildings.keys()
        edges = self.board._roads.keys()
        distances = {}
        previous = {}
        for node in nodes:
            distances[node] = 1000000
            previous[node] = None
        distances[node1] = 0
        unvisited = list(nodes)

        # Iterate through the nodes
        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current)
            # If we've reached the second node, stop
            if current == node2:
                break
            # Otherwise, iterate through the edges
            for edge in edges:
                if current in edge:
                    neighbour = edge[0] if edge[1] == current else edge[1]
                    if neighbour in unvisited:
                        alt = distances[current] + 1
                        if alt < distances[neighbour]:
                            distances[neighbour] = alt
                            previous[neighbour] = current
        return distances[node2]

    def verify_game_integrity(self) -> None:
        """
        Check that the game is in a valid state
        :return: None
        """
        if (
            len(self.board.resource_deck)
            + sum([len(player_.resources) for player_ in self.board.players])
            != 95
        ):
            raise Exception("Resource card count is incorrect")
        if (
            len(self.board.development_card_deck)
            + sum([len(player_.development_cards) for player_ in self.board.players])
            != 25
        ):
            raise Exception("Development card count is incorrect")
        self.log_action("Cards are correct")

        if self == copy.deepcopy(self):
            self.log_action("Deepcopy Test Passed")
        else:
            raise Exception("Deepcopy Test Failed")

    # Moving Cards ----

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

        # Check if the card is a resource card
        if card_type == "resource" and not card == "desert":

            # Iterate through the amount of cards to be given
            for i in range(amount):
                try:
                    player_.resources.append(
                        self.board.resource_deck.pop(
                            self.board.resource_deck.index(card)
                        )
                    )
                # Exception if there are not enough cards in the bank
                except ValueError:
                    if not self.minimax_mode:
                        print("Not enough cards in the bank")

            # Log the action if not in minimax mode
            if not self.minimax_mode:
                self.log_action(
                    f"{player_.name} was given {amount} {card} from the bank"
                )

        # Check if the card is a development card
        elif card_type == "development":
            try:
                # Get a random development card from the bank
                card_given = self.board.development_card_deck.pop(0)
                player_.development_cards.append(card_given)

                # Log the action if not in minimax mode
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_.name} was given a {card_given} card from the bank"
                    )
                    self.log_action(
                        f"{player_.name} now has {len(player_.development_cards)} development cards"
                    )

                return card_given

            # Exception if there are not enough cards in the bank
            except IndexError:
                if not self.minimax_mode:
                    print("Not enough cards in the bank")
                return False

        # If the card is in neither of the above categories, print an error message
        else:
            print(f"Invalid card type - cannot give player {card}")
            time.sleep(5)

    def return_player_card(self, player_: player, card) -> None:
        """
        Returns a card to the bank
        :param player_: The player to take the card from
        :param card: The specific card, e.g. 'wheat' or 'soldier'
        :return: None
        """

        # Check if the card is a resource card
        if card in ["wheat", "wood", "clay", "sheep", "rock"]:
            # Remove the card from the player's hand and add it to the bank
            self.board.resource_deck.append(
                player_.resources.pop(player_.resources.index(card))
            )
            # Log the action if not in minimax mode
            if not self.minimax_mode:
                self.log_action(f"{player_.name} returned a {card} card to the bank")

        # Check if the card is a development card
        elif card in [
            "knight",
            "victory point",
            "road building",
            "year of plenty",
            "monopoly",
        ]:
            # Remove the card from the player's hand and add it to the bank
            self.board.development_card_deck.append(
                player_.development_cards.pop(player_.development_cards.index(card))
            )
            # Log the action if not in minimax mode
            if not self.minimax_mode:
                self.log_action(f"{player_.name} returned a {card} card to the bank")

        # If the card is in neither of the above categories, print an error message
        else:
            print(f"Invalid card type - cannot return {card} from player")
            time.sleep(5)

    def get_potential_building_locations(
        self, player_, building="settlement", initial_placement=False
    ):
        """
        Returns a list of potential locations for a building to be placed
        :param player_: The player who is placing the building
        :param building: The type of building to be placed - settlement or city
        :param initial_placement: Whether this is the initial setup phase
        :return: The list of potential locations
        """
        list = []

        # If the building is a settlement, check if the player has any roads to build on
        if building == "settlement":

            # If this is the initial placement, it doesn't matter if there are any roads, so just return any free locations that are not next to another settlement
            if initial_placement:
                for key, item in self.get_buildings_list().items():
                    if not self.get_buildings_list()[key]["building"]:
                        if not self.check_for_nearby_settlements(key):
                            list.append(key)

            # If this is not the initial placement, check if the player has any roads to build on
            else:
                for road in self.get_roads_list():
                    if self.get_roads_list()[road]["player"] is not None:
                        if (
                            self.get_roads_list()[road]["player"].number
                            == player_.number
                        ):
                            # For each end of the road, check if there is a settlement there already, and if not, add it to the list
                            if not self.check_for_nearby_settlements(road[0]):
                                list.append(road[0])
                            if not self.check_for_nearby_settlements(road[1]):
                                list.append(road[1])

        # If the building is a city, check if the player has any settlements to upgrade
        else:
            for key, item in self.get_buildings_list().items():
                if self.get_buildings_list()[key]["player"] is not None:
                    # Get the key of any settlements that belong to the player and add it to the list
                    if (
                        self.get_buildings_list()[key]["player"].number
                        == player_.number
                        and self.get_buildings_list()[key]["building"] == "settlement"
                    ):
                        list.append(key)
            if len(list) == 0:
                raise ValueError("No settlements to upgrade")

        return list

    def get_potential_road_locations(self, player_) -> list:
        """
        Returns a list of potential locations for a road to be placed
        :param player_: The player who is placing the road
        :return: A list of potential locations
        """
        road_endings = []
        # Get a list of all the roads the player has
        # For each road, add the two ends to the list if they are not already in it
        for road in self.get_roads_list():
            if self.get_roads_list()[road]["player"] is not None:
                if self.get_roads_list()[road]["player"].number == player_.number:
                    if road[0] not in road_endings:
                        road_endings.append(road[0])
                    if road[1] not in road_endings:
                        road_endings.append(road[1])

        list_ = []

        # For each road that contains the road ending, check if there is a road there already
        # If not, add it to the list
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

            # If the player has more robbers than the current largest army, set them as the new largest army
            if (player_.played_robber_cards > self.get_largest_army()[1]) and (
                player_.played_robber_cards >= 3
            ):
                # Update the largest army
                self.board.largest_army = [player_, player_.played_robber_cards]

                # Log the action if not in minimax mode
                if not self.minimax_mode:
                    print(
                        f"{player_} has the largest army with {player_.played_robber_cards} soldiers"
                    )
                    self.log_action(
                        f"{player_} has the largest army with {player_.played_robber_cards} soldiers"
                    )

        # Check for longest road

        for player_ in self.get_players_list():

            # Get a list of all the roads the player has
            player_roads = []
            for road in self.get_roads_list():
                if self.get_roads_list()[road]["player"] is not None:
                    if self.get_roads_list()[road]["player"].number == player_.number:
                        player_roads.append(road)

            # Find the clusters of roads
            clusters = return_clusters(player_roads)

            # If there are no clusters, continue
            if not any(len(cluster) >= 5 for cluster in clusters):
                continue

            # Get the current longest road
            current_longest_road = self.get_longest_road()

            # Get the length of the longest cluster
            max_cluster = len(find_longest_route(max(clusters, key=len))) - 1

            # If the longest cluster is longer than the current longest road, set it as the new longest road
            if max_cluster > current_longest_road[1] and max_cluster >= 5:

                # Update the longest road
                self.board.longest_road = [player_, max_cluster]

                # Log the action if not in minimax mode
                if not self.minimax_mode:
                    print(
                        f"{player_} has a road of length {max_cluster} and has been given the longest road card"
                    )
                    self.log_action(
                        f"{player_.name} has a road of length {max_cluster} and has been given the longest road card"
                    )

    def place_settlement(self, player_, location, setup=False) -> bool:
        """
        Places a settlement on the board
        :param player_: The player placing the settlement
        :param location: The location of the settlement
        :param setup: Whether the settlement is being placed in setup mode
        :return: Whether the settlement was placed
        """

        # Check if the player has any settlements left
        if self.count_structure(player_, "settlement") >= 5:
            print("You cannot build any more settlements")
            return False

        # Log the action if not in minimax mode
        if not self.minimax_mode and not setup:
            print(f"{player_.name} is placing a settlement")

        # Check if someone has already placed a settlement at the location
        if self.get_buildings_list()[location]["player"] is not None:
            raise self.moveNotValid("Settlement already placed at location")

        # If not in setup mode, check if the player has enough resources and take them
        # This is an example of me repeatedly checking whether they have the resources, as it is already checked
        # when finding the moves
        if not self.setup_mode:
            resources_taken = []
            try:
                for resource, amount in self.board.building_cost_list.get(
                    "settlement"
                ).items():
                    for j in range(amount):
                        self.return_player_card(player_, resource)
                        resources_taken.append(resource)
            except KeyError:
                # If the player does not have enough resources, return the resources taken
                for res in resources_taken:
                    self.give_player_card(player_, "resource", res)
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_.name} tried to place a settlement at {location} but did not have enough resources"
                    )
                return False

        # Update the board
        self.board._buildings[location].update(
            {"player": player_, "building": "settlement"}
        )

        # Log the action if not in minimax mode
        if not self.minimax_mode:
            player_.has_built_this_turn = True
            self.log_action(f"{player_.name} placed a settlement at {location}")

        # Check for ports and update them
        for entry in self.get_ports_list().keys():
            # If the port is not owned by anyone, check if the settlement is on it
            # Technically this is not needed as no player can even attempt to place a settlement on a port that someone
            # else has already built near
            if self.get_ports_list()[entry] is not None:
                if location in entry:
                    self.board._ports[entry].update({"player": player_})
                    if not self.minimax_mode:
                        self.log_action(f"{player_.name} has claimed a port at {entry}")

        return True

    def place_city(self, player_, location) -> bool:
        """
        Upgrades a settlement to a city
        :param player_: The player upgrading the settlement
        :param location: The location of the settlement to upgrade
        :return: Whether the settlement was upgraded
        """

        # Check if the player has any cities left
        if self.count_structure(player_, "city") >= 4:
            print("You cannot build any more cities")
            return False

        # Log the action if not in minimax mode
        if not self.minimax_mode:
            print(f"{player_.name} is placing a city")

        # Check that the settlement to upgrade is owned by the player
        if self.get_buildings_list()[location]["player"].number != player_.number:
            raise self.moveNotValid("Cannot upgrade a settlement that is not yours")

        # Check that the settlement to upgrade is actually a settlement
        if self.get_buildings_list()[location]["building"] != "settlement":
            raise self.moveNotValid(
                "Cannot upgrade a building that is not a settlement"
            )

        # Check if the player has enough resources and take them
        for resource, amount in self.board.building_cost_list.get("city").items():
            resources_taken = []
            try:
                for j in range(amount):
                    self.return_player_card(player_, resource)
                    resources_taken.append(resource)
            except KeyError:
                # If the player does not have enough resources, return the resources taken
                for res in resources_taken:
                    self.give_player_card(player_, "resource", res)
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_.name} tried to place a city at {location} but did not have enough resources"
                    )
                return False

        # Update the board
        self.board._buildings[location].update({"player": player_, "building": "city"})

        # Log the action if not in minimax mode
        if not self.minimax_mode:
            player_.has_built_this_turn = True
            self.log_action(f"{player_.name} placed a city at {location}")

        return True

    def place_road(self, player_, location, free_from_dev_card=False) -> bool:
        """
        Places a road on the board
        :param player_: The player placing the road
        :param location: The location of the road
        :param free_from_dev_card: Whether the road is being placed for free from a development card, and so does not cost resources
        :return: Whether the road was placed
        """
        # Check if the player has any roads left
        if self.count_structure(player_, "road") >= 15:
            if isinstance(player_, ai_player):
                if not self.minimax_mode:
                    print("You cannot build any more roads")
            return False

        if not location:
            self.log_action(f"{player_.name} tried to place a road at {location}")
            return False

        # Check if the road is already owned by someone
        if self.get_roads_list()[location]["player"] is not None:
            raise self.moveNotValid("Road already placed at location")

        try:

            # If not in setup mode, check if the player has enough resources and take them
            if not self.setup_mode:
                for resource, amount in self.board.building_cost_list.get(
                    "road"
                ).items():
                    # If the road is being placed for free from a development card, do not take resources
                    if not self.minimax_mode and not free_from_dev_card:
                        taken_resources = []
                        try:
                            for i in range(amount):
                                self.return_player_card(player_, resource)
                                taken_resources.append(resource)
                        except KeyError:
                            # If the player does not have enough resources, return them
                            for res in taken_resources:
                                self.give_player_card(player_, "resource", res)
                            if not self.minimax_mode:
                                self.log_action(
                                    f"{player_.name} tried to place a road at {location} but did not have enough resources"
                                )
                            return False

            # Place the road
            self.board._roads[location].update({"player": player_})

            # Log the action if not in minimax mode
            if not self.minimax_mode:
                player_.has_built_this_turn = True
                self.log_action(
                    f'{player_.name} placed a road at {location} {"(free from development card)" if free_from_dev_card else ""}'
                )

            # Update the special cards
            self.update_special_cards()

            return True

        except KeyError:
            raise self.moveNotValid("A road cannot be placed at this location")

    def buy_development_card(self, player_) -> bool:
        """
        Allows a player to buy a development card
        :param player_: The player buying the card
        :return: Whether the card was bought
        """

        # Check if the player has enough resources
        if (
            player_.count_cards("resources")["wheat"] >= 1
            and player_.count_cards("resources")["sheep"] >= 1
            and player_.count_cards("resources")["rock"] >= 1
        ):
            # Take the resources and give the player a development card
            if len(self.board.development_card_deck) > 0:
                self.return_player_card(player_, "wheat")
                self.return_player_card(player_, "sheep")
                self.return_player_card(player_, "rock")
                card = self.give_player_card(player_, "development", "development_card")

                # Log the action if not in minimax mode
                if not self.minimax_mode:
                    self.log_action(f"{player_.name} bought a development card")
                    self.log_action(
                        f"{player_.name}'s development cards are now {player_.development_cards}"
                    )
                player_.gained_dev_cards_this_turn.append(card)

                return True

            else:
                if not self.minimax_mode:
                    self.log_action("There are no development cards left")

        else:
            return False

    def trade_with_bank(self, player_, give, get) -> None:
        """
        Allows a player to trade with the bank, 4:1
        :param player_: The player trading
        :param give: The resource to be given
        :param get: The resource to be received
        :return: None
        """

        # Log the action if not in minimax mode
        if not self.minimax_mode:
            # Check if the player has already built this turn, if so they cannot trade with the bank
            if player_.has_built_this_turn:
                self.log_action(
                    f"{player_.name} cannot trade with the bank because they have already built this turn"
                )
                return

        # Check if the player has enough resources and take them
        if player_.count_cards("resources")[give] >= 4:
            if not self.minimax_mode:
                self.log_action(f"{player_.name} is trading 4x {give} for 1x {get}")
            # Take the resources and give the player the card
            for i in range(4):
                self.return_player_card(player_, give)
            self.give_player_card(player_, "resource", get)
        else:
            if not self.minimax_mode:
                print("Not enough resources to trade")

    def trade_with_port(self, player_, give, get) -> None:
        """
        Allows a player to trade with a port
        :param player_: The player trading
        :param give: The resource to be given
        :param get: The resource to be received
        :return:
        """

        # Log the action if not in minimax mode, and check if the player has already built this turn, if so they cannot trade with a port
        if not self.minimax_mode:
            if player_.has_built_this_turn:
                self.log_action(
                    f"{player_.name} cannot trade with a port because they have already built this turn"
                )
                return
            self.log_action(
                f"{player_.name} is attempting to use a port to trade {give} for {get}"
            )

        # Check the player owns the port
        for port in self.get_ports_list():
            if self.get_ports_list()[port] is not None:
                if self.get_ports_list()[port]["player"] is not None:
                    if self.get_ports_list()[port]["player"].number == player_.number:
                        # Player owns the port, now check if they have enough resources to trade
                        port_resource = self.get_ports_list()[port]["resource"]
                        # If the port is a 2:1 port, check if the player has enough resources to trade
                        if port_resource == give:
                            if player_.resources.count(give) >= 2:
                                # Player has enough resources, take them and give the player the card
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.give_player_card(player_, "resource", get)
                                # Log the action if not in minimax mode
                                if not self.minimax_mode:
                                    self.log_action(
                                        f"{player_.name} has used a port to trade 2x {give} for 1x {get}"
                                    )
                                return

                        # If the port is a 3:1 port, check if the player has enough resources to trade
                        elif port_resource == "any":
                            if player_.resources.count(give) >= 3:
                                # Player has enough resources, take them and give the player the card
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.return_player_card(player_, give)
                                self.give_player_card(player_, "resource", get)
                                # Log the action if not in minimax mode
                                if not self.minimax_mode:
                                    self.log_action(
                                        f"{player_.name} has used a port to trade 3x {give} for 1x {get}"
                                    )
                                return

        self.log_action(f"{player_.name} does not have enough resources to trade")

    def trade_with_player(
        self, original_player, player_to_trade_with, resource_to_give, resource_to_get
    ) -> None:
        """
        Allows a player to trade with another player
        Trades are always 1:1
        :param original_player: The player trading
        :param player_to_trade_with: The player to trade with
        :param resource_to_give: The resource to be given
        :param resource_to_get: The resource to be received
        :return: None
        """

        # Log the action if not in minimax mode, and check if the player has already built this turn, if so they cannot trade with another player
        if not self.minimax_mode:
            if original_player.has_built_this_turn:
                self.log_action(
                    f"{original_player.name} cannot trade with a player because they have already built this turn"
                )
                return
            print(
                f"{original_player.name} is offering to trade with {player_to_trade_with.name} - {resource_to_give} for {resource_to_get}"
            )
            self.log_action(
                f"{original_player.name} is offering to trade with {player_to_trade_with.name} - {resource_to_give} for {resource_to_get}"
            )

        # Check the players can trade what they want
        if (
            original_player.count_cards("resources")[resource_to_give] >= 1
            and player_to_trade_with.count_cards("resources")[resource_to_get] >= 1
        ):
            # Ask the other player if they want to trade
            result = player_to_trade_with.respond_to_trade(
                self, original_player, resource_to_give, resource_to_get
            )
            # If they do, perform the trade
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
                if not self.all_players_ai:
                    print(
                        f"{original_player.name} traded {resource_to_give} for {resource_to_get} with {player_to_trade_with.name}"
                    )
                    await_user_input()
            # If they don't, log the action if not in minimax mode
            else:
                if not self.minimax_mode:
                    self.log_action(
                        f"{player_to_trade_with.name} refused to trade with {original_player.name}"
                    )
                if not self.all_players_ai:
                    print(
                        f"{player_to_trade_with.name} refused to trade with {original_player.name}"
                    )
                    if not self.all_players_ai:
                        await_user_input()

        # If the players don't have enough resources to trade, log the action if not in minimax mode
        else:
            if not self.minimax_mode:
                print("One or both players do not have enough resources to trade!")
                if not self.all_players_ai:
                    await_user_input()

    def play_development_card(self, player_, card_to_play, *args) -> None:
        """
        Allows the player to play a development card
        :param player_: The player playing the card
        :param card_to_play: The card to be played
        :return: None
        """

        # Log the action if not in minimax mode, and check if the player has already played a development card this turn, if so they cannot play another
        if not self.minimax_mode:
            if player_.has_played_dev_card_this_turn:
                self.log_action(
                    f"{player_.name} has already played a development card this turn"
                )
                return
            self.log_action(f"{player_.name} is playing a {card_to_play}")

        dev_cards = player_.development_cards.copy()
        for card in player_.gained_dev_cards_this_turn:
            dev_cards.remove(card)

        if card_to_play not in dev_cards:
            self.log_action(
                f"{player_.name} attempted to play a {card_to_play} but could not as they gained it this turn"
            )
            return

        # Check the card the player wants to play
        card = card_to_play
        if card == "soldier":
            # Play the soldier card
            # Soldier cards stay in the players hand, so need to check that the player has not already played their soldier cards
            if player_.development_cards.count("soldier") > player_.played_robber_cards:
                player_.robber(self)
                # Increment the number of soldier cards the player has played
                player_.played_robber_cards += 1
                self.update_special_cards()

        # Play the monopoly card
        elif card == "monopoly":
            res_type = args[0]

            # Get every other player's resources of the type specified
            for other_player in self.get_players_list():
                if other_player != player_:
                    # While the other player has the resource type, take it from them and give it to the player
                    while res_type in other_player.resources:
                        self.return_player_card(other_player, res_type)
                        self.give_player_card(player_, "resource", res_type)

        # Play the year of plenty card
        elif card == "year of plenty":
            # Get the two resource types specified
            for i in range(2):
                res_type = args[i]
                self.give_player_card(player_, "resource", res_type)

        # Play the road building card
        elif card == "road building":
            for i in range(2):
                # Place the free road
                self.place_road(
                    player_, player_.choose_road_location(self), free_from_dev_card=True
                )

        # If the card is not a soldier card, return it to the player
        if card != "soldier":
            self.return_player_card(player_, card)

        # Log the action if not in minimax mode, and set the player's played dev card flag to true
        if not self.minimax_mode:
            player_.has_played_dev_card_this_turn = True

    # Turn Actions and Processing a Roll ---------------------------------------------------------

    def process_roll(self, roll, current_player: player) -> None:
        """
        Processes a roll of the dice and performs the necessary board actions
        :param current_player: The player who rolled the dice
        :param roll: The number from the dice roll
        :return: None
        """

        if isinstance(roll, list):
            self.board.current_roll = roll
            roll = sum(roll)
        else:
            self.board.roll = None

        # If the roll is a 7, the robber is rolled and the player must discard half their resources if they have more than 7
        if roll == 7:
            print("The robber has been rolled!")
            self.log_action("The robber has been rolled!")
            for player_ in self.get_players_list():
                if len(player_.resources) >= 7:
                    self.log_action(
                        f"{player_.name} must discard half their resources as they have more than 7"
                    )
                    player_.robber_discard(self)
            self.verify_game_integrity()
            self.log_action("Moving the robber...")
            current_player.robber(self)

            # If the player is an ai player, wait 3 seconds before continuing to allow the player to see the robber move
            if not isinstance(current_player, ai_player):
                time.sleep(3)

        # If the roll is not a 7, the player gets the resources from the tiles they have settlements on
        else:
            player_gained_resources = False
            # Get every building a player has
            for player_ in self.get_players_list():
                # Cards to give is a dictionary of the resources to give to the player, and the number of each resource
                # These are all added at the end
                cards_to_give = {}
                for building in self.get_buildings_list():
                    if self.get_buildings_list()[building].get("building") is not None:
                        tiles = self.get_buildings_list()[building].get("tiles")

                        # If the tiles near a building are the same as the roll, give the player the resources from the tiles
                        for building_tile in tiles:
                            if (
                                building_tile.dice_number == roll
                                and not building_tile.contains_robber
                            ):
                                # If the building is a settlement, give the player one of the resource
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
                                # If the building is a city, give the player two of the resource
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
                    if not self.all_players_ai:
                        print(
                            f"{player_} has gained {cards_to_give[card]} {card} card"
                            + ("s" if cards_to_give[card] > 1 else "")
                        )
                    self.give_player_card(
                        player_, "resource", card, cards_to_give[card]
                    )
                    player_gained_resources = True

            if not player_gained_resources and not self.all_players_ai:
                print("No resources were gained this turn")

    # Moves -------------------------------------------------------------------------------------------------------------

    def return_possible_moves(self, player_: player) -> list[str]:
        """
        Returns a list of possible moves for a given player
        Sometimes called multiple times in a turn if multiple moves are being made
        One of the biggest functions in the game
        :param player_: The player to check
        :return: A list of possible moves
        """

        # Initial counting of settlements and cities for future use
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

        # TRADING MOVES

        # If the player has not already built this turn, they can trade
        if not player_.has_built_this_turn:

            # Check if the player can trade with the bank
            for card in hand:
                if hand[card] >= 4:
                    moves.append("trade with bank")

            # Check if the player can trade with a port
            for port in self.get_ports_list():
                # Check if the port is owned by the player
                if self.get_ports_list()[port] is not None:
                    if self.get_ports_list()[port]["player"] is not None:
                        if (
                            self.get_ports_list()[port]["player"].number
                            == player_.number
                        ):
                            # Get the type of port and the resource it gives
                            type_ = self.get_ports_list()[port]["symbol"]
                            player_resources = player_.count_cards("resources")
                            port_resource = self.get_ports_list()[port]["resource"]
                            highest_resource = max(player_resources.values())
                            # If the player has enough of the resource, they can trade
                            if (
                                "2" in type_ and player_resources[port_resource] >= 2
                            ) or ("3" in type_ and highest_resource >= 3):
                                moves.append("trade with port")

            if (
                not isinstance(player_, ai_player)
                or isinstance(player_, ai_player)
                and not CONFIG["ai_doesnt_initiate_trades"]
            ):
                # Check if the player can trade with another player
                if len(player_.resources) > 0 and any(
                    len(other_player.resources) > 0
                    for other_player in self.get_players_list()
                    if other_player != player_
                ):
                    moves.append("trade with player")

        # BUILDING MOVES

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

        # DEVELOPMENT CARD MOVES

        # Check if the player can play a development card
        # Player can only play one development card per turn

        # Remove any cards that the player has gained this turn as per the rules
        dev_cards = player_.development_cards.copy()
        for card in player_.gained_dev_cards_this_turn:
            dev_cards.remove(card)

        if (
            len(dev_cards) > 0
            and len(dev_cards) > dev_cards.count("victory point")
            and not player_.has_played_dev_card_this_turn
        ):
            moves.append("play development card")

        # Player can always end their turn
        moves.append("end turn")

        sort_order = CONFIG["move_sort_order"]
        moves.sort(key=lambda move: sort_order.index(move))

        return moves

    # Initial Placement --------

    def initial_placement(self) -> None:
        """
        Sets up the board for the game, by allowing players to place their initial settlements and _roads, and then giving them the required cards
        Random placement is not true random - it will only place a settlement on a corner of a tile that will produce two or three resources, to help to avoid softlocks
        :return: None
        """

        # Get the order of players to place their settlements
        print("\n -- Board Setup --\n")
        self.log_action("Board Setup")
        self.setup_mode = True
        order = [player_ for player_ in self.get_players_list()]
        rev_order = order.copy()
        rev_order.reverse()
        order = order + rev_order

        # While there are still players to place their settlements, place their settlements
        while len(order) > 0:
            player_ = order.pop(0)
            print(f"{player_} is placing settlement number {2 - order.count(player_)}")

            if CONFIG["randomise_starting_locations"]:
                location = random.choice(
                    [
                        l
                        for l in self.get_buildings_list()
                        if self.get_buildings_list()[l]["building"] is None
                        and not self.check_for_nearby_settlements(l)
                    ]
                )
                road = random.choice(
                    [road for road in self.get_roads_list() if location in road]
                )
                print(f"Randomly placing settlement at {location}")
                self.board._buildings[location].update(
                    {"player": player_, "building": "settlement"}
                )
                self.board._roads[road].update({"player": player_, "road": "road"})
            else:
                # Get the location of the settlement and place it
                location = player_.initial_placement(self)
            print(f"{player_} has placed their settlement at {location}")
            if len(order) < len(self.board.players):
                # Players receive resources from their second settlement
                tiles_from_settlement = self.get_buildings_list()[location]["tiles"]
                for tile_ in tiles_from_settlement:
                    if not tile_.contains_robber:
                        self.give_player_card(player_, "resource", tile_.resource)

        # Set the setup mode to false and log the actions
        self.setup_mode = False
        self.log_action("Board Setup Complete")
