"""
Main file for the Conquerors of Catan game.
Controls the setup and running of games
Collects Stats and Produces Graphs

Usage:
python3 -m src [--no-menu]

Options:
--no-menu    Skips the menu and starts the game immediately with the default settings and players

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com. For the full licence, please see LICENCE.txt (https://github.com/Harry55494/conquerors-of-catan/blob/master/LICENCE)
"""
import shutil
import signal

from matplotlib.ticker import MaxNLocator

from game import *
from datetime import datetime

import matplotlib.pyplot as plt

if __name__ == "__main__":

    os.system("clear" if os.name == "posix" else "cls")

    print(
        """
        Conquerors of Catan - A Settlers of Catan AI Project - Copyright © 2023 HARRISON PHILLINGHAM
        This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; type `show c' for details.
        """
    )

    time.sleep(3)

    # Add a handler for the keyboard interrupt signal

    def keyboard_interrupt_handler(signal, frame):
        print(
            "\n\nKeyboardInterrupt (ID: {}) has been caught. Exiting...".format(signal)
        )
        shutil.rmtree("temp")
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

    players = [
        # player(1, "blue"),
        ai_random(1, "blue"),
        ai_random(2, "red"),
        ai_minimax(
            3,
            "yellow",
            wishful_thinking=True,
            heuristic_modifiers=[HMDevelopmentCardSpam()],
        ),
    ]

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
            print("4. Licence and Information")
            print("5. Exit")
            if all(isinstance(player, ai_player) for player in players):
                print(
                    "\n! - All players are AI players. The game will be for observation purposes only.\n"
                    "    This can be changed in the player configuration menu.\n"
                )

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
                            if all(isinstance(player, ai_player) for player in players):
                                print(
                                    "\n! - All players are AI players. The game will be for observation purposes only.\n"
                                )

                            answer = input("")

                            # If the length of the players is too high, prevent them adding anymore
                            if answer == str(len(players) + 1):
                                if len(players) == 5:
                                    print("You cannot add any more players")
                                    time.sleep(2)
                                    continue

                                modifiers_to_add = []
                                wt = True

                                # Choose the type of AI to add
                                potential_player = ["human", "random", "minimax"]
                                print("Please choose the number of a player to add:")
                                for i, ai in enumerate(potential_player):
                                    print(str(i + 1) + ". " + ai)
                                player_choice = int(input(""))
                                if player_choice == 1:
                                    ai = player.player
                                elif player_choice == 2:
                                    ai = ai_random
                                elif player_choice == 3:
                                    ai = ai_minimax

                                    modifiers = [
                                        HMEarlyExpansion(),
                                        HMIgnorePorts(),
                                        HMDevelopmentCardSpam(),
                                        HMFavourResources(),
                                    ]
                                    print(
                                        "Please choose the number of a heuristic modifier to add, or type 'done' when you are happy with your selection:"
                                    )
                                    print(
                                        "You can also type 'WT' to toggle wishful thinking"
                                    )
                                    for i, modifier in enumerate(modifiers):
                                        print(str(i + 1) + ". " + modifier.name)
                                    while True:
                                        print(
                                            "Current modifiers: ["
                                            + ", ".join(
                                                [
                                                    modifier.name
                                                    for modifier in modifiers_to_add
                                                ]
                                                + ["WT" if wt else ""]
                                            )
                                            + "]"
                                        )
                                        mod = input()
                                        if mod.lower() == "done":
                                            break
                                        elif mod.lower() == "WT":
                                            wt = not wt
                                            print(
                                                "Wishful thinking is now "
                                                + ("on" if wt else "off")
                                            )
                                        else:
                                            try:
                                                modifier = modifiers[int(mod) - 1]
                                                if modifier in modifiers_to_add:
                                                    print("Removing modifier")
                                                    modifiers_to_add.remove(modifier)
                                                else:
                                                    print("Adding modifier")
                                                    modifiers_to_add.append(modifier)
                                            except:
                                                print("Invalid input")
                                                continue

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
                                if player_choice != 3:
                                    players.append(
                                        ai(
                                            len(players) + 1,
                                            random.choice(available_colours),
                                        )
                                    )

                                else:
                                    players.append(
                                        ai(
                                            len(players) + 1,
                                            random.choice(available_colours),
                                            heuristic_modifiers=modifiers_to_add,
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
                            option_mapping = {
                                "1": {
                                    "CONFIG": "number_of_matches",
                                    "Prompt": "Number of Matches",
                                },
                                "2": {
                                    "CONFIG": "target_score",
                                    "Prompt": "Victory Point Target",
                                },
                                "3": {
                                    "CONFIG": "table_top_mode",
                                    "Prompt": "Table Top Mode",
                                },
                                "4": {
                                    "CONFIG": "display_mode_focus",
                                    "Prompt": "Display Mode",
                                },
                                "5": {
                                    "CONFIG": "board_layout",
                                    "Prompt": "Board Layout",
                                },
                                "6": {
                                    "CONFIG": "randomise_starting_locations",
                                    "Prompt": "Randomise Starting Locations",
                                },
                            }
                            print(
                                "\nSelect a number to modify the current setup, or return to go back:\n"
                            )

                            for option in option_mapping:
                                print(
                                    option
                                    + ". "
                                    + option_mapping[option]["Prompt"].ljust(35)
                                    + str(CONFIG[option_mapping[option]["CONFIG"]])
                                    .rjust(7)
                                    .title()
                                )
                            print(len(option_mapping) + 1, ". Return")
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

                            elif answer == 5:
                                print(
                                    "Please enter which board layout you want, 'default' or 'random'"
                                )
                                print("1. Default")
                                print("2. Random")
                                answer = int(input(""))
                                if answer == 1:
                                    CONFIG["board_layout"] = "default"
                                elif answer == 2:
                                    CONFIG["board_layout"] = "random"
                                else:
                                    raise ValueError

                            elif answer == 6:
                                print(
                                    "Please enter whether you would like to randomise starting locations (y/n):"
                                )
                                answer = input("")
                                if answer == "y":
                                    CONFIG["randomise_starting_locations"] = True
                                elif answer == "n":
                                    CONFIG["randomise_starting_locations"] = False
                                else:
                                    raise ValueError

                            # Catch invalid options
                            elif answer == 7:
                                break

                        # Catch invalid values
                        except ValueError:
                            print("Invalid choice!")
                            time.sleep(1)
                            continue

                # Print the licence and information
                elif choice == 4:
                    os.system("clear" if os.name == "posix" else "cls")
                    print(
                        """
                        Conquerors of Catan - A Settlers of Catan AI Project
                        © 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com
                        This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
                        This is free software, and you are welcome to redistribute it
                        under certain conditions; type `show c' for details.

                        For the full licence, please see LICENCE.txt (https://github.com/Harry55494/conquerors-of-catan/blob/master/LICENCE)
                        """
                    )
                    await_user_input("Press enter to return to the menu")

                # Exit the program, with a farewell message
                elif choice == 5:
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

    players_list = [players]
    if "--no-menu" in sys.argv:
        # Create additional sets of players to test
        # players_list.extend(...)
        pass
    else:
        players_list = [players]

    for players_set in players_list:

        # Setup Logging

        if not os.path.exists("temp"):
            os.makedirs("temp")
        for file in os.listdir("temp"):
            if file.startswith("match_"):
                shutil.rmtree(f"temp/{file}")

        print("Clearing logs...")
        for file in os.listdir("logs/players"):
            os.remove(os.path.join("logs/players", file))

        for player in players_set:
            if isinstance(player, ai_player):
                player.make_log_file()

        # Setup Game

        match_queue = []
        results_list = {}
        match_turns = {}
        times = []
        player_turn_times = {}

        players = players_set

        # Create Match
        for i in range(CONFIG["number_of_matches"]):
            players = copy.deepcopy(players)
            match = game(players, [i + 1, CONFIG["number_of_matches"]])
            match_queue.append(match)
            print("Match " + str(i + 1) + " created")

        # Run Matches
        for match in match_queue:
            match_number = str(match_queue.index(match) + 1)
            print(
                "Starting Match "
                + match_number
                + " of "
                + str(CONFIG["number_of_matches"])
            )
            # Player placement and playing
            match.initial_placement()
            match.play()
            # Get Match results
            results = match.results
            results_list[match_number] = results
            match_turns[match_number] = match.player_num_turns
            times.append(match.duration)
            player_turn_times[match_number] = match.turn_time_total
            print("\nMatch " + match_number + " Results: " + str(results))
            print("\nTotal Results: " + str(results_list))

            shutil.copytree("logs", f"temp/match_{match_number}")

            figure = plt.figure()
            for player in match.players:
                plt.plot(
                    range(len(match.player_victory_points[player.name])),
                    match.player_victory_points[player.name],
                    label=player.name,
                    color=player.matplotlib_colour,
                    marker=" ",
                )
            plt.xlabel("Turn")
            plt.ylabel("Victory Points")
            plt.title(f"Match {match_number} - Victory Points")

            ax = plt.gca()
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())

            plt.savefig(f"temp/match_{match_number}/victory_points.png")

            if CONFIG["presentation_mode"]:
                print(f"Next match in 15 ... ", end="")
                for i in range(14, 0, -1):
                    time.sleep(1)
                    print(f"{i} ... ", end="")
            else:
                time.sleep(3) if not CONFIG["presentation_mode"] else time.sleep(15)

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
            data.append(
                str(round(total_wins / CONFIG["number_of_matches"] * 100, 2)) + "%"
            )
            data.append(round(total_points / CONFIG["number_of_matches"], 2))

            total_time = 0
            for time__ in player_turn_times.values():
                total_time += time__[player.name]

            # Calculate the average number of turns it takes to win
            # If the player didn't win, calculate the average number of turns it would take to win at that pace
            # Also Calculates the average turn time, as both require iterating over the turn maps
            rounds_to_win = []

            total_player_turns = 0
            for mt, results in zip(match_turns.values(), results_list.values()):
                num_turns = int(mt[player.name])
                result = results[player.name]
                if result >= CONFIG["target_score"]:
                    rounds_to_win.append(num_turns)
                else:
                    progress = (num_turns / result) * (CONFIG["target_score"])
                    rounds_to_win.append(progress)
                total_player_turns += num_turns
            average_time = round(total_time / total_player_turns, 2)

            data.append(round(sum(rounds_to_win) / len(rounds_to_win), 3))

            data.append(str(average_time) + "s")

            # Append that player's data for that match into the overall list
            player_data.append(data)

        # Sort the data based on player number
        player_data.sort(key=lambda x: (x[1]), reverse=True)

        for person in player_data:
            person[1] = f"{person[1]}"
            person[2] = f"{person[2]:.2f}"
            person[3] = f"{person[3]:.3f}"
            person[4] = f"{person[4]}"

        time_ = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        # Print data using tabulate to format it nicely
        print("\nFinal Results: \n")
        tabbed_data = tabulate(
            player_data,
            headers=[
                "Player",
                "Win Rate",
                "Avg Victory Points",
                "Avg Turns to Win",
                "Avg Turn Time",
            ],
            tablefmt="simple_grid",
        )
        print(tabbed_data)

        average_time = sum(times) / len(times)
        average_time = round(average_time / 60, 2)
        print("\nAverage Time per Match: " + str(average_time) + " minutes\n")

        # Save the data to a file
        if not os.path.exists("games"):
            os.mkdir("games")

        shutil.copytree("temp", "games/" + time_)

        with open("games/" + time_ + "/results.txt", "w+") as file:
            file.write(tabbed_data)

        # No point showing graphs for less than one match
        if CONFIG["number_of_matches"] > 1:

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
                    color=player.matplotlib_colour,
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
                    color=player.matplotlib_colour,
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
                "Results of "
                + str(CONFIG["number_of_matches"])
                + " Matches at "
                + time_
            )

            if not os.path.exists("games"):
                os.mkdir("games")
            if not os.path.exists(f"games/{time_}"):
                os.mkdir(f"games/{time_}")

            # Save figure
            plt.savefig(f"games/{time_}/vp_matches.png")

            shutil.rmtree("temp")

            # Show it
            plt.show()

        else:

            print("\nNot enough matches to plot results")
