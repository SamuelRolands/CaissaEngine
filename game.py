import board
import storage
import legend
from validate import validate_move, undo_move, is_in_check, is_checkmate

def print_board(board_dict):
    """Displays the chess board as an 8x8 grid with piece symbols and coordinate labels."""
    piece_symbols = {
        'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
        'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟'
    }
    files = "abcdefgh"
    
    print("\nCurrent Board State:")
    for rank in range(8, 0, -1):
        row_str = f"{rank} "
        for file in files:
            square = f"{file}{rank}"
            piece_here = None
            for key, pos in board_dict.items():
                if pos == square:
                    piece_here = key
                    break
            if piece_here:
                symbol = piece_symbols.get(piece_here[:2], piece_here[:2])
            else:
                symbol = '.'
            row_str += symbol + " "
        print(row_str)
    print("  " + " ".join(files))
    print("-" * 30)

def get_piece_at(square, board_dict):
    """Returns the piece key at a given square, or None if empty."""
    for p, pos in board_dict.items():
        if pos == square:
            return p
    return None

def move_piece(board_dict):
    """Handles user move input, including capturing, turn management, and pawn promotion."""
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

            # **Pawn Promotion Logic**
            if piece[1] == 'P':  # Only applies to pawns
                rank = int(end[1])
                if (piece[0] == 'w' and rank == 8) or (piece[0] == 'b' and rank == 1):
                    print("Pawn promotion! Choose a piece (Q, R, B, N):")
                    while True:
                        promotion_choice = input().strip().upper()
                        if promotion_choice in ['Q', 'R', 'B', 'N']:
                            new_piece = piece[0] + promotion_choice  # e.g., 'wQ' for white queen
                            del board_dict[piece]  # Remove pawn
                            board_dict[new_piece] = end  # Replace with new piece
                            print(f"Pawn promoted to {new_piece}!")
                            break
                        else:
                            print("Invalid choice. Enter Q, R, B, or N.")

            storage.save_move(piece, start, end)
            print_board(board_dict)

            # Switch turn.
            turn = 'b' if turn == 'w' else 'w'

        except ValueError:
            print("Incorrect format. Use: 'wP1 e2 e4'")

if __name__ == "__main__":
    legend.print_legend()
    chess_board = board.initialize_board()
    print_board(chess_board)
    move_piece(chess_board)
