import board
import storage
from validate import validate_move

def print_board(board_dict):
    """Displays the board state in a readable format."""
    print("\nCurrent Board State:")
    for piece, position in sorted(board_dict.items()):
        print(f"{piece}: {position}")
    print("-" * 30)

def move_piece(board_dict):
    """Handles user move input and updates the board."""
    while True:
        user_input = input("Enter move (e.g., wP1 e2 e4) or 'quit': ").strip()

        if user_input.lower() == "quit":
            print("Game exited.")
            break
        try:
            piece, start, end = user_input.split()
            
            if piece not in board_dict or board_dict[piece] != start:
                print("Invalid move: Piece not found at given position.")
                continue

            if not validate_move(piece, start, end, board_dict):
                print("Invalid move: Does not follow chess rules.")
                continue

            board_dict[piece] = end
            storage.save_move(piece, start, end)

            print_board(board_dict)

        except ValueError:
            print("Incorrect format. Use: 'wP1 e2 e4'")
if __name__ == "__main__":
    chess_board = board.initialize_board()
    print_board(chess_board)
    move_piece(chess_board)
