import random

from ai_player import ai_player


class ai_minimax(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="minimax")

    def evaluateBoard(self, interface):
        """
        Heuristic function to evaluate the board state
        :param interface: boardInterface
        :return: The evaluation of the board as an integer
        """

        # NOTES
        # Main Score points should be based on the following:
        # 1. Victory Points - This contains the number of cities and settlements, so no need to calculate this as well
        # 2. Number of roads
        # 3. Number of resource player has access to
        # 4. Number of development cards
        # 5. Position of settlements and cities, based on scarcity of resources

        # Resources of other opponents
        # Resource Scarcity

        # No need to calculate the number of settlements and cities, as this is already calculated in the victory points
        # No need to calculate how many resource cards a player has in their hand, as this would suggest players to horde cards instead of spending

        score = 0

        # Victory Points ------------------------------------------------------

        current_vp = self.calculateVictoryPoints(interface)

        other_players = [player for player in interface.get_players_list() if player != self]
        other_players.sort(key=lambda x: x.calculateVictoryPoints(interface), reverse=True)
        total_other_players_points = sum(
            [player.calculateVictoryPoints(interface) for player in other_players]
        )

        score += current_vp * 10

        if current_vp >= 10:
            return 1000000
        if current_vp == 9:  # Bonus points for being close to winning
            score += 50

        if current_vp > other_players[0].calculateVictoryPoints(interface):
            score += 50
        elif current_vp == other_players[0].calculateVictoryPoints(interface):
            score += 25

        # Number of roads -----------------------------------------------------

        score += interface.count_structure(self, "road") * 2

        # Number of resources player has access to -----------------------------
        # This is relative to the number of resources a player would get on a turn if every dice roll was rolled.

        # Higher numbers are less common, so they should be weighted more

        # rarity = board.calculate_resource_rarity()

        resources = []
        for key, item in interface.get_buildings_list().items():
            if interface.get_buildings_list()[key]["player"] == self:
                if interface.get_buildings_list()[key]["building"] == "settlement":
                    resources.append(item for item in interface.get_buildings_list()[key]["tiles"])
                elif interface.get_buildings_list()[key]["building"] == "city":
                    resources.append(item for item in interface.get_buildings_list()[key]["tiles"])
                    resources.append(item for item in interface.get_buildings_list()[key]["tiles"])
        score += len(resources) * 3

        # Number of development cards ------------------------------------------

        score += len(self.development_cards) * 3
        score += self.played_robber_cards * 3

        return score


if __name__ == "__main__":

    players = [ai_minimax(1, "green"), ai_minimax(2, "yellow")]
    interface = boardInterface(players)
    for building in interface.get_buildings_list():
        if random.randint(0, 4) == 4:
            interface.get_buildings_list()[building].update(
                {
                    "player": players[random.randint(0, len(players) - 1)],
                    "building": "settlement" if random.randint(0, 4) != 0 else "city",
                }
            )
        if random.randint(0, 3) == 3:
            interface.get_buildings_list()[building].update({"player": None, "building": None})

    for road in interface.get_roads_list():
        if random.randint(0, 3) == 3:
            interface.get_roads_list()[road].update(
                {"player": players[random.randint(0, len(players) - 1)]}
            )

        if random.randint(0, 3) == 3:
            interface.get_roads_list()[road].update({"player": None})

    for player in players:
        player.calculateVictoryPoints(interface)
    interface.board.update_special_cards()
    interface.print_board()
    print("\n")
    for player in players:
        print(f"Score for {player} = {player.evaluateBoard(interface)}")
