def print_legend():
    """Prints a legend mapping the naming scheme to Unicode chess symbols."""
    piece_symbols = {
        'wK': '♔  White King',
        'wQ': '♕  White Queen',
        'wR': '♖  White Rook',
        'wB': '♗  White Bishop',
        'wN': '♘  White Knight',
        'wP': '♙  White Pawn',
        'bK': '♚  Black King',
        'bQ': '♛  Black Queen',
        'bR': '♜  Black Rook',
        'bB': '♝  Black Bishop',
        'bN': '♞  Black Knight',
        'bP': '♟  Black Pawn'
    }
    print("=== Legend ===")
    for key, value in piece_symbols.items():
        print(f"{key}: {value}")
    print("-" * 30)
