players_list = ["player 1", "player 2", "player 3", "player 4"]


def get_next_player(current_player):
    if current_player == players_list[-1]:
        return players_list[0]
    else:
        return players_list[players_list.index(current_player) + 1]


if __name__ == "__main__":
    current_player = players_list[0]
    for i in range(10):
        print(current_player)
        current_player = get_next_player(current_player)
