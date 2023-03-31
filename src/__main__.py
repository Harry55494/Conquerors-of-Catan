"""
Main file for the Conquerors of Catan game.
Controls the setup and running of games

Usage:
python3 -m src [--no-menu]

Options:
--no-menu    Skips the menu and starts the game immediately with the default settings and players

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
"""

import signal

from src.game import *
from tabulate import tabulate
from datetime import datetime

if __name__ == "__main__":

    # Add a handler for the keyboard interrupt signal

    def keyboard_interrupt_handler(signal, frame):
        print(
            "\n\nKeyboardInterrupt (ID: {}) has been caught. Exiting...".format(signal)
        )
        exit(signal)

    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    # Setup logging, making directories if they don't exist

    print("Setting up Game...")

    if not os.path.exists("logs"):
        print("Setting up logging...")
        os.mkdir("logs")
    if not os.path.exists("logs/players"):
        os.mkdir("logs/players")

    # Clear logs

    print("Clearing logs...")
    for file in os.listdir("logs/players"):
        os.remove(os.path.join("logs/players", file))

    # Create the default players

    players = [ai_random(1, "red"), ai_minimax(2, "yellow")]

    # If the user has specified the "--no-menu" argument, skip the menu

    if "--no-menu" in sys.argv:
        print("Skipping Menu")

    else:

        # Variable for if the menu has been visited before
        first = True

        # Loop until the user chooses to start the game
        while True:
            os.system("clear" if os.name == "posix" else "cls")
            # Type out the title if it's the first time the menu has been visited
            if first:
                for letter in "\nWelcome to Conquerors of Catan!\n":
                    print(letter, end="")
                    sys.stdout.flush()
                    time.sleep(0.1)
                time.sleep(0.1)
                first = False
            else:
                print("\nWelcome to Conquerors of Catan!")

            # Print Options
            print("\nPlease select an option:")
            print("1. Play Game")
            print("2. Configure Players")
            print("3. Configure Game Options")
            print("4. Exit")

            # Get the user's choice
            try:
                choice = int(input(""))

                # If the user chose to play the game, break out of the loop
                if choice == 1:
                    for letter in "Starting game in ":
                        print(letter, end="")
                        sys.stdout.flush()
                        time.sleep(0.1)
                    for i in range(3, 0, -1):
                        print(str(i) + " ", end="")
                        time.sleep(1)
                    break

                # If the user chose to configure the players, go to the player configuration menu
                elif choice == 2:

                    while True:

                        try:

                            os.system("clear" if os.name == "posix" else "cls")
                            print(
                                "\nPlease enter a player number to remove them, or choose another option:\n"
                            )

                            # Sort and print players
                            sorted_ = sorted(players, key=lambda x: x.number)
                            for player in sorted_:
                                print(player)
                            print(len(players) + 1, "- Add New Player")
                            print(len(players) + 2, "- Return")

                            answer = input("")

                            # If the length of the players is too high, prevent them adding anymore
                            if answer == str(len(players) + 1):
                                if len(players) == 5:
                                    print("You cannot add any more players")
                                    time.sleep(2)
                                    continue

                                # Choose the type of AI to add
                                potential_ais = ["random", "minimax"]
                                print("Please choose the number of an AI to add:")
                                for i, ai in enumerate(potential_ais):
                                    print(str(i + 1) + ". " + ai)
                                ai_choice = int(input(""))
                                if ai_choice == 1:
                                    ai = ai_random
                                elif ai_choice == 2:
                                    ai = ai_minimax
                                else:
                                    raise ValueError

                                # Choose a random colour for the AI, that isn't already in use
                                available_colours = [
                                    "red",
                                    "yellow",
                                    "blue",
                                    "green",
                                    "magenta",
                                    "cyan",
                                ]
                                for colour in [player.colour for player in players]:
                                    available_colours.remove(colour)

                                # Create the AI and append it to the list
                                players.append(
                                    ai(
                                        len(players) + 1,
                                        random.choice(available_colours),
                                    )
                                )

                            elif answer == str(len(players) + 2):
                                break

                            # Else, start the removal process
                            else:

                                # Can't remove anymore players
                                if len(players) == 2:
                                    print("You cannot remove any more players")
                                    time.sleep(2)
                                    continue
                                answer = int(answer)
                                if answer > len(players):
                                    raise ValueError

                                # Ask for confirmation if the answer is correct and valid
                                confirm = input(
                                    "Are you sure you want to remove player "
                                    + str(answer)
                                    + "? (y/n) "
                                )

                                # Find the player and remove them
                                if confirm == "y":
                                    for i, player in enumerate(players):
                                        if player.number == answer:
                                            players.pop(i)

                                        for j, player_ in enumerate(players):
                                            player.number = i + 1
                                elif confirm == "n":
                                    continue
                                else:
                                    raise ValueError

                        # Catch value errors and restart the menu
                        except ValueError:
                            print("Invalid choice!")
                            time.sleep(1)
                            continue

                # Options modifying
                elif choice == 3:

                    while True:
                        try:

                            # Print all the options
                            os.system("clear" if os.name == "posix" else "cls")
                            print(
                                "\nSelect a number to modify the current setup, or return to go back:\n"
                            )
                            print(
                                "1. Number of Matches: ".ljust(25)
                                + str(CONFIG["number_of_matches"]).rjust(5)
                            )
                            print(
                                "2. Victory Point Target: ".ljust(25)
                                + str(CONFIG["target_score"]).rjust(5)
                            )
                            print(
                                "3. Table Top Mode: ".ljust(25)
                                + str(CONFIG["table_top_mode"]).rjust(5)
                            )
                            print(
                                "4. Display Mode: ".ljust(25)
                                + str(CONFIG["display_mode_focus"]).rjust(5)
                            )
                            print("5. Return")

                            # Get the answer
                            answer = int(input(""))

                            # All options perform value checking to make sure they are acceptable
                            # If they are not, a ValueError is raised and caught at the end

                            # Set number of matches
                            if answer == 1:
                                print(
                                    "Please enter the number of matches you would like to play:"
                                )
                                new_val = int(input(""))
                                if 0 < new_val < 100:
                                    CONFIG["number_of_matches"] = new_val
                                else:
                                    raise ValueError

                            # Set target score
                            elif answer == 2:
                                print("Please enter the target score for a match:")
                                new_val = int(input(""))
                                if 3 < new_val < 100:
                                    CONFIG["target_score"] = new_val
                                else:
                                    raise ValueError

                            # Enable or Disable Tabletop mode, for playing next to a board
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

                            # Enter display priority
                            elif answer == 4:
                                print(
                                    "Please enter which display variant you want, 'text' or 'board'\n"
                                    "Text prioritises readability, board makes the board updates smoother."
                                    "\nPick text if you are playing with at least one human player"
                                )
                                print("1. Text")
                                print("2. Board")
                                answer = int(input(""))
                                if answer == 1:
                                    CONFIG["display_mode_focus"] = "text"
                                elif answer == 2:
                                    CONFIG["display_mode_focus"] = "board"
                                else:
                                    raise ValueError

                            # Catch invalid options
                            elif answer == 5:
                                break

                        # Catch invalid values
                        except ValueError:
                            print("Invalid choice!")
                            time.sleep(1)
                            continue

                # Exit the program, with a farewell message
                elif choice == 4:
                    for letter in "\nFarewell Settler!\n":
                        print(letter, end="", flush=True)
                        time.sleep(0.1)
                    sys.exit(0)
                else:
                    raise ValueError

            # If the user enters an invalid choice, the program will ask again.
            # Excepts errors from all submenus too
            except ValueError:
                print("Invalid choice!")
                time.sleep(1)
                continue

    # Setup Logging

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
        # Player placement and playing
        match.initial_placement()
        match.play()
        # Get Match results
        results = match.results
        results_list[match_number] = results
        print("\nMatch " + match_number + " Results: " + str(results))
        print("Total Results: " + str(results_list))
        print("\n")
        time.sleep(3)

    player_data = []

    # Summarise all the data for each game for stats
    # Summarises a match's results for a player, and then appends that round to the players overall scores
    for player in players:
        data = []
        total_points, total_wins = 0, 0
        # Check whether a player has the highest score, meaning they won that game
        for results in results_list.values():
            total_points += results[player.name]
            highest_score = max(results.values())
            if results[player.name] == highest_score:
                total_wins += 1
        # Append each data type
        data.append(
            player.name
            + " ("
            + (player.strategy if isinstance(player, ai_player) else "")
            + ")"
        )
        data.append(str(total_wins / CONFIG["number_of_matches"] * 100) + "%")
        data.append(total_points / CONFIG["number_of_matches"])
        # Append that player's data for that match into the overall list
        player_data.append(data)

    # Sort the data based on player number
    player_data.sort(key=lambda x: x[1], reverse=True)

    # Print data using tabulate to format it nicely
    print("\n\nFinal Results: \n")
    print(
        tabulate(
            player_data,
            headers=["Player", "Win Rate", "Average Victory Points"],
            tablefmt="grid",
        )
    )

    # No point showing graphs for less than one match
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

        # Plot each player's scores
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

        # Add labels
        ax1.set_xlabel("Match No.")
        ax1.set_ylabel("Victory Points")
        ax1.set_title("Victory Points Per Match")

        # Plot cumulative scores over time

        # Create a list of cumulative scores by adding and appending the values
        for player in players:
            cumulative_score = 0
            cumulative_scores = []
            for results in results_list.values():
                cumulative_score += results[player.name]
                cumulative_scores.append(cumulative_score)

            # Plot the players cumulative scores
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

        # Add labels
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

        # Add title
        fig.suptitle(
            "Results of " + str(CONFIG["number_of_matches"]) + " Matches at " + time
        )

        # Save figure
        plt.savefig(f"graphs/{time}_figure.png")

        # Show it
        plt.show()

    else:

        print("Not enough matches to plot results")
