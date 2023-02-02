from src.ai_player import ai_player


class ai_random(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="rule-based")
