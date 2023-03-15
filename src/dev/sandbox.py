import copy

from src.game import *

player1 = ai_random(1, "red")
player2 = ai_random(2, "blue")
player3 = copy.deepcopy(player1)

print(player1 == player2)
print(player1.number == player2.number)
print(player1 == player3)
print(player1.number == player3.number)
