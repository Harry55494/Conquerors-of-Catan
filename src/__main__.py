from board import *
import time

if __name__ == '__main__':

    # Define the players and the board. Turns happen in the order specified here
    players = [ai_random(1, 'blue'), ai_random(2, 'red')]
    board = board(board_type='default', players=players)
    os.system('clear' if os.name == 'posix' else 'cls')

    turn, player_has_won, all_players_ai = 1, False, (all(isinstance(player, ai_player) for player in players))

    board.initial_placement()

    for player in players:
        player.calculateVictoryPoints(board)

    while not player_has_won:
        for player_ in players:

            board.print_board(print_letters=False)
            print('\n')
            print('- Turn ' + str(turn) + ' -')
            if not all_players_ai:
                print(player_, 'is playing')

            if player_.__class__ == player:
                waiter = input('Press enter to roll the dice')
                dice_roll = roll_dice()
                print(f'You rolled {dice_roll}')

            else:
                dice_roll = roll_dice()
                print(f'{player_} rolled {dice_roll}')

            board.process_roll(dice_roll, player_)

            player_.turn_actions(board)

            board.check_for_special_cards()

            print(f'{player_} has finished their go')

            if all_players_ai:
                time.sleep(0.25)
            else:
                time.sleep(3)


            if player_.calculateVictoryPoints(board) >= 10:
                player_has_won = True
                os.system('clear')
                board.print_board()
                print(player_, 'has won!')
                break
        turn += 1

        if turn > 250:
            print('Game has gone on too long. Ending game')
            break
