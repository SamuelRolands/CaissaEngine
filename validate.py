has_moved = {
    'wK': False, 'bK': False,  # Kings
    'wR1': False, 'wR2': False,  # White rooks
    'bR1': False, 'bR2': False   # Black rooks
}

move_history = []  # Stores previous moves for undo functionality

def is_path_clear(start, end, board):
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

def validate_move(piece, start, end, board):
    start_file, start_rank = start[0], int(start[1])
    end_file, end_rank = end[0], int(end[1])
    file_diff = abs(ord(end_file) - ord(start_file))
    rank_diff = abs(end_rank - start_rank)
    piece_type = piece[1]  # 'P', 'N', 'B', etc.
    
    if piece_type == 'P':
        direction = 1 if piece[0] == 'w' else -1

        if start_file == end_file:
            if (end_rank - start_rank) == direction and end not in board.values():
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True
            if (end_rank - start_rank) == 2 * direction and (start_rank == 2 or start_rank == 7):
                intermediate_rank = start_rank + direction
                intermediate_square = f"{start_file}{intermediate_rank}"
                if any(pos == intermediate_square for pos in board.values()) or end in board.values():
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
        if file_diff == 0 or rank_diff == 0:
            if is_path_clear(start, end, board):
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True

    elif piece_type == 'Q':
        if file_diff == rank_diff or file_diff == 0 or rank_diff == 0:
            if is_path_clear(start, end, board):
                move_history.append((piece, start, end, board.get(end)))
                board[piece] = end
                return True

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
    if move_history:
        last_move = move_history.pop()
        piece, start, end, captured_piece = last_move
        board[piece] = start
        if captured_piece:
            board[captured_piece] = end  # Restore captured piece
        return True
    return False

if __name__ == "__main__":
    test_board = {
        'wP1': 'e2', 'bP1': 'e7',
        'wK': 'e1', 'bK': 'e8',
        'wQ': 'd1', 'bQ': 'd8',
        'wB1': 'c1', 'bB1': 'c8',
        'wR1': 'a1', 'bR1': 'a8'
    }

    print(validate_move('wP1', 'e2', 'e4', test_board))  # True
    print(validate_move('wQ', 'd1', 'h5', test_board))  # False (blocked)
    print(validate_move('wR1', 'a1', 'a4', test_board))  # True
    print(undo_move(test_board))  # True (undoes last move)
    print(test_board)  # Check board state after undo
