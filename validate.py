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
    
    while (current_file != ord(end_file)) or (current_rank != end_rank):
        square = f"{chr(current_file)}{current_rank}"
        if square in board.values():
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
        if max(file_diff, rank_diff) == 1:
            return True

    return False
