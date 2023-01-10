import random
import time

from ai_player import ai_player


class ai_random(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy='random')

    def initial_placement(self, interface):
        accepted = False
        building = ''
        while accepted is False:

            rand_int = random.randint(0, len(interface.get_buildings_list()) - 1)
            if (interface.get_buildings_list()[list(interface.get_buildings_list().keys())[rand_int]][
                    'player'] is None) and not (
                    any(map(str.isdigit, list(interface.get_buildings_list().keys())[rand_int]))) and not \
                    interface.check_for_nearby_settlements(list(interface.get_buildings_list().keys())[rand_int]):
                accepted = True
                building = list(interface.get_buildings_list().keys())[rand_int]
                interface.place_settlement(self, building)
                potential_roads = []
                for road in interface.get_roads_list():
                    if building in road:
                        potential_roads.append(road)

                accepted_road = False
                while accepted_road is False:
                    rand_int = random.randint(0, len(potential_roads) - 1)
                    if interface.get_roads_list()[list(interface.get_roads_list().keys())[rand_int]]['player'] is None:
                        accepted_road = True
                        interface.place_road(self, potential_roads[rand_int])

        print(f'{self} has placed their initial settlement at {building}')

        return building

    def choose_road_location(self, interface):
        road_endings = []
        total_roads = 0
        for road in interface.get_roads_list():
            if interface.get_roads_list()[road]['player'] == self:
                total_roads += 1
                road_endings.append(road[0])
                road_endings.append(road[1])
        if total_roads == 15:
            return False
        not_accepted = True
        while not_accepted:
            rand_int = random.randint(0, len(interface.get_roads_list()) - 1)
            if interface.get_roads_list()[list(interface.get_roads_list().keys())[rand_int]]['player'] is None:
                if list(interface.get_roads_list().keys())[rand_int][0] in road_endings or \
                        list(interface.get_roads_list().keys())[rand_int][1] in road_endings:
                    return list(interface.get_roads_list().keys())[rand_int]

    def choose_placement_location(self, interface, building_type='settlement'):

        settlements_count = 0
        cities_count = 0
        for building in interface.get_buildings_list():
            if interface.get_buildings_list()[building]['player'] == self:
                if interface.get_buildings_list()[building]['building'] == 'settlement':
                    settlements_count += 1
                elif interface.get_buildings_list()[building]['building'] == 'city':
                    cities_count += 1

        if building_type == 'settlement':

            if settlements_count == 5:
                print(f'{self} has no more settlements to place')
                return False

            road_endings = []
            for road in interface.get_roads_list():
                if interface.get_roads_list()[road]['player'] == self:
                    if not interface.check_for_nearby_settlements(road[0]):
                        road_endings.append(road[0])
                    if not interface.check_for_nearby_settlements(road[1]):
                        road_endings.append(road[1])
            if len(road_endings) == 0:
                print(f'{self} has no places they can build settlements')
                return False
            not_accepted = True
            while not_accepted:
                time.sleep(0.1)
                rand_int = random.randint(0, len(road_endings) - 1)
                location = road_endings[rand_int]
                if (interface.get_buildings_list()[location]['player'] is None or
                    interface.get_buildings_list()[location][
                        'player'] == self and building == 'settlement') and not interface.check_for_nearby_settlements(
                    location):
                    return location

        elif building_type == 'city':
            settlements = []
            for building in interface.get_buildings_list():
                if interface.get_buildings_list()[building]['player'] == self and \
                        interface.get_buildings_list()[building]['building'] == 'settlement':
                    settlements.append(building)
            if len(settlements) == 0:
                return False
            not_accepted = True
            while not_accepted:
                rand_int = random.randint(0, len(settlements) - 1)
                location = settlements[rand_int]
                if interface.get_buildings_list()[location]['player'] == self and \
                        interface.get_buildings_list()[location]['building'] == 'settlement':
                    return location

        else:
            print('Invalid building type')

    def play_development_card(self, interface):

        card = self.development_cards[self.development_cards.index(random.choice(self.development_cards))]
        if card == 'victory point':
            return
        else:
            print(f'{self} is playing a development card - {card}')
            if card == 'soldier':
                if self.development_cards.count('soldier') > self.played_robber_cards:
                    self.robber(interface)
                    self.played_robber_cards += 1

            elif card == 'monopoly':
                res_type = random.choice(['wheat', 'sheep', 'rock', 'brick', 'wood'])
                for other_player in interface.get_players_list():
                    if other_player != self:
                        while res_type in other_player.resources:
                            interface.return_player_card(other_player, res_type)
                            interface.give_player_card(self, 'resource', res_type)
            elif card == 'year of plenty':
                for i in range(2):
                    res_type = random.choice(['wheat', 'sheep', 'rock', 'brick', 'wood'])
                    interface.give_player_card(self, 'resource', res_type)
            elif card == 'road building':
                for i in range(2):
                    self.choose_road_location(interface)
            if not card == 'soldier':
                interface.return_player_card(self, card)

    def robber(self, interface):
        tile_letters = []

        for tile in interface.get_tiles_list():
            if tile.resource != 'desert':
                tile_letters.append(tile.letter)
        interface.move_robber(tile_letters[random.randint(0, len(tile_letters) - 1)])
        # TODO - add stealing from other players

    def robber_discard(self, interface):
        while len(self.resources) > 7:
            rand_int = random.randint(0, len(self.resources) - 1)
            interface.return_player_card(self, self.resources[rand_int])

    def turn_actions(self, board, interface):
        hand = self.count_cards('resources')
        buildings_count = {'settlements': 0, 'cities': 0}
        for building in interface.get_buildings_list():
            if interface.get_buildings_list()[building]['player'] == self:
                if interface.get_buildings_list()[building]['building'] == 'settlement':
                    buildings_count['settlements'] += 1
                elif interface.get_buildings_list()[building]['building'] == 'city':
                    buildings_count['cities'] += 1
        for card in hand:
            if hand[card] >= 4:
                interface.trade_with_bank(self, card, random.choice(list(interface.get_resource_deck())))
        hand = self.count_cards('resources')
        if hand['wheat'] >= 2 and hand['rock'] >= 3 and buildings_count['settlements'] > 0:
            location = self.choose_placement_location(interface, 'city')
            if location:
                interface.place_city(self, location)
        hand = self.count_cards('resources')
        if hand['wheat'] >= 1 and hand['sheep'] >= 1 and hand['wood'] >= 1 and hand['clay'] >= 1 and buildings_count[
            'settlements'] < 11:
            location = self.choose_placement_location(interface)
            if location:
                interface.place_settlement(self, location)
        hand = self.count_cards('resources')
        if hand['wood'] >= 1 and hand['clay'] >= 1 and interface.has_potential_road(self) and random.randint(0, 1) == 1:
            location = self.choose_road_location(interface)
            if location:
                interface.place_road(self, location)
        hand = self.count_cards('resources')
        if hand['sheep'] >= 1 and hand['rock'] >= 1 and hand['wheat'] >= 1 and random.randint(0, 2) == 1:
            interface.buy_development_card(self)
        if len(self.development_cards) > 0 and random.randint(0, 1) == 1:
            if 'victory point' in self.development_cards and len(self.development_cards) == 1:
                pass
            else:
                self.play_development_card(interface)
