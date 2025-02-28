import board
import storage
from validate import validate_move

def print_board(board_dict):
    """Displays the board state in a readable format."""
    print("\nCurrent Board State:")
    for piece, position in sorted(board_dict.items()):
        print(f"{piece}: {position}")
    print("-" * 30)

def get_piece_at(square, board_dict):
    """Returns the piece (key) at a given square, or None if empty."""
    for p, pos in board_dict.items():
        if pos == square:
            return p
    return None

def move_piece(board_dict):
    """Handles user move input, including capturing and turn management."""
    turn = 'w'  # White starts
    while True:
        user_input = input(f"Turn {turn.upper()} - Enter move (e.g., wP1 e2 e4) or 'quit': ").strip()
        if user_input.lower() == "quit":
            print("Game exited.")
            break

        try:
            piece, start, end = user_input.split()
            
            # Enforce turn: piece must match current turn.
            if piece[0] != turn:
                print("Invalid move: It's not your turn.")
                continue

            # Check if the piece exists at the given start position.
            if piece not in board_dict or board_dict[piece] != start:
                print("Invalid move: Piece not found at given position.")
                continue

            # Validate the move according to piece-specific rules.
            if not validate_move(piece, start, end, board_dict):
                print("Invalid move: Does not follow chess rules.")
                continue

            # Check for capturing: Is the destination occupied?
            target_piece = get_piece_at(end, board_dict)
            if target_piece:
                # Prevent capturing your own piece.
                if target_piece[0] == piece[0]:
                    print("Invalid move: Cannot capture your own piece.")
                    continue
                else:
                    print(f"Capture! {piece} takes {target_piece}.")
                    # Remove the captured piece.
                    del board_dict[target_piece]

            # Move the piece.
            board_dict[piece] = end
            storage.save_move(piece, start, end)
            print_board(board_dict)

            # Switch turn.
            turn = 'b' if turn == 'w' else 'w'

        except ValueError:
            print("Incorrect format. Use: 'wP1 e2 e4'")

if __name__ == "__main__":
    chess_board = board.initialize_board()
    print_board(chess_board)
    move_piece(chess_board)
