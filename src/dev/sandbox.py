import copy
import timeit

from src.game import *

if not os.path.exists("logs"):
    print("Setting up logging...")
    os.mkdir("logs")
if not os.path.exists("logs/players"):
    os.mkdir("logs/players")

players = [ai_random(1, "red"), ai_random(2, "blue"), ai_minimax(3, "yellow")]
board_interface = board_interface(players)
board_interface.initial_placement()

board_interface.print_board(True)
print("\n\n\n\n")
print(board_interface.get_distance_between_nodes("a1", "b,e,g"))

time = timeit.timeit(
    "board_interface.get_distance_between_nodes('a1', 'b,e,g')",
    globals=globals(),
    number=10000,
)
print(f"Average time: {time / 10000} seconds")
