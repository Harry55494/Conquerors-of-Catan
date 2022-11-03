import random
import time

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
                    any(map(str.isdigit, list(board.buildings.keys())[rand_int]))) and not \
                    board.check_for_nearby_settlements(list(board.buildings.keys())[rand_int]):
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

    def place_road(self, board):
        road_endings = []
        for road in board.roads:
            if board.roads[road]['player'] == self:
                road_endings.append(road[0])
                road_endings.append(road[1])
        not_accepted = True
        while not_accepted:
            rand_int = random.randint(0, len(board.roads) - 1)
            if board.roads[list(board.roads.keys())[rand_int]]['player'] is None:
                if list(board.roads.keys())[rand_int][0] in road_endings or list(board.roads.keys())[rand_int][1] in road_endings:
                    board.roads[list(board.roads.keys())[rand_int]].update({'player': self})
                    not_accepted = False
                    for resource, amount in board.building_cost_list.get('road').items():
                        for i in range(amount):
                            board.return_player_card(self, resource)

    def place_building(self, board, building='settlement'):
        if building == 'settlement':
            road_endings = []
            for road in board.roads:
                if board.roads[road]['player'] == self:
                    if not board.check_for_nearby_settlements(road[0]):
                        road_endings.append(road[0])
                    if not board.check_for_nearby_settlements(road[1]):
                        road_endings.append(road[1])
            if len(road_endings) == 0:
                return False
            not_accepted = True
            while not_accepted:
                time.sleep(0.1)
                rand_int = random.randint(0, len(road_endings) - 1)
                location = road_endings[rand_int]
                if (board.buildings[location]['player'] is None or board.buildings[location]['player'] == self and building == 'settlement') and not board.check_for_nearby_settlements(location):
                    board.buildings[location].update({'player': self, 'building': 'settlement'})
                    not_accepted = False
                    for resource, amount in board.building_cost_list.get('settlement').items():
                        for j in range(amount):
                            board.return_player_card(self, resource)
        elif building == 'city':
            settlements = []
            for building in board.buildings:
                if board.buildings[building]['player'] == self and board.buildings[building]['building'] == 'settlement':
                    settlements.append(building)
            if len(settlements) == 0:
                return False
            not_accepted = True
            while not_accepted:
                rand_int = random.randint(0, len(settlements) - 1)
                location = settlements[rand_int]
                if board.buildings[location]['player'] == self and board.buildings[location]['building'] == 'settlement':
                    board.buildings[location].update({'player': self, 'building': 'city'})
                    not_accepted = False
                    for resource, amount in board.building_cost_list.get('city').items():
                        for i in range(amount):
                            board.return_player_card(self, resource)

    def play_development_card(self, board):

        card = self.development_cards.pop(self.development_cards.index(random.choice(self.development_cards)))
        if card == 'victory point':
            self.development_cards.append('victory point')
            return
        else:
            print(f'{self} is playing a development card - {card}')
            if card == 'soldier':
                self.robber(board)
            elif card == 'monopoly':
                res_type = random.choice(['wheat', 'sheep', 'rock', 'brick', 'wood'])
                for other_player in board.players:
                    if other_player != self:
                        while res_type in other_player.resources:
                            board.return_player_card(other_player, res_type)
                            board.give_player_card(self, 'resource', res_type)
            elif card == 'year of plenty':
                for i in range(2):
                    res_type = random.choice(['wheat', 'sheep', 'rock', 'brick', 'wood'])
                    board.give_player_card(self, 'resource', res_type)
            elif card == 'road building':
                for i in range(2):
                    self.place_road(board)
            board.return_player_card(self, card)


    def buy_development_card(self, board):
        if self.count_cards('resources')['wheat'] >= 1 and self.count_cards('resources')['sheep'] >= 1 and self.count_cards('resources')['rock'] >= 1:
            board.return_player_card(self, 'wheat')
            board.return_player_card(self, 'sheep')
            board.return_player_card(self, 'rock')
            board.give_player_card(self, 'development', 'development')
            return True
        else:
            return False

    def trade_with_bank(self, board, give, get):
        if self.count_cards('resources')[give] >= 4:
            board.return_player_card(self, give)
            board.return_player_card(self, give)
            board.return_player_card(self, give)
            board.return_player_card(self, give)
            board.give_player_card(self, 'resource', get)
            return True
        else:
            return False

    def robber(self, board):
        tile_letters = []
        for tile in board.tiles:
            if tile.resource != 'desert':
                tile_letters.append(tile.letter)
        board.move_robber(tile_letters[random.randint(0, len(tile_letters) - 1)])
        # TODO - add stealing from other players

    def robber_discard(self, board):
        while len(self.resources) > 7:
            rand_int = random.randint(0, len(self.resources) - 1)
            board.return_player_card(self, self.resources[rand_int])

    def turn_actions(self, board):
        hand = self.count_cards('resources')
        buildings_count = {'settlements': 0, 'cities': 0}
        for building in board.buildings:
            if board.buildings[building]['player'] == self:
                if board.buildings[building]['building'] == 'settlement':
                    buildings_count['settlements'] += 1
                elif board.buildings[building]['building'] == 'city':
                    buildings_count['cities'] += 1
        for card in hand:
            if hand[card] >= 4:
                self.trade_with_bank(board, card, random.choice(list(board.resource_deck)))
        if hand['wheat'] >= 2 and hand['rock'] >= 3 and buildings_count['settlements'] > 0:
            self.place_building(board, 'city')
        if hand['wheat'] >= 1 and hand['sheep'] >= 1 and hand['wood'] >= 1 and hand['clay'] >= 1 and buildings_count['settlements'] < 11:
            self.place_building(board)
        if hand['wood'] >= 1 and hand['clay'] >= 1 and board.has_potential_road(self) and random.randint(0, 1) == 1:
            self.place_road(board)
        if hand['sheep'] >= 1 and hand['rock'] >= 1 and hand['wheat'] >= 1 and random.randint(0, 1) == 1:
            self.buy_development_card(board)
        if len(self.development_cards) > 0 and random.randint(0, 1) == 1:
            if 'victory point' in self.development_cards and len(self.development_cards) == 1:
                pass
            else:
                self.play_development_card(board)
