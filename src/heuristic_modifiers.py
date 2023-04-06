"""
Heuristic Modifiers, to provide varying strategies for the AI player
Multiple Modifiers can be chained together to create a more complex strategy

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""
import sys


class HeuristicModifier:
    def __init__(self, name):
        self.name = name
        if self.__class__ is HeuristicModifier:
            raise TypeError("HeuristicModifier cannot be instantiated directly")
        pass

    def __call__(self, interface, score_map):
        return score_map


# ----------------------------------------------


class HMDefault(HeuristicModifier):
    def __init__(self):
        super().__init__("Default")

    def __call__(self, interface, score_map):
        return score_map


class HMHeavilyFavourCities(HeuristicModifier):
    def __init__(self):
        super().__init__("Heavily Favour Cities")

    def __call__(self, interface, score_map):
        for city in self.game.cities:
            score_map[city.position] += 1000
        return score_map
