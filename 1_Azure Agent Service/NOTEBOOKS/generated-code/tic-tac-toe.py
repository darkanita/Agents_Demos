def print_board(board):
    """
    Print the current state of the tic tac toe board.
    
    Args:
        board (list): A 3x3 list representing the game board.
    """
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board, player):
    """
    Check if the given player has won the game.
    
    Args:
        board (list): The current game board.
        player (str): The player symbol, either 'X' or 'O'.
    
    Returns:
        bool: True if the player has won, False otherwise.
    """
    for i in range(3):
        # Check rows and columns
        if all([spot == player for spot in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True

    # Check diagonals
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False


def get_free_positions(board):
    """
    Get a list of free positions on the board.
    
    Args:
        board (list): The current game board.
    
    Returns:
        list: A list of tuples indicating free positions (row, col).
    """
    free_positions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                free_positions.append((i, j))
    return free_positions


def get_player_move(player, board):
    """
    Prompt the player for a move and validate the input.
    
    Args:
        player (str): The player symbol.
        board (list): The current game board.
    
    Returns:
        tuple: The valid (row, col) move chosen by the player.
    """
    free_positions = get_free_positions(board)
    while True:
        move_input = input(f"Player {player}, enter your move as 'row col' (0, 1, or 2): ").strip()
        if not move_input:
            print("Input cannot be empty. Please try again.")
            continue
        parts = move_input.split()
        if len(parts) != 2:
            print("Please enter exactly two numbers separated by space.")
            continue
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            print("Invalid input. Please enter numeric values only.")
            continue
        if (row, col) not in free_positions:
            print("This position is either taken or out of range. Please try again.")
            continue
        return row, col


def play_game():
    """
    Manage the flow of the tic tac toe game.
    """
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    print("Welcome to Tic Tac Toe!")
    print("Enter your move by typing the row and column numbers separated by a space (e.g., '0 2').")
    print("Rows and columns are indexed from 0 to 2.\n")

    while True:
        print_board(board)
        if not get_free_positions(board):
            print("It's a draw!")
            break

        try:
            row, col = get_player_move(current_player, board)
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting.")
            return

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        current_player = "O" if current_player == "X" else "X"


def main():
    """
    Main function to start and manage replay of the game.
    """
    while True:
        play_game()
        replay = input("Do you want to play again? (y/n): ").strip().lower()
        if replay not in ["y", "yes"]:
            print("Thanks for playing Tic Tac Toe. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
