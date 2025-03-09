has_moved = {
    'wK': False, 'bK': False,  # Kings
    'wR1': False, 'wR2': False,  # White rooks
    'bR1': False, 'bR2': False   # Black rooks
}

move_history = []  # Stores previous moves for undo functionality

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
        if square in board.values():  # checks if any piece occupies the square
            return False
        current_file += file_step
        current_rank += rank_step

    return True

def validate_move(piece, start, end, board):
    """
    Validates if the move is legal based on the piece type and chess rules.
    If valid, the move is recorded in move_history and the board is updated.
    """
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    file_diff = abs(ord(end_file) - ord(start_file))
    rank_diff = abs(end_rank - start_rank)
    piece_type = piece[1]  # 'P', 'N', 'B', etc.
    
    # For logging captured piece (if any)
    captured_piece = board.get(get_piece_at(end, board))
    
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

    elif piece_type == 'N':
        if (file_diff, rank_diff) in [(1, 2), (2, 1)]:
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    elif piece_type == 'B':
        if file_diff == rank_diff and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    elif piece_type == 'R':
        if (file_diff == 0 or rank_diff == 0) and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    elif piece_type == 'Q':
        if (file_diff == rank_diff or file_diff == 0 or rank_diff == 0) and is_path_clear(start, end, board):
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True

    elif piece_type == 'K':
        if max(file_diff, rank_diff) == 1:
            has_moved[piece] = True
            move_history.append((piece, start, end, board.get(end)))
            board[piece] = end
            return True
        
        # Castling Logic: King moves exactly 2 squares sideways
        if not has_moved.get(piece, True) and rank_diff == 0 and file_diff == 2:
            kingside = end_file > start_file  # True if castling kingside
            rook_pos = f"{'h' if kingside else 'a'}{start_rank}"
            rook_piece = f"{piece[0]}R{'2' if kingside else '1'}"
            if not has_moved.get(rook_piece, True) and is_path_clear(start, rook_pos, board):
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True

    return False

def get_piece_at(square, board):
    """
    Returns the piece key that is located at the given square,
    or None if the square is empty.
    """
    for p, pos in board.items():
        if pos == square:
            return p
    return None

def undo_move(board):
    """
    Reverts the last move made, restoring the board state.
    Returns True if a move was undone, False otherwise.
    """
    if move_history:
        last_move = move_history.pop()
        piece, start, end, captured_piece = last_move
        board[piece] = start
        if captured_piece:
            # To restore the captured piece, we need its key.
            # Here we assume captured_piece holds the key (if it was stored) or we can re-add it manually.
            board[captured_piece] = end
        return True
    return False

def can_attack(piece, target, board):
    """
    Returns True if the piece can attack the target square (according to its movement rules),
    without side effects (does not update board or move history).
    This function is used for check detection.
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
        # Pawn captures diagonally
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
    It finds the king's position and then checks if any opponent's piece can attack it.
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

if __name__ == "__main__":
    # Test board for move validation and check detection
    test_board = {
        'wP1': 'e2', 'bP1': 'e7',
        'wK': 'e1', 'bK': 'e8',
        'wQ': 'd1', 'bQ': 'd8',
        'wB1': 'c1', 'bB1': 'c8',
        'wR1': 'a1', 'bR1': 'a8'
    }
    
    # Basic move validation tests
    print(validate_move('wP1', 'e2', 'e4', test_board))  # True
    print(validate_move('wQ', 'd1', 'h5', test_board))  # False (blocked by pawn at e2)
    print(validate_move('wR1', 'a1', 'a4', test_board))  # True
    print(validate_move('wB1', 'c1', 'f4', test_board))  # False (path blocked by pawn at d2 if any)
    print(validate_move('wK', 'e1', 'e3', test_board))  # False (king can't move 2 squares normally)
    
    # Test check detection:
    # Place an opponent rook in a position to check the white king.
    test_board['bR1'] = 'e8'  # Black rook remains at e8 (for example)
    # Now, manually position the black rook so it can attack white king at e1.
    test_board['bR1'] = 'e2'  # Suppose black rook moves to e2, attacking white king at e1.
    print(is_in_check(test_board, 'w'))  # Expected: True, because bR1 on e2 attacks white king on e1.
    
    # Undo a move test
    print(undo_move(test_board))  # Should undo last move.
    print(test_board)
