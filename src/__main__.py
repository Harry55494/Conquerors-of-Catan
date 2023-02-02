from src.game import *

match_queue = []

if __name__ == "__main__":

    # Define the players and the board. Turns happen in the order specified here
    players = [ai_random(2, "red"), ai_minimax(1, "yellow")]

    match = game(players)
    match_queue.append(match)

    for match in match_queue:
        match.initial_placement()
        match.play()
        results = match.results
        print("Results: " + str(results))
