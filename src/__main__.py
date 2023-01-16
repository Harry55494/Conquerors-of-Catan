from board_interface import *
from src.ai_minimax import ai_minimax
from src.ai_random import *

if __name__ == "__main__":

    # Define the players and the board. Turns happen in the order specified here
    players = [ai_random(3, "blue"), ai_random(2, "red"), ai_minimax(1, "yellow")]
    players = sorted(players, key=lambda x: x.number)
    interface = boardInterface(players)
    os.system("clear" if os.name == "posix" else "cls")

    turn, player_has_won, all_players_ai = (
        1,
        False,
        (all(isinstance(player, ai_player) for player in players)),
    )

    interface.initial_placement()

    for player in players:
        player.calculateVictoryPoints(interface)

    while not player_has_won:
        for player_ in players:

            interface.print_board()
            print("\n")
            print("- Turn " + str(turn) + " -")
            interface.turn_number = turn
            interface.log_action(f"{player_.name}'s turn")
            if not all_players_ai:
                print(player_, "is playing")

            if player_.__class__ == player:
                waiter = input("Press enter to roll the dice")
                dice_roll = roll_dice()
                print(f"You rolled {dice_roll}")

            else:
                dice_roll = roll_dice()
                print(f"{player_} rolled {dice_roll}")

            interface.log_action(f"{player_.name} rolled {dice_roll}")

            interface.process_roll(dice_roll, player_)

            interface.log_action(
                f"{player_.name}'s resources are now {player_.resources}"
            )

            player_.turn_actions(interface)

            interface.board.update_special_cards()

            print(f"{player_} has finished their go")

            if all_players_ai:
                time.sleep(0.03)
            else:
                time.sleep(3)

            if player_.calculateVictoryPoints(interface) >= 10:
                player_has_won = True
                os.system("clear")
                interface.print_board()
                print("\n")
                print("- Turn " + str(turn) + " -")
                print(player_, "has won!")
                player_.calculateVictoryPoints(interface, True)
                break
        turn += 1

        if turn > 200:
            print("Game has gone on too long. Ending game")
            break
