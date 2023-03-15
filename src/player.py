import termcolor
from src.CONFIG import CONFIG


class endOfTurnException(Exception):
    pass


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
        self.number = number
        self.colour = colour
        self.name = "Player " + str(number)
        self.coloured_name = termcolor.colored(self.name, self.colour)
        self.victory_points = 0
        self.resources = []
        self.development_cards = []
        self.played_robber_cards = 0
        print(self.coloured_name, "has joined the game")

    # override print function
    def __str__(self):
        return self.coloured_name

    def __eq__(self, other):
        if not isinstance(other, player):
            return False
        return self.number == other.number

    def count_cards(self, card_type) -> dict:
        card_count = {}
        if card_type in ["resource", "resources"]:
            list_ = self.resources
            for resource in ["wheat", "wood", "sheep", "clay", "rock"]:
                card_count[resource] = 0
        else:
            list_ = self.development_cards
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
        if type_ in ["resource", "resources"]:
            list_to_print = self.resources
        else:
            list_to_print = self.development_cards
        list_to_print.sort()
        print(
            f"{'You'} ({self.coloured_name}) have {len(list_to_print)} {type_} card(s) in your hand.",
            end="",
        )
        if len(list_to_print) > 0:
            print(" They are:")
            card_count = self.count_cards(type_)
            for card in card_count:
                print(f"{card_count[card]} x {card} ", end=" ")
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

        if buildings_list is None:
            buildings_list = interface.get_buildings_list()

        for building in buildings_list:
            if buildings_list[building] is not None:
                if buildings_list[building].get("player") == self:
                    if buildings_list[building].get("building") == "settlement":
                        self.victory_points += 1
                        sources["settlements"] += 1
                    elif buildings_list[building].get("building") == "city":
                        self.victory_points += 2
                        sources["cities"] += 1
        for card in self.development_cards:
            if card == "victory point":
                self.victory_points += 1
                sources["development cards"] += 1
        if interface.get_largest_army()[0] == self:
            self.victory_points += 2
            sources["largest_army"] += 1
        if interface.get_longest_road()[0] == self:
            self.victory_points += 2
            sources["longest_road"] += 1

        if output:
            print(f"Player has {self.victory_points} victory points")
            for source in sources:
                if sources[source] > 0:
                    print(f"{source}: {sources[source]}")
                    if source == "development cards":
                        self.printHand("development cards")

        return self.victory_points

    # Placing Roads and Settlements ------------------------------------------------

    def choose_placement_location(self, interface, type_="settlement"):
        """
        Chooses a place on the board to place a settlement or city
        :param interface:
        :param type_: The type of building to place
        :return: The location of the building
        """
        interface.print_board(print_letters=True)
        accepted, location = False, ""
        while not accepted:
            location = input(
                f"{self} , where would you like to place your {type_}? "
                f"\nPlease enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners"
                f"\n(Single corner numbers increase as you move clockwise around a tile)\n"
            )
            location = location.lower()
            letters = location.split(",")
            letters = [letter.strip() for letter in letters]
            letters.sort()
            location = ",".join(letters)
            if location in interface.get_buildings_list():
                if (
                    interface.get_buildings_list()[location]["player"] is None
                    or interface.get_buildings_list()[location]["player"] == self
                    and type_ == "settlement"
                ) and not interface.check_for_nearby_settlements(location):
                    accepted = True
                else:
                    print("That location is already occupied!")
            else:
                print("That is not a valid location!")
        return location

    def choose_road_location(
        self, interface, requirement=None, ignore_current_endings=True
    ):
        """
        Places a road on the board for a player
        :param ignore_current_endings:
        :param requirement:
        :param interface:
        :return: None
        """
        current_road_endings = []
        for tuple_, details in interface.get_roads_list().items():
            if details["player"] == self:
                current_road_endings.append(tuple_[0])
                current_road_endings.append(tuple_[1])

        interface.print_board(print_letters=True)
        accepted = False
        while not accepted:
            coordinates = []
            if requirement is not None:
                coordinates.append(requirement)
            while len(coordinates) < 2:
                print(
                    f"{self} , where would you like to place your road?\n"
                    f"Please enter in the form of a reference such as 'a,b,e', or of 'a1', 'a2' for single corners"
                )
                if requirement is not None:
                    print(f"Your road must connect to {requirement}")
                location = input(
                    f"Please enter the {len(coordinates) + 1}{'st' if len(coordinates) + 1 == 1 else 'nd'} location\n"
                )

                location = location.lower()
                letters = location.split(",")
                letters = [letter.strip() for letter in letters]
                letters.sort()
                location = ",".join(letters)
                coordinates.append(location)
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
                        return coordinates
                else:
                    print("That location is already occupied!")

    def initial_placement(self, interface):
        building = self.choose_placement_location(interface, "settlement")
        interface.place_settlement(self, building, True)
        interface.place_road(self, self.choose_road_location(interface, building, True))
        return building

    # Turn Functions ------------------------------------------------

    def robber(self, interface):
        """
        Perform the robber actions for a player
        :param interface:
        :return:
        """
        interface.print_board(print_letters=True)
        print(f"{self}, has rolled the robber!")
        print(f"{self}, where would you like to move the robber?")
        accepted = False
        while not accepted:
            location = input(
                "Please enter the letter of the tile you would like to move the robber to\n"
            )
            location = location.lower()
            if any([tile_.letter == location for tile_ in interface.get_tiles_list()]):
                accepted = True
                interface.move_robber(location)
            else:
                print("Invalid location")
        new_robber_location = [
            tile_ for tile_ in interface.get_tiles_list() if tile_.contains_robber
        ][0]
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

        player_to_steal_from = None

        if len(players_to_steal_from) > 1:
            print("Please select a player to steal from")
            print(player_item for player_item in players_to_steal_from)
            player_nums = [
                int(player_item.number) for player_item in players_to_steal_from
            ]
            accepted = False
            while not accepted:
                choice = input(
                    "Please enter the number of the player you would like to steal from\n"
                )
                if choice.isdigit() and int(choice) in player_nums:
                    accepted = True
                    for player_ in players_to_steal_from:
                        if player_.number == int(choice):
                            player_to_steal_from = player_
                else:
                    print("Invalid choice")
        elif len(players_to_steal_from) == 1:
            player_to_steal_from = players_to_steal_from[0]
        else:
            print("No players to steal from")

        if player_to_steal_from is not None:
            interface.steal_from_player(player_to_steal_from, self)

    def robber_discard(self, interface):
        total_to_discard = len(self.resources) // 2
        print(f"{self} has {len(self.resources)} resources and must discard half")
        while total_to_discard > 0:
            print(f"{self} has {total_to_discard} resources to discard")
            self.printHand()
            card = input("Which card would you like to discard? ")
            if card in self.resources:
                interface.return_player_card(self, card)
                total_to_discard -= 1
            else:
                print("Invalid card")

    def build(self, interface):
        """
        Allows the player to build a settlement, city, or road
        :param interface:
        :return:
        """
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
        required_resources = interface.get_building_cost_list()[decision]
        print(required_resources)
        has_resources = True
        for resource, amount in required_resources.items():
            print(self.resources.count(resource))
            print(resource + ": " + str(amount))
            if self.resources.count(resource) < amount:
                print(f"You do not have enough resources to acquire a {decision}")
                return
        if has_resources:
            for resource, amount in required_resources.items():
                for i in range(amount):
                    interface.return_player_card(self, resource)
            if decision == "settlement":
                interface.place_settlement(
                    self, self.choose_placement_location(interface, "settlement")
                )
            elif decision == "city":
                interface.place_city(
                    self, self.choose_placement_location(interface, "city")
                )
            elif decision == "road":
                interface.place_road(
                    self, self.choose_road_location(interface, None, False)
                )
            elif decision == "development card":
                interface.buy_development_card(self)

    def trade_with_bank(self, interface):
        has_enough = False
        can_trade_with = []
        for resource in self.resources:
            if self.resources.count(resource) > 3:
                has_enough = True
                can_trade_with.append(resource)
        if has_enough:
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
                while resource not in can_trade_with:
                    resource = input(
                        "Please enter the resource you would like to trade with the bank\n"
                    )
            trade_for = ""
            while trade_for not in ["wood", "clay", "sheep", "wheat", "ore"]:
                trade_for = input("What resource would you like to trade for?\n")
            interface.trade_with_bank(self, resource, trade_for)
        else:
            print("You do not have enough of a resource to trade with the bank")

    def respond_to_trade(self, original_player, receiving, giving):
        """
        Allows the player to respond to a trade offer
        :param original_player: The player who made the offer
        :param receiving: The resource the player is receiving
        :param giving: The resource the player is giving
        :return:
        """
        print(
            f"{original_player} would like to trade you {receiving} for {giving}. Would you like to accept this trade? (y/n)"
        )
        accepted = input()
        while accepted not in ["y", "n"]:
            accepted = input("Please enter y or n\n")
        if accepted == "y":
            return True
        else:
            return False

    def play_development_card(self, interface):
        """
        Allows the player to play a development card
        :param interface: The interface object
        :return:
        """
        self.printHand("development")
        if len(self.development_cards) > 0:
            card = input("Which card would you like to play?\n")
            while card not in self.development_cards:
                card = input("Please enter a valid card\n")
            args = []
            if card == "monopoly":
                res_type = input(
                    "What resource would you like to take from all other players?\n"
                )
                while res_type not in ["wood", "clay", "sheep", "wheat", "ore"]:
                    res_type = input(
                        "What resource would you like to monopolise?\nwood, clay, sheep, wheat, ore\n"
                    )
                args.append(res_type)
            elif card == "year of plenty":
                for i in range(2):
                    res_type = input(
                        "What resource would you like to take from the bank?\n"
                    )
                    while res_type not in ["wood", "clay", "sheep", "wheat", "ore"]:
                        res_type = input(
                            "What resource would you like to monopolise?\nwood, clay, sheep, wheat, ore\n"
                        )
                    args.append(res_type)
            interface.play_development_card(self, card, args)
        else:
            print("You have no development cards")

    def turn_actions(self, interface):
        """
        Performs the actions a player can take on their turn
        :param interface:
        :return: None
        """
        interface.print_board()
        self.printHand("resources")
        self.printHand("development")
        print(f"{self}, what would you like to do?")
        moves = interface.return_possible_moves(self)
        moves.append("view building list")
        moves.append("end turn")
        for move in moves:
            print(f"- {move.title()}")
        action = input().lower()
        if action in ["view building list", "building list", "view", "list"]:
            for building, resources in interface.get_building_cost_list.items():
                print(f"{building}: {resources}")
        elif action in [
            "build",
            "buy development card",
            "buy",
        ] or action.__contains__("build"):
            self.build(interface)
        elif action in ["trade with bank", "trade"]:
            self.trade_with_bank(interface)
        elif action in [
            "play development card",
            "development card",
            "play dev card",
            "dev card",
        ]:
            self.play_development_card(interface)
        elif action in ["end turn", "end"]:
            raise endOfTurnException
        else:
            print("Invalid action")
