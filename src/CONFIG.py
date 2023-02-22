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
    "table_top_mode": False,
}
