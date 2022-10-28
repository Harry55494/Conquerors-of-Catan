import random

from ai_player import ai_player


class ai_random(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy='random')

    def initial_placement(self, board):
        accepted = False
        building = ''
        while accepted is False:

            rand_int = random.randint(0, len(board.buildings) - 1)
            if (board.buildings[list(board.buildings.keys())[rand_int]]['player'] is None) and not (
                    any(map(str.isdigit, list(board.buildings.keys())[rand_int]))) and \
                    not board.check_for_nearby_settlements(list(board.buildings.keys())[rand_int]):
                accepted = True
                building = list(board.buildings.keys())[rand_int]
                board.buildings[building].update({'player': self, 'building': 'settlement'})
                potential_roads = []
                for road in board.roads:
                    if building in road:
                        potential_roads.append(road)

                accepted_road = False
                while accepted_road is False:
                    rand_int = random.randint(0, len(potential_roads) - 1)
                    if board.roads[list(board.roads.keys())[rand_int]]['player'] is None:
                        accepted_road = True
                        board.roads[potential_roads[rand_int]].update({'player': self})

        print(f'{self} has placed their initial settlement at {building}')

        return building

    def robber(self, board):
        tile_letters = []
        for tile in board.tiles:
            if tile.resource != 'desert':
                tile_letters.append(tile.letter)
        board.move_robber(tile_letters[random.randint(0, len(tile_letters) - 1)])

    def robber_discard(self, board):
        while len(self.resources) > 7:
            rand_int = random.randint(0, len(self.resources) - 1)
            board.return_player_card(self, self.resources[rand_int])

    def turn_actions(self, board):
        print(f'{self} is deciding what to do this turn')
