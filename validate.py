has_moved = {
    'wK': False, 'bK': False,  # Kings
    'wR1': False, 'wR2': False,  # White rooks
    'bR1': False, 'bR2': False   # Black rooks
}

def is_path_clear(start, end, board):
    """
    Checks that all squares between start and end (exclusive) are empty.
    Works for linear (vertical, horizontal, or diagonal) moves.
    """
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    
    file_step = 0
    rank_step = 0
    if end_file > start_file:
        file_step = 1
    elif end_file < start_file:
        file_step = -1
    if end_rank > start_rank:
        rank_step = 1
    elif end_rank < start_rank:
        rank_step = -1
    
    current_file = ord(start_file) + file_step
    current_rank = start_rank + rank_step
    
    while (current_file != ord(end_file)) and (current_rank != end_rank):
        square = f"{chr(current_file)}{current_rank}"
        if any(pos == square for pos in board.values()):
            return False
        current_file += file_step
        current_rank += rank_step
    return True


def validate_move(piece, start, end, board):
    """Validates if the move is legal based on the piece type and chess rules."""
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    file_diff = abs(ord(end_file) - ord(start_file))
    rank_diff = abs(end_rank - start_rank)
    piece_type = piece[1]  # 'P', 'N', 'B', etc.
    
    if piece_type == 'P':
        direction = 1 if piece[0] == 'w' else -1

        if start_file == end_file:

            if (end_rank - start_rank) == direction:
                if end in board.values():
                    return False
                return True

            if (end_rank - start_rank) == 2 * direction and (start_rank == 2 or start_rank == 7):
                intermediate_rank = start_rank + direction
                intermediate_square = f"{start_file}{intermediate_rank}"
                if intermediate_square in board.values() or end in board.values():
                    return False
                return True

        elif file_diff == 1 and (end_rank - start_rank) == direction:

            if end in board.values():
                return True

    elif piece_type == 'N':
        if (file_diff, rank_diff) in [(1, 2), (2, 1)]:
            return True

    elif piece_type == 'B':
        if file_diff == rank_diff:
            return is_path_clear(start, end, board)

    elif piece_type == 'R':
        if file_diff == 0 or rank_diff == 0:
            return is_path_clear(start, end, board)

    elif piece_type == 'Q':
        if file_diff == rank_diff or file_diff == 0 or rank_diff == 0:
            return is_path_clear(start, end, board)

    elif piece_type == 'K':
        # Regular one-square move
        if max(file_diff, rank_diff) == 1:
            has_moved[piece] = True
            return True
    
        # Castling Logic: King moves exactly 2 squares sideways
        if not has_moved[piece] and rank_diff == 0 and file_diff == 2:
            kingside = end_file > start_file  # True if castling kingside
            rook_pos = f"{'h' if kingside else 'a'}{start_rank}"
            rook_piece = f"{piece[0]}R{'2' if kingside else '1'}"

            # Check if the rook is unmoved and the path is clear
            if not has_moved.get(rook_piece, True):
                if is_path_clear(start, rook_pos, board):
                    return True

        return False


    return False

if __name__ == "__main__":
    test_board = {
        'wP1': 'e2', 'bP1': 'e7',  # Sample pieces
        'wK': 'e1', 'bK': 'e8',
        'wQ': 'd1', 'bQ': 'd8'
    }

    print(validate_move('wP1', 'e2', 'e4', test_board))  # Should be True (pawn move)
    print(validate_move('wP1', 'e2', 'e5', test_board))  # Should be False (pawn too far)
    print(validate_move('wQ', 'd1', 'h5', test_board))  # Should be True (queen move)
    print(validate_move('bK', 'e8', 'e6', test_board))  # Should be False (king too far)
    print(is_path_clear('d1', 'h5', test_board))  # Expecting True if path is clear


