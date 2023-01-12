from board_interface import *

if __name__ == '__main__':

    # Define the players and the board. Turns happen in the order specified here
    players = [player(1, 'blue'), ai_random(2, 'red')]
    interface = boardInterface(players)
    os.system('clear' if os.name == 'posix' else 'cls')

    turn, player_has_won, all_players_ai = 1, False, (all(isinstance(player, ai_player) for player in players))

    interface.initial_placement()

    for player in players:
        player.calculateVictoryPoints(interface)

    while not player_has_won:
        for player_ in players:

            interface.print_board()
            print('\n')
            print('- Turn ' + str(turn) + ' -')
            interface.turn_number = turn
            if not all_players_ai:
                print(player_, 'is playing')

            if player_.__class__ == player:
                waiter = input('Press enter to roll the dice')
                dice_roll = roll_dice()
                print(f'You rolled {dice_roll}')

            else:
                dice_roll = roll_dice()
                print(f'{player_} rolled {dice_roll}')

            interface.process_roll(dice_roll, player_)

            player_.turn_actions(interface)

            interface.board.update_special_cards()

            print(f'{player_} has finished their go')

            if all_players_ai:
                time.sleep(0.01)
            else:
                time.sleep(3)

            if player_.calculateVictoryPoints(interface) >= 10:
                player_has_won = True
                os.system('clear')
                interface.print_board()
                print(player_, 'has won!')
                player_.calculateVictoryPoints(interface, True)
                break
        turn += 1

        if turn > (100 * len(players)):
            print('Game has gone on too long. Ending game')
            break
