"""
Heuristic Modifiers, to provide varying strategies for the AI player
Multiple Modifiers can be chained together to create a more complex strategy

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""


def player_heuristic_stats():
    return {
        "victory points": None,
        "settlements": {},
        "cities": {},
        "roads": {},
        "ports": {},
    }


class HeuristicModifier:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation
        if self.__class__ is HeuristicModifier:
            raise TypeError("HeuristicModifier cannot be instantiated directly")
        pass

    def __call__(self, interface, stats_map, mod_map):
        """
        Method used to apply the heuristic modifier to the score
        :param interface: The interface to the game
        :param score: The current score
        :param stats_map: The stats of the player
        :return: The new score and stats map
        """
        raise NotImplementedError("HeuristicModifier.__call__ must be overridden")


# ----------------------------------------------


class HMDefault(HeuristicModifier):
    def __init__(self):
        super().__init__("Default", "D")

    def __call__(self, interface, stats_map, mod_map):

        score = 0
        mod_map = {}

        # Victory Points ----------------------------
        score += 10 * stats_map["victory points"]
        mod_map["victory points"] = 10 * stats_map["victory points"]

        # Winning or Close to Winning ----------------------------
        if stats_map["victory points"] - 1 == stats_map["target score"]:
            score += 10000
            mod_map["close to winning"] += 10000

        if stats_map["victory points"] > stats_map["other players"][
            0
        ].calculateVictoryPoints(interface):
            score += 100
            mod_map = mod_map | {"leading": 100}
        elif stats_map["victory points"] == stats_map["other players"][
            0
        ].calculateVictoryPoints(interface):
            score += 50
            mod_map = mod_map | {"tied": 50}

        # Penalise for relying on development cards to win
        score -= 5 * stats_map["development_cards"].count("victory point")
        mod_map["relying on dev cards"] = -5 * stats_map["development_cards"].count(
            "victory point"
        )

        # Buildings ----------------------------

        for settlement in stats_map["settlements"]:
            score_to_add = 500
            score_to_add += 2 * sum(
                [
                    tile.frequency
                    for tile in stats_map["settlements"][settlement]["nearby tiles"]
                ]
            )
            score_to_add += 2 * len(
                stats_map["settlements"][settlement]["nearby tiles"]
            )
            score += score_to_add
            mod_map["settlement@{}".format(settlement)] = score_to_add

        for city in stats_map["cities"]:
            score_to_add = 1000
            score_to_add += 3 * sum(
                [tile.frequency for tile in stats_map["cities"][city]["nearby tiles"]]
            )
            score_to_add += 2 * len(stats_map["cities"][city]["nearby tiles"])
            score += score_to_add
            mod_map["city@{}".format(city)] = score_to_add

        for port in stats_map["ports"]:
            if stats_map["ports"][port]["type"] == "3:1":
                score += 2 * max(stats_map["roll map"].values())
                mod_map["3:1 port@{}".format(port)] = 2 * max(
                    stats_map["roll map"].values()
                )
            elif stats_map["ports"][port]["type"] == "2:1":
                if stats_map["ports"][port]["resource"] in stats_map["has_access_to"]:
                    mod_map["2:1 port@{}".format(port)] = (
                        2 * stats_map["roll map"][stats_map["ports"][port]["resource"]]
                    )
                    score += (
                        2 * stats_map["roll map"][stats_map["ports"][port]["resource"]]
                    )

        if "average_distance_between_settlements" in stats_map:
            if stats_map["average_distance_between_settlements"] < 6:
                score += 10
                mod_map["settlements close together"] = 10
            if stats_map["average_distance_between_settlements"] > 8:
                score -= 10
                mod_map["settlements far apart"] = -10

        # Resources ----------------------------

        score += len(stats_map["resources"])
        mod_map["resources"] = len(stats_map["resources"])

        # Penalise for having too many resources
        score -= 0.5 * max(len(stats_map["resources"]) - 12, 0)
        mod_map["too many resources"] = -0.5 * max(len(stats_map["resources"]) - 12, 0)

        # Rate higher for having more resources nearby
        score += 3 * len(stats_map["has_access_to"])
        mod_map["has access to"] = 3 * len(stats_map["has_access_to"])

        resources = stats_map["resources"]
        if resources.count("rock") >= 3 and resources.count("grain") >= 2:
            score += 50
            mod_map["can build city"] = 50
        if (
            resources.count("wood") >= 1
            and resources.count("grain") >= 1
            and resources.count("sheep") >= 1
            and resources.count("clay") >= 0
        ):
            score += 25
            mod_map["can build settlement"] = 25
        if resources.count("wood") >= 1 and resources.count("clay") >= 1:
            score += 5
            mod_map["can build road"] = 5
        if (
            resources.count("rock") >= 1
            and resources.count("sheep") >= 1
            and resources.count("grain") >= 1
        ):
            score += 10
            mod_map["can buy development card"] = 10

        score += resources.count("clay")
        mod_map["clay"] = resources.count("clay")
        score += resources.count("rock")
        mod_map["rock"] = resources.count("rock")

        # Special Cards ----------------------------
        if stats_map["longest_road"]:
            mod_map["longest road"] = 50
            score += 50
        if stats_map["largest_army"]:
            mod_map["largest army"] = 50
            score += 50

        # Too far ahead in army
        if stats_map["army_size"] - 2 > max(
            [player.played_robber_cards for player in stats_map["other players"]]
        ):
            score -= 25
            mod_map["too far ahead in army"] = -25

        # Played Robber Cards
        score += stats_map["army_size"] * 3
        mod_map["army size"] = stats_map["army_size"] * 3

        score += stats_map["longest_continuous_road"] * (
            7 if not stats_map["longest_road"] else 2
        )
        mod_map["longest continuous road"] = stats_map["longest_continuous_road"] * (
            7 if not stats_map["longest_road"] else 2
        )

        # Development Cards ----------------------------

        # Penalise for having too many development cards
        score -= 0.5 * max(len(stats_map["development_cards"]) - 12, 0)
        mod_map["too many dev cards"] = -0.5 * max(
            len(stats_map["development_cards"]) - 12, 0
        )

        # Roads ----------------------------

        score -= 1.5 * max(0, len(stats_map["roads"]) - 10)
        mod_map["too many roads"] = -1.5 * max(0, len(stats_map["roads"]) - 10)

        # Nicely spread out settlements
        if len(stats_map["roads"]) > 0:
            if (
                (len(stats_map["settlements"]) + len(stats_map["cities"]))
                / len(stats_map["roads"])
            ) < 2:
                score += 25
                mod_map["nicely spread out settlements"] = 25

            score += stats_map["available_settlement_positions"] * 5
            mod_map["available settlement positions"] = (
                stats_map["available_settlement_positions"] * 5
            )
            if stats_map["opponents_on_roads"]:
                score -= stats_map["opponents_on_roads"] * 5
                mod_map["opponents on roads"] = -stats_map["opponents_on_roads"] * 5

        if score != sum(mod_map.values()):
            raise Exception("Score and mod_map don't add up")

        return sum(mod_map.values()), mod_map


class HMIgnorePorts(HeuristicModifier):
    def __init__(self):
        super().__init__("Ignore Ports", "NP")

    def __call__(self, interface, stats_map, mod_map):
        for key in list(mod_map.keys()):
            if "port" in key:
                mod_map[key] = -50
        return mod_map


class HMEarlyExpansion(HeuristicModifier):
    def __init__(self):
        super().__init__("Early Expansion", "EE")

    def __call__(self, interface, stats_map, mod_map):
        if interface.turn_number < 15 or len(stats_map["roads"]) < 7:
            mod_map["roads"] = 7 * len(stats_map["roads"])
            if "available_settlement_positions" in mod_map:
                mod_map["available_settlement_positions"] = (
                    2 * mod_map["available_settlement_positions"]
                )

        # TODO Own Mod Map Class?
        return mod_map
