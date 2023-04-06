"""
Game class, for setting up and running a game

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

from src.board_interface import *
from src.player import player, endOfTurnException


class game:
    """
    Game class, for setting up and running a game
    Contains functions for setting up the game, running through the turns, and checking the game state, and then saving the results
    """

    class setupError(Exception):
        """
        Exception raised when there is an error in the setup of the game
        """

        pass

    def setup_checking(self):
        """
        Sets up the game, checking that the game is valid
        :return: None
        """
        # Player Checking
        # Checks for the number of players, and that the player numbers and colours are unique
        if not 2 <= len(self.players) <= 5:
            raise self.setupError("There must be between 2 and 5 players")
        player_nums = [player_.number for player_ in self.players]
        player_colours = [player_.colour for player_ in self.players]
        if len(player_nums) != len(set(player_nums)):
            raise self.setupError("Player numbers must be unique")
        if len(player_colours) != len(set(player_colours)):
            raise self.setupError("Player colours must be unique")

        # Game Checking
        if CONFIG["table_top_mode"]:
            print("Table top mode is enabled")
            print("An acknowledgement will be required to continue each turn")

        # Double checks that the target score is valid, and warns the user if it is not the default
        if CONFIG["target_score"] != 10:
            if CONFIG["target_score"] < 3:
                raise self.setupError("Target score must be at least 3")
            print(
                "Warning: Target score is set to "
                + str(CONFIG["target_score"])
                + " points"
            )
            print(
                "Game will be "
                + ("shorter" if CONFIG["target_score"] < 10 else "longer")
                + " than usual"
            )
            for i in range(3, 0, -1):
                print("Continuing in " + str(i) + " seconds")
                time.sleep(1)

    def __init__(self, players: list[player]):
        """
        Initialises a 'match' of the game, which is just a game with stored results.
        :param players: A list of the players in the game
        :return: None
        """

        # Shuffle the players so that the player order is random
        # Then sort the players by their number, so that the player order is correct
        random.shuffle(players)
        for i, player in enumerate(players):
            player.number = i + 1
        players = sorted(players, key=lambda x: x.number)

        # Set up the game variables
        self.players = players
        self.all_players_ai = all(
            isinstance(player, ai_player) for player in self.players
        )
        self.interface = board_interface(self.players)
        self.turn = 1
        self.player_has_won = False
        self.results = {player.name: 0 for player in self.players}

    def initial_placement(self):
        """
        Run the initial placement methods of the players
        :return: None
        """

        os.system("clear" if os.name == "posix" else "cls")

        # Perform the setup checking
        self.setup_checking()

        # Set up the initial placement of the players
        self.interface.initial_placement()

        # Clone the player so that the objects from outside this match are not affected
        # Python passes objects by reference, so if the player objects are changed, the objects outside for all matches will be changed
        current_player = self.interface.get_players_list()[0]
        for i in range(10):
            current_player = copy.deepcopy(
                self.interface.get_next_player(current_player)
            )

        # Calculate the victory points for the players
        for player in self.players:
            player.calculateVictoryPoints(self.interface)

    def play(self):
        """
        The main game loop
        :return: None
        """

        # Checks if the game has been won
        while not self.player_has_won:

            # Announce the start of the turn
            self.interface.log_action(f"\n\nTurn {self.turn} started")

            # Game Loop for each player
            # Each iteration here is one round of turns
            for player_ in self.players:

                # Sort cards and set variables
                player_.resources.sort()
                player_.development_cards.sort()
                player_.has_built_this_turn = False
                player_.has_played_dev_card_this_turn = False
                player_.dev_cards_at_start_of_turn = player_.development_cards.copy()
                player_.gained_dev_cards_this_turn = []

                # Set the turn number and print the board
                self.interface.print_board()
                print("\n")
                print("- Turn " + str(self.turn) + " -")
                self.interface.turn_number = self.turn
                self.interface.board.turn = self.turn
                self.interface.log_action(f"{player_.name}'s turn")
                if not self.interface.all_players_ai:
                    print(player_, "is playing")

                # Dice Roll
                # If the game is in table-top mode, the dice roll is input by the user
                if CONFIG["table_top_mode"]:
                    while True:
                        dice_roll = input("Enter dice roll: ")
                        try:
                            dice_roll = int(dice_roll)
                            if dice_roll < 2 or dice_roll > 12:
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid dice roll")

                else:

                    # If the player is an AI, the dice roll is automatically generated
                    # If the player is a human, the dice roll is done after a keypress
                    if player_.__class__ == src.player.player:
                        input("Press enter to roll the dice")
                        print("\033[F", end="")
                        two_dice = roll_dice()
                        dice_roll = sum(two_dice)
                        if isinstance(two_dice, list):
                            self.interface.board.current_roll = two_dice
                            two_dice = sum(two_dice)
                        else:
                            self.interface.board.roll = None
                        self.interface.print_board()
                        print(f"You rolled {dice_roll}" + " " * 20 + "\033[K")

                    else:
                        two_dice = roll_dice()
                        dice_roll = sum(two_dice)
                        if isinstance(two_dice, list):
                            self.interface.board.current_roll = two_dice
                            two_dice = sum(two_dice)
                        else:
                            self.interface.board.roll = None
                        self.interface.print_board()
                        print(f"{player_} rolled {dice_roll}")

                # Log the dice roll
                self.interface.log_action(f"{player_.name} rolled {dice_roll}")

                if two_dice is None:
                    two_dice = dice_roll

                # Process the dice roll, giving the players resources
                self.interface.process_roll(two_dice, player_)

                # Print the player's resources
                self.interface.log_action(
                    f"{player_.name}'s resources are now {player_.resources}"
                )

                if not isinstance(player_, ai_player):
                    await_user_input()

                # Player Actions -----------------------------------------------------
                num_moves_made = 0

                # Limit the number of moves that can be made in a turn
                # Different limits for AI and human players
                try:
                    limit = (
                        CONFIG["max_moves_per_turn_ai"]
                        if isinstance(player_, ai_player)
                        else CONFIG["max_moves_per_turn_human"]
                    )
                    if not limit:
                        limit = 100
                    for i in range(limit):
                        # Get the player to perform an action
                        player_.turn_actions(self.interface)
                        self.interface.update_special_cards()
                        num_moves_made += 1
                except endOfTurnException:
                    pass

                # Player has finished their go, log this
                print(f"{player_} has finished their go, making {num_moves_made} moves")
                self.interface.log_action(
                    f"{player_.name}'s resources are now {player_.resources} at the end of their turn"
                )

                # End of turn waiting
                if not CONFIG["table_top_mode"]:
                    if self.interface.all_players_ai:
                        time.sleep(0.1)
                    else:
                        await_user_input()

                else:
                    # If tabletop mode, wait for the user to acknowledge the end of the turn so that the physical board can be updated
                    if isinstance(player_, ai_player):
                        await_user_input()

                # Check if the player has won
                if (
                    player_.calculateVictoryPoints(self.interface)
                    >= CONFIG["target_score"]
                ):
                    self.player_has_won = True
                    os.system("clear")
                    self.interface.print_board()
                    print("\n")
                    print("- Turn " + str(self.turn) + " -")
                    print(player_, "has won!")
                    player_.calculateVictoryPoints(self.interface, True)
                    break

            # End of turn waiting for tabletop mode
            if CONFIG["table_top_mode"]:
                print("End of turn " + str(self.turn))
                time.sleep(1)

            self.turn += 1

            # Check if the game has gone on too long, and end it if so
            if self.turn > 200:
                print("Game has gone on too long. Ending game early")
                # In this situation, the player with the most victory points wins
                winner = max(
                    self.players, key=lambda x: x.calculateVictoryPoints(self.interface)
                )
                print(f"{winner} has won!")
                break

        # Dump the moves of the players
        for player in self.players:
            if isinstance(player, ai_player):
                player.dump_moves()
            self.results[player.name] = player.calculateVictoryPoints(self.interface)
