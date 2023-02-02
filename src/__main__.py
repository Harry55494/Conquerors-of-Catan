from src.game import *
import matplotlib.pyplot as plt
from tabulate import tabulate

if __name__ == "__main__":

    players = [ai_random(2, "red"), ai_minimax(1, "yellow")]
    match_queue = []
    results_list = {}
    number_of_matches = 3

    # Create Match
    for i in range(number_of_matches):
        players = copy.deepcopy(players)
        match = game(players)
        match_queue.append(match)

    # Run Matches
    for match in match_queue:
        match_number = str(match_queue.index(match) + 1)
        print("Starting Match " + match_number + " of " + str(number_of_matches))
        match.initial_placement()
        match.play()
        results = match.results
        results_list[match_number] = results
        print("\nMatch " + match_number + " Results: " + str(results))
        print("Total Results: " + str(results_list))
        print("\n")
        time.sleep(3)

    player_data = []

    for player in players:
        data = []
        total_points, total_wins = 0, 0
        for results in results_list.values():
            total_points += results[player.name]
            if results[player.name] >= CONFIG["target_score"]:
                total_wins += 1
        data.append(player.name)
        data.append(total_wins / number_of_matches)
        data.append(total_points / number_of_matches)
        player_data.append(data)

    player_data.sort(key=lambda x: x[1], reverse=True)

    print("\n\nFinal Results: \n")
    print(
        tabulate(
            player_data,
            headers=["Player", "Win Rate", "Average Victory Points"],
            tablefmt="grid",
        )
    )

    if number_of_matches > 1:

        # Plot Results

        # plot target score line
        plt.plot(
            [0, number_of_matches],
            [CONFIG["target_score"], CONFIG["target_score"]],
            label="Win Threshold",
            linestyle="--",
            color="red",
        )

        for player in players:
            plt.plot(
                list(results_list.keys()),
                [results[player.name] for results in results_list.values()],
                label=player.name,
                marker="x",
            )

        plt.xlabel("Match No.")
        plt.ylabel("Victory Points")
        plt.title("Victory Points Per Match")
        plt.legend()

        plt.show()
