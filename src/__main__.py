from board import *
from player import *
import time

if __name__ == '__main__':

    # Define the players and the board. Turns happen in the order specified here
    players = [player(1, 'blue', 'Human'), player(2, 'red', 'AI')]
    board = board(board_type='default', players=players)

    player_has_won = False

    turn = 1

    board.initial_placement()

    for player in players:
        player.calculateVictoryPoints(board)

    while not player_has_won:
        for player_ in players:
            os.system('clear' if os.name == 'posix' else 'cls')
            board.print_board(print_letters=False)
            print('\n')
            print('- Turn ' + str(turn) + ' -')
            print(player_.coloured_name, 'is playing')

            if player_.type == 'Human':
                waiter = input('Press enter to roll the dice')
                dice_roll = roll_dice()
                print(f'You rolled {dice_roll}')

            else:
                dice_roll = roll_dice()
                print(f'{player_.coloured_name} rolled {dice_roll}')

            board.process_roll(dice_roll)

            player_.printHand()

            time.sleep(5)

            if player_.calculateVictoryPoints(board) >= 10:
                player_has_won = True
                os.system('clear')
                board.print_board()
                print(player_.coloured_name, 'has won!')
                break
        turn += 1
