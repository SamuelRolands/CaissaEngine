import board
import storage
import legend
from validate import validate_move


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
    """Returns the piece (key) at a given square, or None if empty."""
    for p, pos in board_dict.items():
        if pos == square:
            return p
    return None

def is_stalemate(turn, board_dict):
    """Checks if the current player has no legal moves but is not in check."""
    for piece, position in board_dict.items():
        if piece[0] == turn:  # Check only the current player's pieces
            for rank in range(1, 9):
                for file in "abcdefgh":
                    destination = f"{file}{rank}"
                    if validate_move(piece, position, destination, board_dict):
                        return False  # At least one legal move exists
    return True  # No legal moves available

def move_piece(board_dict):
    """Handles user move input, including capturing, turn management, and en passant."""
    turn = 'w'
    en_passant_target = None  # Tracks possible en passant capture square
    
    while True:
        user_input = input(f"Turn {turn.upper()} - Enter move (e.g., wP1 e2 e4) or 'quit': ").strip()
        if user_input.lower() == "quit":
            print("Game exited.")
            break

        try:
            piece, start, end = user_input.split()

            if piece[0] != turn:
                print("Invalid move: It's not your turn.")
                continue

            if piece not in board_dict or board_dict[piece] != start:
                print("Invalid move: Piece not found at given position.")
                continue

            if not validate_move(piece, start, end, board_dict):
                print("Invalid move: Does not follow chess rules.")
                continue

            target_piece = get_piece_at(end, board_dict)
            if target_piece:
                if target_piece[0] == piece[0]:
                    print("Invalid move: Cannot capture your own piece.")
                    continue
                else:
                    print(f"Capture! {piece} takes {target_piece}.")
                    del board_dict[target_piece]
            
            # En passant logic
            if piece[1] == 'P':  # If the piece is a pawn
                start_file, start_rank = start[0], int(start[1])
                end_file, end_rank = end[0], int(end[1])
                
                if abs(end_rank - start_rank) == 2:
                    en_passant_target = (end_file, (start_rank + end_rank) // 2)
                else:
                    if en_passant_target and end == f"{en_passant_target[0]}{en_passant_target[1]}":
                        captured_pawn = get_piece_at(f"{en_passant_target[0]}{start_rank}", board_dict)
                        if captured_pawn and captured_pawn[0] != piece[0] and captured_pawn[1] == 'P':
                            print(f"En passant! {piece} captures {captured_pawn}.")
                            del board_dict[captured_pawn]

            board_dict[piece] = end
            storage.save_move(piece, start, end)
            print_board(board_dict)
            
            # Check for stalemate
            if is_stalemate('b' if turn == 'w' else 'w', board_dict):
                print("Game over: Stalemate! It's a draw.")
                break
            
            turn = 'b' if turn == 'w' else 'w'
            
        except ValueError:
            print("Incorrect format. Use: 'wP1 e2 e4'")

if __name__ == "__main__":
    legend.print_legend()
    chess_board = board.initialize_board()
    print_board(chess_board)
    move_piece(chess_board)
