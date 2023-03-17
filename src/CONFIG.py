CONFIG = {
    # Minimax Depth -
    # Depth to which the minimax algorithm will search
    # 0 means it only looks at the current state
    "minimax_max_depth": 4,
    # Display Mode -
    # Whether to display the board cleanly but with poor text formatting, or with good text formatting but a flashing screen
    # Options are 'board' or 'text'
    "display_mode_focus": "text",
    # Target Score -
    # Modify the target score for shorter or longer games
    # Minimum is 3
    "target_score": 10,
    # MiniMax Max Time -
    # Maximum time in seconds that the MiniMax algorithm will take to find the best move
    # If it takes longer than this, it will return the best move it has found so far
    "minimax_time_limit": 90,
    # Table Top Mode -
    # If enabled, waits for a keypress after each AI turn, to acknowledge the move
    # Used only when playing with a physical board, not just with a human
    "log_minimax_score_calculation": False,
    # Log MiniMax Score Calculation -
    # If enabled, logs the score calculation for each move in the MiniMax algorithm
    # This is useful for debugging, but will fill up the log file very quickly
    "table_top_mode": False,
    # Number of Matches -
    # Number of matches to play in a row before exiting
    "number_of_matches": 1,
    # Maximum Moves per Turn -
    # Set the maximum number of moves that can be made in a single turn, per player type
    "max_moves_per_turn_human": None,
    "max_moves_per_turn_ai": 5,
}
