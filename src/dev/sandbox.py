import copy

from src.game import *

player1 = ai_random(1, "red")
player2 = ai_random(2, "blue")
player3 = copy.deepcopy(player1)

print(player1 == player2)
print(player1.number == player2.number)
print(player1 == player3)
print(player1.number == player3.number)

players = [
    ai_random(1, "red"),
    ai_minimax(2, "yellow", wishful_thinking=True),
    ai_minimax(3, "blue", wishful_thinking=False),
    ai_random(4, "green"),
]

players = random.sample(players, len(players))
print([player.name for player in players])


def get_next_player(self, current_player) -> player:
    """
    Gets the next player in the list of players
    Used by Minimax to get the next player
    Uses player numbers, so could be improved for when players are not in order
    :param current_player: The current player
    :return: The next player
    """
    if current_player.number == players[-1].number:
        # print("Returning first player")
        return players[0]
    else:
        # Find the player with matching number
        current_player_number = current_player.number
        for position, player in enumerate(players):
            if player.number == current_player_number:
                return players[position + 1]


current_player = players[0]

for i in range(0, 10):
    next_player = get_next_player(None, current_player)
    print(current_player.number)
    current_player = next_player
