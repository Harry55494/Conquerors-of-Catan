"""
Configuration file for the games
Is overwritten by anything set while the program is running, but then will return to this upon a restart

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com. For the full licence, please see LICENCE.txt (https://github.com/Harry55494/conquerors-of-catan/blob/master/LICENCE)
"""


CONFIG = {
    # BOARD / GAME CONFIGURATION ----------------------------------------------
    # Display Mode -
    # Whether to display the board cleanly but with poor text formatting ('board'), or with good text formatting but a flashing screen ('text')
    # Options are 'board' or 'text'. Developer recommended is 'text'
    "display_mode_focus": "text",
    # Target Score -
    # Modify the target score for shorter or longer games
    # Minimum is 3
    "target_score": 10,
    # Number of Matches -
    # Number of matches to play in a row before generating results and exiting
    "number_of_matches": 1,
    # Board Layout -
    # Set to either 'default' or 'random'
    # 'default' will use the standard board layout
    # 'random' will use a random board layout
    "board_layout": "default",
    # Table Top Mode -
    # If enabled, waits for a keypress after each AI turn, to acknowledge the move
    # Used only when playing with a physical board, not required when playing with a human on the computer
    "table_top_mode": False,
    # Randomise Starting Locations -
    # If enabled, the starting locations of all players will be randomised
    "randomise_starting_locations": False,
    # Presentation Mode
    "presentation_mode": False,
    # MINIMAX CONFIGURATION ---------------------------------------------------
    # Minimax Depth -
    # Depth to which the minimax algorithm will search
    # 0 means it only looks at the current state
    "minimax_max_depth": 6,
    # MiniMax Max Time -
    # Maximum time in seconds that the MiniMax algorithm will take to find the best move
    # If it takes longer than this, it will return the best move it has found so far
    "minimax_time_limit": 30,
    # Log MiniMax Score Calculation -
    # If enabled, logs the score calculation for each move in the MiniMax algorithm
    # This is useful for debugging, but will fill up the log file very quickly
    "log_minimax_score_calculation": False,
    # Epsilon Pruning Level -
    # If enabled, the MiniMax algorithm will use epsilon pruning to speed up the search
    # Epsilon pruning evaluates similar moves before appending them to the tree, to avoid unnecessary calculations
    # Provides a large speed boost, but a slight loss in performance
    # 0 = Disabled
    # 1 = Development Cards and Trades Only
    # 2 = All Moves
    # Recommended Level is 1
    # See README.md for more information
    "epsilon_pruning_level": 1,
    # AI CONFIGURATION --------------------------------------------------------
    # Maximum Moves per Turn -
    # Set the maximum number of moves that can be made in a single turn, per player type
    "max_moves_per_turn_human": None,
    "max_moves_per_turn_ai": 5,
    # AI Doesn't Initiate Trades -
    # If enabled, the AI will not initiate trades
    # This can save a lot of time in the MiniMax algorithm
    "ai_doesnt_initiate_trades": True,
    # Sort Order for Moves -
    # Set the order in which the AI will evaluate moves
    # Can influence the AI's strategy if the full move set is not explored
    "move_sort_order": [
        "build city",
        "build settlement",
        "build road",
        "play development card",
        "trade with player",
        "trade with port",
        "trade with bank",
        "buy development card",
        "end turn",
    ],
    # MatPlotLib Colour Mappings
    "colour_mappings": {
        "blue": "#1f77b4",
        "red": "#d62728",
        "green": "#2ca02c",
        "yellow": "#ff7f0e",
        "cyan": "#17becf",
        "magenta": "#9467bd",
    },
}
