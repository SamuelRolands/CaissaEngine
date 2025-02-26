def validate_move(piece, start, end, board):
    """Validates if the move is legal based on the piece type and chess rules."""
    
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    file_diff = abs(ord(end_file) - ord(start_file))
    rank_diff = abs(end_rank - start_rank)

    piece_type = piece[1]
    
    if piece_type == 'P':
        direction = 1 if piece[0] == 'w' else -1
        if start_file == end_file:
            if (end_rank - start_rank) == direction:
                return True
            if (end_rank - start_rank) == 2 * direction and (start_rank == 2 or start_rank == 7):
                return True
        elif file_diff == 1 and (end_rank - start_rank) == direction:
            return True

    elif piece_type == 'N':
        if (file_diff, rank_diff) in [(1, 2), (2, 1)]:
            return True

    elif piece_type == 'B':
        if file_diff == rank_diff:
            return True

    elif piece_type == 'R':
        if file_diff == 0 or rank_diff == 0:
            return True

    elif piece_type == 'Q':
        if file_diff == rank_diff or file_diff == 0 or rank_diff == 0:
            return True

    elif piece_type == 'K':
        if max(file_diff, rank_diff) == 1:
            return True

    return False
