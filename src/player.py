"""
Player class
Contains the default implementations of all required methods, which are all overridden by the AI class
Implementations all require human input

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""
import sys

import termcolor
from src.CONFIG import CONFIG

# Exception to be raised when a player ends their turn
# This is a hack to break out of the loop in the game class
class endOfTurnException(Exception):
    pass


def await_user_input(prompt="Press any key to continue..."):
    input(prompt)


class player:
    """
    Player class
    Implements player specific functions for the board.
    """

    def __init__(self, number, colour):
        """
        Initialises a player object
        :param number: The player number
        :param colour: The colour of the player
        """
        # Sets all the variables
        self.number = number
        self.colour = colour
        self.name = "Player " + str(number)
        self.coloured_name = termcolor.colored(self.name, self.colour)
        self.victory_points = 0
        self.resources = []
        self.development_cards = []
        self.played_robber_cards = 0
        self.has_built_this_turn = False
        self.has_played_dev_card_this_turn = False
        print(self.coloured_name, "has joined the game")

    def __str__(self) -> str:
        """
        Returns the coloured player's name
        :return: The player's name
        """
        return f"{self.coloured_name}  (Human)"

    def __eq__(self, other) -> bool:
        """
        Checks if two players are the same
        :param other: The other player
        :return: True if they are the same, False otherwise
        """
        if not isinstance(other, player):
            return False
        return self.number == other.number

    def count_cards(self, card_type) -> dict:
        """
        Counts the number of each card in the player's hand
        :param card_type: The type of card to count, either "resource" or "development"
        :return: The number of each card
        """
        card_count = {}

        # Get the card list
        if card_type in ["resource", "resources"]:
            list_ = self.resources
            for resource in ["wheat", "wood", "sheep", "clay", "rock"]:
                card_count[resource] = 0
        else:
            list_ = self.development_cards

        # Count the cards
        for card in list_:
            if card in card_count:
                card_count[card] += 1
            else:
                card_count[card] = 1

        return card_count

    def printHand(self, type_="resources") -> None:
        """
        Prints the player's hand of either resource cards or development cards
        :return: None
        """
        # Get the card list and sort it
        if type_ in ["resource", "resources"]:
            list_to_print = self.resources
        else:
            list_to_print = self.development_cards
        list_to_print.sort()

        print(
            f"{'You'} ({self.coloured_name}) have {len(list_to_print)} {type_} card(s) in your hand.",
            end="",
        )
        # If the list is not empty, print the cards
        if len(list_to_print) > 0:
            print(" They are:")
            card_count = self.count_cards(type_)
            # Print each card and its count
            for card in card_count:
                print(f"{card_count[card]} x {card} ", end=" ")
            print("")
        else:
            print("")
        self.resources.sort()
        self.development_cards.sort()

    def calculateVictoryPoints(
        self, interface, output=False, buildings_list=None
    ) -> int:
        """
        Calculates the player's victory points, from both their settlements/cities and their development cards
        :param buildings_list:
        :param output: Whether to print the victory points
        :param interface: The interface, so that _buildings can be checked
        :return: The player's victory points
        """
        self.victory_points = 0
        sources = {
            "settlements": 0,
            "cities": 0,
            "development cards": 0,
            "longest_road": 0,
            "largest_army": 0,
        }

        # Get the buildings list
        if buildings_list is None:
            buildings_list = interface.get_buildings_list()

        # Count the number of settlements and cities, and add the victory points
        for building in buildings_list:
            if buildings_list[building] is not None:
                if buildings_list[building].get("player") == self:
                    if buildings_list[building].get("building") == "settlement":
                        self.victory_points += 1
                        sources["settlements"] += 1
                    elif buildings_list[building].get("building") == "city":
                        self.victory_points += 2
                        sources["cities"] += 1
        # Count the number of development cards that are victory points, and add the victory points
        for card in self.development_cards:
            if card == "victory point":
                self.victory_points += 1
                sources["development cards"] += 1
        # Check if the player has the largest army or longest road, and add the victory points
        if interface.get_largest_army()[0] == self:
            self.victory_points += 2
            sources["largest_army"] += 1
        # Check if the player has the longest road, and add the victory points
        if interface.get_longest_road()[0] == self:
            self.victory_points += 2
            sources["longest_road"] += 1

        # If output is True, print the victory points
        if output:
            print(f"Player has {self.victory_points} victory points")
            for source in sources:
                # If a source has any victory points, print it
                if sources[source] > 0:
                    print(f"{source}: {sources[source]}")
                    # Also print the development cards if the source is development cards
                    if source == "development cards":
                        self.printHand("development cards")

        return self.victory_points

    # Placing Roads and Settlements ------------------------------------------------

    def choose_placement_location(self, interface, type_="settlement") -> str:
        """
        Chooses a place on the board to place a settlement or city
        :param interface:
        :param type_: The type of building to place
        :return: The location of the building
        """

        # Print the board
        interface.print_board(print_letters=True)
        accepted, location = False, ""

        # Keep asking for a location until a valid one is given
        while not accepted:
            location = input(
                f"{self} , where would you like to place your {type_}? "
                f"\nPlease enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners"
                f"\n(Single corner numbers increase as you move clockwise around a tile)\n"
            )
            # Make the location lowercase and split it into a list, then sort it to make it easier to check
            letters = location.lower()
            if "," in location:
                letters = location.split(",")
            # check for number references
            if not any([letter.isdigit() for letter in letters]):
                letters = [letter.strip() for letter in letters]
                letters.sort()
                location = ",".join(letters)

            # Check if the location is valid and not already occupied
            if location in interface.get_buildings_list():
                if (
                    interface.get_buildings_list()[location]["player"] is None
                    or interface.get_buildings_list()[location]["player"] == self
                    and type_ == "settlement"
                ) and not interface.check_for_nearby_settlements(location):
                    # If the location is valid and not already occupied, accept it
                    accepted = True
                else:
                    print("That location is already occupied!")
            else:
                print("That is not a valid location!")

        # Return the location for whatever is calling this function
        return location

    def choose_road_location(
        self, interface, requirement=None, ignore_current_endings=True
    ) -> tuple:
        """
        Places a road on the board for a player
        :param interface: The interface, so that the board can be printed
        :param requirement: The location that the road must start at, if any
        :param ignore_current_endings: Whether to ignore the current road endings
        :return: The location of the road
        """

        # Get the current road endings
        # Roads need to connect to a current road ending
        current_road_endings = []
        for tuple_, details in interface.get_roads_list().items():
            if details["player"] == self:
                current_road_endings.append(tuple_[0])
                current_road_endings.append(tuple_[1])

        # Print the board
        interface.print_board(print_letters=True)

        accepted = False
        while not accepted:
            coordinates = []
            # If a requirement is given, add it to the coordinates
            if requirement is not None:
                coordinates.append(requirement)
            # Keep asking for a location until two valid locations are in the list
            while len(coordinates) < 2:
                print(
                    f"{self} , where would you like to place the "
                    + ("start" if len(coordinates) == 0 else "end")
                    + " of your road?"
                    f"\nPlease enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners"
                )
                # If a requirement is given, print it out
                if requirement is not None:
                    print(f"Your road must connect to {requirement}")
                # Get the location
                location = input(
                    f"Please enter the {len(coordinates) + 1}{'st' if len(coordinates) + 1 == 1 else 'nd'} location\n"
                )

                # Make the location lowercase and split it into a list, then sort it to make it easier to check
                letters = location.lower()
                if "," in location:
                    letters = location.split(",")
                # check for number references
                if not any([letter.isdigit() for letter in letters]):
                    letters = [letter.strip() for letter in letters]
                    letters.sort()
                    location = ",".join(letters)
                coordinates.append(location)

            # Check if the location is valid and not already occupied
            if tuple(coordinates) not in interface.get_roads_list():
                coordinates = coordinates[::-1]
            coordinates = tuple(coordinates)

            if coordinates in interface.get_roads_list():
                if interface.get_roads_list()[coordinates]["player"] is None:
                    if (
                        ignore_current_endings
                        or (coordinates[0] in current_road_endings)
                        or (coordinates[1] in current_road_endings)
                    ):
                        # If the location is valid and not already occupied, accept it and return the coordinates
                        return coordinates
                else:
                    print("That location is already occupied!")
            else:
                print("That is not a valid location!")

    def initial_placement(self, interface) -> str:
        """
        Places the initial settlements and roads for a player
        Simply calls the choose_placement_location and choose_road_location functions
        :param interface: The interface, so that the board can be printed
        :return: The location of the first settlement
        """
        building = self.choose_placement_location(interface, "settlement")
        interface.place_settlement(self, building, True)
        interface.place_road(self, self.choose_road_location(interface, building, True))
        return building

    # Turn Functions ------------------------------------------------

    def robber(self, interface) -> None:
        """
        Perform the robber actions for a player
        :param interface:
        :return: None
        """
        # Print the board
        interface.print_board(print_letters=True)
        print(f"{self}, has rolled the robber!")
        print(f"{self}, where would you like to move the robber?")
        accepted = False
        # Wait for a valid location to be given
        while not accepted:
            location = input(
                "Please enter the letter of the tile you would like to move the robber to\n"
            )
            location = location.lower()
            if any([tile_.letter == location for tile_ in interface.get_tiles_list()]):
                accepted = True
                interface.move_robber(location)
            else:
                print("Invalid location!")

        # Move the robber to the given location
        new_robber_location = [
            tile_ for tile_ in interface.get_tiles_list() if tile_.contains_robber
        ][0]

        # Get a list of players that can be stolen from
        players_to_steal_from = []
        for key in interface.get_buildings_list():
            value = interface.get_buildings_list()[key]
            if key.find(new_robber_location.letter) != -1:
                if (
                    value["player"] is not None
                    and value["player"] not in players_to_steal_from
                    and value["player"] != self
                ):
                    players_to_steal_from.append(value["player"])

        singular_player_to_steal_from = None

        # If there are multiple players to steal from, ask which one to steal from
        if len(players_to_steal_from) > 1:
            print("Please select a player to steal from")
            print(player_item for player_item in players_to_steal_from)
            player_nums = [
                int(player_item.number) for player_item in players_to_steal_from
            ]
            # Perform regular waiting
            accepted = False
            while not accepted:
                choice = input(
                    "Please enter the number of the player you would like to steal from\n"
                )
                if choice.isdigit() and int(choice) in player_nums:
                    accepted = True
                    for player_ in players_to_steal_from:
                        if player_.number == int(choice):
                            singular_player_to_steal_from = player_
                else:
                    print("Invalid choice")
        # If there is only one player to steal from, steal from them
        elif len(players_to_steal_from) == 1:
            singular_player_to_steal_from = players_to_steal_from[0]
        # If there are no players to steal from, print that
        else:
            print("No players to steal from")
            await_user_input()

        # If a player was chosen to steal from, steal from them
        if singular_player_to_steal_from is not None:
            interface.steal_from_player(singular_player_to_steal_from, self)

    def robber_discard(self, interface) -> None:
        """
        Allows the player to discard half of their resources
        :param interface: Interface object
        :return: None
        """
        # Get the number of resources to discard
        total_to_discard = len(self.resources) // 2
        print(f"{self} has {len(self.resources)} resources and must discard half")
        # Iterate and ask for cards to discard
        while total_to_discard > 0:
            print(f"{self} has {total_to_discard} resources to discard")
            self.printHand()
            card = input("Which card would you like to discard? ")
            if card in self.resources:
                interface.return_player_card(self, card)
                total_to_discard -= 1
            else:
                print("Invalid card")

    def build(self, interface) -> bool:
        """
        Allows the player to build a settlement, city, or road
        :param interface: Interface object
        :return: True if the player built something, False if they did not
        """
        # Get what the player wants to build
        self.printHand("resource")
        decision = input(
            f"What would you like to buy, a road, a settlement, a city, a development card or cancel?\n"
        )
        while decision not in [
            "road",
            "settlement",
            "city",
            "development card",
            "cancel",
        ]:
            decision = input("Please enter a valid option\n")
        if decision == "cancel":
            return False
        # Get the cost of the building
        required_resources = interface.get_building_cost_list()[decision]
        print(required_resources)
        # Check if the player has enough resources
        for resource, amount in required_resources.items():
            print(self.resources.count(resource))
            print(resource + ": " + str(amount))
            if self.resources.count(resource) < amount:
                print(f"You do not have enough resources to acquire a {decision}")
                return False
        # If the player has enough resources, take them and build the building
        for resource, amount in required_resources.items():
            for i in range(amount):
                interface.return_player_card(self, resource)

        # If the player built a settlement, place it
        if decision == "settlement":
            interface.place_settlement(
                self, self.choose_placement_location(interface, "settlement")
            )
        # If the player built a city, place it
        elif decision == "city":
            interface.place_city(
                self, self.choose_placement_location(interface, "city")
            )
        # If the player built a road, place it
        elif decision == "road":
            interface.place_road(
                self, self.choose_road_location(interface, None, False)
            )
        # If the player bought a development card, buy it
        elif decision == "development card":
            interface.buy_development_card(self)

    def trade_with_bank(self, interface) -> None:
        """
        Allows the player to trade with the bank
        :param interface: Interface object
        :return: None
        """
        # Check if the player has enough of a resource to trade with the bank
        can_trade_with = [
            resource
            for resource in self.resources
            if self.resources.count(resource) > 3
        ]

        # If the player has enough of a resource, ask what they want to trade for
        if len(can_trade_with) > 0:
            if len(can_trade_with) == 1:
                resource = can_trade_with[0]
            else:
                print(
                    "You have enough of the following resources to trade with the bank"
                )
                print(set(can_trade_with))
                resource = input(
                    "Please enter the resource you would like to trade with the bank\n"
                )
                # Wait for a valid response
                while resource not in can_trade_with:
                    resource = input(
                        "Please enter the resource you would like to trade with the bank\n"
                    )
            trade_for = ""
            # Wait for a valid response for what to trade for
            while trade_for not in ["wood", "clay", "sheep", "wheat", "rock"]:
                trade_for = input("What resource would you like to trade for?\n")
            # Trade with the bank
            interface.trade_with_bank(self, resource, trade_for)
        else:
            print("You do not have enough of a resource to trade with the bank")

    def offer_trade(self, interface):
        """
        Allows the player to offer a trade to another player
        :param interface: Interface object
        :return: None
        """
        # Get the player to trade with
        other_players = [
            player for player in interface.get_players_list() if player != self
        ]
        print("Which player would you like to trade with?")
        for i, player in enumerate(other_players):
            print(f"{i + 1}: {player}")
        player_to_trade_with = other_players[int(input()) - 1]
        # Get the resource to trade for
        while True:
            print("What resource would you like to gain from the trade?")
            resource_to_gain = input()
            if resource_to_gain in ["wood", "clay", "sheep", "wheat", "rock"]:
                break
            else:
                print("Please enter a valid resource")
        # Get the resource to trade
        while True:
            print("What resource would you like to give up in the trade?")
            self.printHand("resource")
            resource_to_give = input()
            if resource_to_give in ["wood", "clay", "sheep", "wheat", "rock"]:
                if resource_to_give not in self.resources:
                    print("You do not have that resource")
                else:
                    break
            else:
                print("Please enter a valid resource")
        # Offer the trade
        print("Trade Summary:")
        print(
            f"Player {self} would like to trade {resource_to_give} for {resource_to_gain}"
        )
        while True:
            print("Would you like to proceed? (y/n)")
            if input().lower() == "y":
                interface.trade_with_player(
                    self, player_to_trade_with, resource_to_gain, resource_to_give
                )
                return
            elif input().lower() == "n":
                print("Trade cancelled")
                return
            else:
                print("Please enter a valid response")

    def respond_to_trade(self, interface, original_player, receiving, giving) -> bool:
        """
        Allows the player to respond to a trade offer
        :param original_player: The player who made the offer
        :param receiving: The resource the player is receiving
        :param giving: The resource the player is giving
        :return: True if the player accepts the trade, False if they do not
        """
        # Simply ask the player if they want to accept the trade
        print(
            f"{original_player} would like to trade you {receiving} for {giving}. Would you like to accept this trade? (y/n)"
        )
        accepted = input().lower()
        while accepted not in ["y", "n"]:
            accepted = input("Please enter y or n\n")
        return accepted == "y"

    def play_development_card(self, interface) -> None:
        """
        Allows the player to play a development card
        :param interface: The interface object
        :return: None
        """
        # Check if the player has any development cards
        self.printHand("development")
        if len(self.development_cards) > 0:
            # Ask the player which card they want to play
            card = input("Which card would you like to play?\n")
            while card not in self.development_cards:
                card = input("Please enter a valid card\n")
            args = []
            # Get further information if necessary
            if card == "monopoly":
                res_type = input(
                    "What resource would you like to take from all other players?\n"
                )
                while res_type not in ["wood", "clay", "sheep", "wheat", "rock"]:
                    res_type = input(
                        "What resource would you like to monopolise?\nwood, clay, sheep, wheat, ore\n"
                    )
                args.append(res_type)
            elif card == "year of plenty":
                for i in range(2):
                    res_type = input(
                        "What resource would you like to take from the bank?\n"
                    )
                    while res_type not in ["wood", "clay", "sheep", "wheat", "rock"]:
                        res_type = input(
                            "What resource would you like to monopolise?\nwood, clay, sheep, wheat, ore\n"
                        )
                    args.append(res_type)
            # Play the card
            interface.play_development_card(self, card, args)
        else:
            print("You have no development cards")

    def turn_actions(self, interface) -> None:
        """
        Performs the actions a player can take on their turn
        :param interface:
        :return: None
        """
        # Print the board and the player's hand
        interface.print_board()
        self.printHand("resources")
        self.printHand("development")
        print(f"{self}, what would you like to do?")
        # Get the possible moves
        moves = interface.return_possible_moves(self)
        moves.insert(0, "view building cost list")
        # Ask the player what they want to do
        number_move_pairings = {str(i + 1): move for i, move in enumerate(moves)}
        for i, move in enumerate(moves):
            print(f"{i + 1}: {move.title()}")
        # Get the player's action
        action = int(input())
        while action not in range(1, len(moves) + 1):
            action = int(input("Please enter a valid action\n"))
        action = number_move_pairings[str(action)].lower()

        # Switch on the action
        if action == "view building cost list":
            for building, resources in interface.get_building_cost_list().items():
                print(f"{building}: {resources}")
        elif action == "place settlement":
            interface.place_settlement(
                self, self.choose_placement_location(interface, "settlement")
            )
        elif action == "place city":
            interface.place_city(
                self, self.choose_placement_location(interface, "city")
            )
        # If the player built a road, place it
        elif action == "build road":
            interface.place_road(
                self, self.choose_road_location(interface, None, False)
            )
        # If the player bought a development card, buy it
        elif action == "buy development card":
            interface.buy_development_card(self)
        elif action in ["trade with bank"]:
            self.trade_with_bank(interface)
        elif action == "trade with player":
            self.offer_trade(interface)
        elif action in [
            "play development card",
            "development card",
            "play dev card",
            "dev card",
        ]:
            self.play_development_card(interface)
        elif action == "end turn":
            # If the player ends their turn, raise an exception to end the turn
            raise endOfTurnException
        else:
            # If the player enters an invalid action, print an error message and loop
            print("Invalid action")
            sys.exit(1)
