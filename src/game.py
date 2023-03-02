from src.board_interface import *
from src.player import endOfTurnException


class game:
    class setupError(Exception):
        pass

    def setup_checking(self):
        # Player Checking
        if len(self.players) < 2:
            raise self.setupError("There must be at least 2 players")
        player_nums = [player_.number for player_ in self.players]
        player_colours = [player_.colour for player_ in self.players]
        if len(player_nums) != len(set(player_nums)):
            raise self.setupError("Player numbers must be unique")
        if len(player_colours) != len(set(player_colours)):
            raise self.setupError("Player colours must be unique")
        if len(self.players) > 5:
            raise self.setupError("There can be a maximum of 5 players")

        # Game Checking
        if CONFIG["table_top_mode"]:
            print("Table top mode is enabled")
            print("An acknowledgement will be required to continue each turn")

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
        :param players:
        """

        random.shuffle(players)
        for i, player in enumerate(players):
            player.number = i + 1

        players = sorted(players, key=lambda x: x.number)

        self.players = players
        self.interface = board_interface(self.players)
        self.turn = 1
        self.player_has_won = False
        self.all_players_ai = all(
            isinstance(player, ai_player) for player in self.players
        )
        self.results = {player.name: 0 for player in self.players}

    def initial_placement(self):

        os.system("clear" if os.name == "posix" else "cls")

        self.setup_checking()

        self.interface.initial_placement()

        current_player = self.interface.get_players_list()[0]
        for i in range(10):
            print(current_player.name)
            current_player = copy.deepcopy(
                self.interface.get_next_player(current_player)
            )

        # time.sleep(10)

        for player in self.players:
            player.calculateVictoryPoints(self.interface)

    def play(self):

        while not self.player_has_won:

            # Game Loop
            for player_ in self.players:

                self.interface.turn = self.turn
                self.interface.print_board()
                print("\n")
                print("- Turn " + str(self.turn) + " -")
                self.interface.turn_number = self.turn
                self.interface.log_action(f"{player_.name}'s turn")
                if not self.all_players_ai:
                    print(player_, "is playing")

                # Dice Roll
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

                    if player_.__class__ == src.player.player:
                        input("Press enter to roll the dice")
                        dice_roll = roll_dice()
                        print(f"You rolled {dice_roll}")

                    else:
                        dice_roll = roll_dice()
                        print(f"{player_} rolled {dice_roll}")

                self.interface.log_action(f"{player_.name} rolled {dice_roll}")

                self.interface.process_roll(dice_roll, player_)

                self.interface.log_action(
                    f"{player_.name}'s resources are now {player_.resources}"
                )

                num_moves_made = 0

                try:
                    limit = (
                        CONFIG["max_moves_per_turn_ai"]
                        if isinstance(player_, ai_player)
                        else CONFIG["max_moves_per_turn_human"]
                    )
                    if not limit:
                        limit = 100
                    for i in range(limit):
                        player_.turn_actions(self.interface)
                        self.interface.update_special_cards()
                        num_moves_made += 1
                except endOfTurnException:
                    pass

                print(f"{player_} has finished their go, making {num_moves_made} moves")

                # End of turn waiting
                if not CONFIG["table_top_mode"]:
                    if self.all_players_ai:
                        time.sleep(0.1)
                    else:
                        time.sleep(3)
                else:
                    if isinstance(player_, ai_player):
                        input("\nPress enter to acknowledge and continue")

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

            if CONFIG["table_top_mode"]:
                print("End of turn " + str(self.turn))
                time.sleep(1)

            self.turn += 1

            if self.turn > 200:
                print("Game has gone on too long. Ending game early")
                winner = max(
                    self.players, key=lambda x: x.calculateVictoryPoints(self.interface)
                )
                print(f"{winner} has won!")
                break

        for player in self.players:
            player.dump_moves()
            self.results[player.name] = player.calculateVictoryPoints(self.interface)
