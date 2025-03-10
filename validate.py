import copy

# --- Globals ---
has_moved = {
    'wK': False, 'bK': False,  # Kings
    'wR1': False, 'wR2': False,  # White rooks
    'bR1': False, 'bR2': False   # Black rooks
}

move_history = []  # Stores previous moves for undo functionality

# --- Helper Functions ---

def is_path_clear(start, end, board):
    """
    Checks that all squares between start and end (exclusive) are empty.
    Works for linear (vertical, horizontal, or diagonal) moves.
    """
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    
    file_step = 1 if end_file > start_file else -1 if end_file < start_file else 0
    rank_step = 1 if end_rank > start_rank else -1 if end_rank < start_rank else 0

    current_file = ord(start_file) + file_step
    current_rank = start_rank + rank_step

    while (current_file != ord(end_file) or current_rank != end_rank):
        square = f"{chr(current_file)}{current_rank}"
        if square in board.values():
            return False
        current_file += file_step
        current_rank += rank_step

    return True

def get_piece_at(square, board):
    """
    Returns the piece key at the given square, or None if empty.
    """
    for p, pos in board.items():
        if pos == square:
            return p
    return None

# --- Move Validation (Destructive) ---

def validate_move(piece, start, end, board):
    """
    Validates if the move is legal based on piece-specific rules.
    If valid, updates the board and logs the move in move_history.
    """
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    file_diff = abs(ord(end_file) - ord(start_file))
    rank_diff = abs(end_rank - start_rank)
    piece_type = piece[1]  # 'P', 'N', 'B', etc.
    
    # Pawn moves
    if piece_type == 'P':
        direction = 1 if piece[0] == 'w' else -1
        if start_file == end_file:
            if (end_rank - start_rank) == direction and end not in board.values():
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True
            if (end_rank - start_rank) == 2 * direction and (start_rank == (2 if piece[0]=='w' else 7)):
                intermediate_rank = start_rank + direction
                intermediate_square = f"{start_file}{intermediate_rank}"
                if intermediate_square in board.values() or end in board.values():
                    return False
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True
        elif file_diff == 1 and (end_rank - start_rank) == direction:
            if end in board.values():
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True
    
    # Knight moves
    elif piece_type == 'N':
        if (file_diff, rank_diff) in [(1, 2), (2, 1)]:
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    # Bishop moves
    elif piece_type == 'B':
        if file_diff == rank_diff and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    # Rook moves
    elif piece_type == 'R':
        if (file_diff == 0 or rank_diff == 0) and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    # Queen moves
    elif piece_type == 'Q':
        if (file_diff == rank_diff or file_diff == 0 or rank_diff == 0) and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    # King moves (normal and castling)
    elif piece_type == 'K':
        if max(file_diff, rank_diff) == 1:
            has_moved[piece] = True
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True
        if not has_moved.get(piece, True) and rank_diff == 0 and file_diff == 2:
            kingside = end_file > start_file
            rook_pos = f"{'h' if kingside else 'a'}{start_rank}"
            rook_piece = f"{piece[0]}R{'2' if kingside else '1'}"
            if not has_moved.get(rook_piece, True) and is_path_clear(start, rook_pos, board):
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True

    return False

def undo_move(board):
    """
    Reverts the last move and restores the board state.
    Returns True if a move was undone, else False.
    """
    if move_history:
        piece, start, end, captured_piece = move_history.pop()
        board[piece] = start
        if captured_piece:
            board[captured_piece] = end
        return True
    return False

# --- Non-Destructive Simulation for Check Detection ---
def simulate_validate_move(piece, start, end, board):
    """
    Simulates a move on a copy of the board.
    Returns True if the move is legal; otherwise, False.
    This function does not update the actual board or move history.
    """
    board_copy = copy.deepcopy(board)
    return validate_move(piece, start, end, board_copy)

# --- Check & Checkmate Detection ---

def can_attack(piece, target, board):
    """
    Returns True if the given piece can attack the target square, using its movement rules.
    This is used for check detection.
    """
    start = board[piece]
    start_file, start_rank = start[0], int(start[1])
    target_file, target_rank = target[0], int(target[1])
    file_diff = abs(ord(target_file) - ord(start_file))
    rank_diff = abs(target_rank - start_rank)
    piece_type = piece[1]
    color = piece[0]
    
    if piece_type == 'P':
        direction = 1 if color == 'w' else -1
        return file_diff == 1 and (target_rank - start_rank) == direction
    elif piece_type == 'N':
        return (file_diff, rank_diff) in [(1, 2), (2, 1)]
    elif piece_type == 'B':
        return file_diff == rank_diff and is_path_clear(start, target, board)
    elif piece_type == 'R':
        return (file_diff == 0 or rank_diff == 0) and is_path_clear(start, target, board)
    elif piece_type == 'Q':
        return (file_diff == rank_diff or file_diff == 0 or rank_diff == 0) and is_path_clear(start, target, board)
    elif piece_type == 'K':
        return max(file_diff, rank_diff) == 1
    return False

def is_in_check(board, color):
    """
    Returns True if the king of the given color ('w' or 'b') is in check.
    """
    king = f"{color}K"
    if king not in board:
        return False
    king_pos = board[king]
    for piece, pos in board.items():
        if piece[0] != color:  # opponent's piece
            if can_attack(piece, king_pos, board):
                return True
    return False

def is_checkmate(board, color):
    """
    Returns True if the king of the given color is in checkmate,
    i.e., in check and with no legal moves to escape.
    """
    if not is_in_check(board, color):
        return False
    from string import ascii_lowercase
    possible_files = ascii_lowercase[:8]  # 'a' through 'h'
    possible_ranks = '12345678'
    for piece, pos in board.items():
        if piece[0] == color:
            for f in possible_files:
                for r in possible_ranks:
                    target = f"{f}{r}"
                    board_copy = copy.deepcopy(board)
                    if board_copy.get(piece) != pos:
                        continue
                    if simulate_validate_move(piece, pos, target, board_copy):
                        if not is_in_check(board_copy, color):
                            return False
    return True

# --- Testing Code ---
if __name__ == "__main__":
    test_board = {
        'wP1': 'e2', 'bP1': 'e7',
        'wK': 'e1', 'bK': 'e8',
        'wQ': 'd1', 'bQ': 'd8',
        'wB1': 'c1', 'bB1': 'c8',
        'wR1': 'a1', 'bR1': 'a8'
    }
    
    print("Move Validation Tests:")
    print(validate_move('wP1', 'e2', 'e4', test_board))  # Expected True
    print(validate_move('wQ', 'd1', 'h5', test_board))  # Expected False (blocked by pawn at e2)
    print(validate_move('wR1', 'a1', 'a4', test_board))  # Expected True
    print(validate_move('wB1', 'c1', 'f4', test_board))  # Expected False (if blocked)
    print(validate_move('wK', 'e1', 'e3', test_board))  # Expected False
    
    print("\nCheck Detection Test:")
    # Position black rook to check white king:
    test_board['bR1'] = 'e2'
    print("Is white in check? ", is_in_check(test_board, 'w'))  # Expected True
    
    print("\nCheckmate Detection Test:")
    # Minimal checkmate scenario (example):\n    # White king trapped at h1, black queen and king close by.\n    # Note: This is a very simplified position.\n    checkmate_board = {\n        'wK': 'h1',\n        'bK': 'f3',\n        'bQ': 'g3'\n    }\n    print(\"Is white checkmated?\", is_checkmate(checkmate_board, 'w'))\n", end="")
    from string import ascii_lowercase
    checkmate_board = {
        'wK': 'h1',
        'bK': 'f3',
        'bQ': 'g3'
    }
    print("Is white checkmated?", is_checkmate(checkmate_board, 'w'))
    
    print("\nUndo Move Test:")
    print("Undoing last move...")
    if undo_move(test_board):
        print("Move undone.")
    print("Board state after undo:", test_board)
