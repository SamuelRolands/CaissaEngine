import board
import storage
import legend
from validate import validate_move, undo_move, is_in_check

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
                # Get symbol using the first two characters (e.g., 'wP')
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
    """
    Handles user move input including:
      - Executing moves
      - Checking if the move leaves the king in check (illegal)
      - Undoing the move if needed
      - Allowing 'undo' and 'quit' commands
    """
    turn = 'w'  # White starts
    while True:
        user_input = input(f"Turn {turn.upper()} - Enter move (e.g., wP1 e2 e4), 'undo', or 'quit': ").strip()
        
        if user_input.lower() == "quit":
            print("Game exited.")
            break
        
        if user_input.lower() == "undo":
            if undo_move(board_dict):
                print("Last move undone.")
                print_board(board_dict)
            else:
                print("No moves to undo.")
            continue
        
        try:
            piece, start, end = user_input.split()
            
            # Enforce turn: ensure the piece belongs to the current player.
            if piece[0] != turn:
                print("Invalid move: It's not your turn.")
                continue
            
            # Check if the piece exists at the start square.
            if piece not in board_dict or board_dict[piece] != start:
                print("Invalid move: Piece not found at the given position.")
                continue
            
            # Validate and execute the move.
            if not validate_move(piece, start, end, board_dict):
                print("Invalid move: Does not follow chess rules.")
                continue
            
            # Save move to storage.
            storage.save_move(piece, start, end)
            
            # **Check:** If the move leaves the player's king in check, it's illegal.
            if is_in_check(board_dict, turn):
                print("Illegal move: Your king is in check!")
                # Undo the move.
                undo_move(board_dict)
                continue
            
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
