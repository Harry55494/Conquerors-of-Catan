import sys

from board import *
import time

if __name__ == '__main__':

    # Define the players and the board. Turns happen in the order specified here
    players = [player(1, 'blue'), ai_player(2, 'red')]
    board = board(board_type='default', players=players)

    turn, player_has_won = 1, False

    board.initial_placement(random)

    for player in players:
        player.calculateVictoryPoints(board)

    while not player_has_won:
        for player_ in players:
            os.system('clear' if os.name == 'posix' else 'cls')
            board.print_board(print_letters=False)
            print('\n')
            print('- Turn ' + str(turn) + ' -')
            print(player_, 'is playing')

            if player_.human_or_ai == 'Human':
                waiter = input('Press enter to roll the dice')
                dice_roll = roll_dice()
                print(f'You rolled {dice_roll}')

            else:
                dice_roll = roll_dice()
                print(f'{player_} rolled {dice_roll}')

            board.process_roll(dice_roll, player_)

            player_.printHand()

            board.turn_actions(player_)

            print(f'{player_} has finished their go')

            time.sleep(1)

            if player_.calculateVictoryPoints(board) >= 10:
                player_has_won = True
                os.system('clear')
                board.print_board()
                print(player_, 'has won!')
                break
        turn += 1
