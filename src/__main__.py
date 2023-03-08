import signal

from src.game import *
from tabulate import tabulate
from datetime import datetime

if __name__ == "__main__":

    def keyboard_interrupt_handler(signal, frame):
        print(
            "\n\nKeyboardInterrupt (ID: {}) has been caught. Exiting...".format(signal)
        )
        exit(signal)

    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    print("Setting up Game...")

    players = [ai_random(2, "red"), ai_minimax(1, "yellow")]

    # Import Arguments

    if "--no-menu" in sys.argv:
        print("Skipping Menu")

    else:

        first = True

        while True:
            os.system("clear" if os.name == "posix" else "cls")
            if first:
                for letter in "\nWelcome to Conquerors of Catan!\n":
                    print(letter, end="")
                    sys.stdout.flush()
                    time.sleep(0.1)
                time.sleep(0.1)
                first = False
            else:
                print("\nWelcome to Conquerors of Catan!")

            print("\nPlease select an option:")
            print("1. Play Game")
            print("2. Configure Players")
            print("3. Configure Game Options")
            print("4. Exit")
            try:
                choice = int(input(""))
                if choice == 1:
                    for letter in "Starting game in ":
                        print(letter, end="")
                        sys.stdout.flush()
                        time.sleep(0.1)
                    for i in range(3, 0, -1):
                        print(str(i) + " ", end="")
                        time.sleep(1)
                    break
                elif choice == 2:

                    while True:

                        try:

                            os.system("clear" if os.name == "posix" else "cls")
                            print(
                                "\nPlease enter a player number to remove them, or type new to add a new player:\n"
                            )
                            sorted_ = sorted(players, key=lambda x: x.number)
                            for player in sorted_:
                                print(player)
                            print(len(players) + 1, "- Return")

                            answer = input("")
                            if answer == "new":
                                potential_ais = ["random", "minimax", "mcts"]
                                print("Please select an AI to add:")
                                for i, ai in enumerate(potential_ais):
                                    print(str(i + 1) + ". " + ai)
                                ai_choice = int(input(""))
                                if ai_choice == 1:
                                    ai = ai_random
                                elif ai_choice == 2:
                                    ai = ai_minimax
                                elif ai_choice == 3:
                                    ai = ai_mcts
                                else:
                                    raise ValueError
                                available_colours = ["red", "yellow", "blue", "green"]
                                for colour in [player.colour for player in players]:
                                    available_colours.remove(colour)
                                players.append(
                                    ai(
                                        len(players) + 1,
                                        random.choice(available_colours),
                                    )
                                )

                            elif answer == str(len(players) + 1):
                                break
                            else:
                                if len(players) == 2:
                                    print("You cannot remove any more players")
                                    time.sleep(2)
                                    continue
                                answer = int(answer)
                                for i, player in enumerate(players):
                                    if player.number == answer:
                                        players.pop(i)

                                    for j, player_ in enumerate(players):
                                        player.number = i + 1
                                else:
                                    raise ValueError

                        except ValueError:
                            print("Invalid choice!")
                            time.sleep(1)
                            continue

                elif choice == 3:

                    while True:
                        try:
                            os.system("clear" if os.name == "posix" else "cls")
                            print(
                                "\nSelect a number to modify the current setup, or return to go back:\n"
                            )
                            print(
                                "1. Number of Matches: "
                                + str(CONFIG["number_of_matches"])
                            )
                            print(
                                "2. Victory Point Target: "
                                + str(CONFIG["target_score"])
                            )
                            print("3. Table Top Mode: " + str(CONFIG["table_top_mode"]))
                            print("4. Return")
                            answer = int(input(""))
                            if answer == 1:
                                print(
                                    "Please enter the number of matches you would like to play:"
                                )
                                new_val = int(input(""))
                                if 0 < new_val < 100:
                                    CONFIG["number_of_matches"] = new_val
                                else:
                                    raise ValueError
                            elif answer == 2:
                                print("Please enter the target score for a match:")
                                new_val = int(input(""))
                                if 3 < new_val < 100:
                                    CONFIG["target_score"] = new_val
                                else:
                                    raise ValueError
                            elif answer == 3:
                                print(
                                    "Please enter whether you would like to play in Table Top Mode (y/n):"
                                )
                                answer = input("")
                                if answer == "y":
                                    CONFIG["table_top_mode"] = True
                                elif answer == "n":
                                    CONFIG["table_top_mode"] = False
                                else:
                                    raise ValueError
                            elif answer == 4:
                                break

                        except ValueError:
                            print("Invalid choice!")
                            time.sleep(1)
                            continue

                elif choice == 4:
                    for letter in "Farewell!":
                        print(letter, end="", flush=True)
                        time.sleep(0.1)
                    sys.exit(0)
                else:
                    raise ValueError

            except ValueError:
                print("Invalid choice!")
                time.sleep(1)
                continue

    # Setup Logging

    if not os.path.exists("logs"):
        os.mkdir("logs")
        os.mkdir("logs/players")

    for file in os.listdir("logs/players"):
        os.remove(os.path.join("logs/players", file))

    # Setup Game

    match_queue = []
    results_list = {}

    # Create Match
    for i in range(CONFIG["number_of_matches"]):
        players = copy.deepcopy(players)
        match = game(players)
        match_queue.append(match)
        print("Match " + str(i + 1) + " created")

    # Run Matches
    for match in match_queue:
        match_number = str(match_queue.index(match) + 1)
        print(
            "Starting Match " + match_number + " of " + str(CONFIG["number_of_matches"])
        )
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
        data.append(str(total_wins / CONFIG["number_of_matches"] * 100) + "%")
        data.append(total_points / CONFIG["number_of_matches"])
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

    if CONFIG["number_of_matches"] > 1:

        # Plot Results

        import matplotlib.pyplot as plt

        time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        # Also add graph that shows the cumulative scores over time
        # Compare it to the average needed to win 50% of games
        # Should be a good comparison of how well the AIs are doing

        fig, ax = plt.subplots(1, 2, figsize=(13, 7))
        ax1, ax2 = ax.flatten()

        # Victory Points Per Match
        ax1.plot(
            [0, CONFIG["number_of_matches"]],
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
            ax.xaxis.set_major_locator(
                plt.MaxNLocator(min(CONFIG["number_of_matches"], 10))
            )
            # order legend by player number
            handles, labels = ax.get_legend_handles_labels()
            handles, labels = zip(*sorted(zip(handles, labels), key=lambda t: t[1]))
            ax.legend(handles, labels)

        fig.suptitle(
            "Results of " + str(CONFIG["number_of_matches"]) + " Matches at " + time
        )

        plt.savefig(f"graphs/{time}_figure.png")

        plt.show()

    else:

        print("Not enough matches to plot results")
