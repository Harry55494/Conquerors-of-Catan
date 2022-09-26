from board import *
from player import *
import time

if __name__ == '__main__':

    # Run these two lines if you haven't run the program before
    #os.system("pip install -r requirements.txt ")
    #os.system("clear")

    players = [player(1, 'blue', 'Human'), player(2, 'red', 'AI')]
    board = board(board_type='default', players=players)

    for building in board.buildings:
        board.buildings[building].update({'player': players[random.randint(0, len(players)-1)],
                                          'building': 'settlement' if random.randint(0, 4) != 0 else 'city'})
        if random.randint(0,3) == 3:
            board.buildings[building].update({'player': None, 'building': None})

    for road in board.roads:
        board.roads[road].update({'player': players[random.randint(0, len(players)-1)]})

        if random.randint(0,3) == 3:
            board.roads[road].update({'player': None})

    for player in players:
        player.calculateVictoryPoints(board)

    player_has_won = False

    turn = 1

    while not player_has_won:
        for player_ in players:
            os.system('clear')
            board.print_board()
            print('\n')
            print('- Turn ' + str(turn) + ' -')
            print(player_.coloured_name, 'is playing')

            if player_.type == 'Human':
                waiter = input('Press enter to roll the dice')
                dice_roll = roll_dice()
                print('You rolled', dice_roll)

            else:
                dice_roll = roll_dice()
                print(f'{player_.coloured_name} rolled', dice_roll)

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
