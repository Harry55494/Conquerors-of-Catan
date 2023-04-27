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


# Data was re-printed here as it was wrongly sorted the first time

print("\nFinal Results:\n")

data = [
    ["Player 1 (random)", 0, 5, 87, 0.03],
    ["Player 3 (random)", 0, 4.5, 85, 0.03],
    ["Player 2 (minimax)", 75.0, 9.1, 41, 4.48],
    ["Player 4 (random)", 25.0, 7, 53, 0.03],
]

data.sort(key=lambda x: (x[1]), reverse=True)

for person in data:
    person[1] = f"{person[1]}%"
    person[2] = f"{person[2]:.2f}"
    person[3] = f"{person[3]:.3f}"
    person[4] = f"{person[4]:.2f}s"

tabbed_data = tabulate(
    data,
    headers=[
        "Player",
        "Win Rate",
        "Avg Victory Points",
        "Avg Turns to Win",
        "Avg Turn Time",
    ],
    tablefmt="simple_grid",
)
print(tabbed_data)

print("\nAverage Time per Match: 4.43 minutes")
