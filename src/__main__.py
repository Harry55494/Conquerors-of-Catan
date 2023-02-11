from src.game import *
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import datetime

if __name__ == "__main__":

    for file in os.listdir("logs/players"):
        os.remove(os.path.join("logs/players", file))

    players = [ai_random(2, "red"), ai_minimax(1, "yellow")]
    match_queue = []
    results_list = {}
    number_of_matches = 1

    # Create Match
    for i in range(number_of_matches):
        players = copy.deepcopy(players)
        match = game(players)
        match_queue.append(match)
        print("Match " + str(i + 1) + " created")

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
            highest_score = max(results.values())
            if results[player.name] == highest_score:
                total_wins += 1
        data.append(
            player.name
            + " ("
            + (player.strategy if isinstance(player, ai_player) else "")
            + ")"
        )
        data.append(str(total_wins / number_of_matches * 100) + "%")
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

        time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        # Also add graph that shows the cumulative scores over time
        # Compare it to the average needed to win 50% of games
        # Should be a good comparison of how well the AIs are doing

        fig, ax = plt.subplots(1, 2, figsize=(13, 7))
        ax1, ax2 = ax.flatten()

        # Victory Points Per Match
        ax1.plot(
            [0, number_of_matches],
            [CONFIG["target_score"], CONFIG["target_score"]],
            label="Win Threshold",
            linestyle="--",
            color="red",
        )

        for player in players:
            ax1.plot(
                list(results_list.keys()),
                [results[player.name] for results in results_list.values()],
                label=(
                    player.name
                    + " ("
                    + (player.strategy if isinstance(player, ai_player) else "")
                    + ")"
                ),
                marker="x",
            )

        ax1.set_xlabel("Match No.")
        ax1.set_ylabel("Victory Points")
        ax1.set_title("Victory Points Per Match")

        # Plot cumulative scores over time

        for player in players:
            cumulative_score = 0
            cumulative_scores = []
            for results in results_list.values():
                cumulative_score += results[player.name]
                cumulative_scores.append(cumulative_score)
            ax2.plot(
                list(results_list.keys()),
                cumulative_scores,
                label=(
                    player.name
                    + " ("
                    + (player.strategy if isinstance(player, ai_player) else "")
                    + ")"
                ),
                marker="x",
            )

        ax2.set_xlabel("Match No.")
        ax2.set_ylabel("Cumulative Victory Points")
        ax2.set_title("Cumulative V.P. Per Match")

        # Shared axis management:
        for ax in [ax1, ax2]:
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(plt.MaxNLocator(min(number_of_matches, 10)))
            # order legend by player number
            handles, labels = ax.get_legend_handles_labels()
            handles, labels = zip(*sorted(zip(handles, labels), key=lambda t: t[1]))
            ax.legend(handles, labels)

        plt.savefig(f"graphs/{time}_figure.png")

        plt.show()

    else:

        print("Not enough matches to plot results")
