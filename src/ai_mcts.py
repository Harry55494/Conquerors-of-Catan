from src.ai_player import ai_player


class ai_mcts(ai_player):
    def __init__(self, number, colour):
        super().__init__(number=number, colour=colour, strategy="MCTS")
