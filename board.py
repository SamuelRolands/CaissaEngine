def initialize_board():
    """Creates the starting position of a chessboard as a dictionary."""
    board = {}

    for i, file in enumerate("abcdefgh", start=1):
        board[f"wP{i}"] = f"{file}2"
        board[f"bP{i}"] = f"{file}7"

    for i, file in enumerate(["a", "h"]):
        board[f"wR{i+1}"] = f"{file}1"
        board[f"bR{i+1}"] = f"{file}8"
    for i, file in enumerate(["b", "g"]):
        board[f"wN{i+1}"] = f"{file}1"
        board[f"bN{i+1}"] = f"{file}8"
    for i, file in enumerate(["c", "f"]):
        board[f"wB{i+1}"] = f"{file}1"
        board[f"bB{i+1}"] = f"{file}8"

    board["wQ"] = "d1"
    board["bQ"] = "d8"
    board["wK"] = "e1"
    board["bK"] = "e8"

    return board

if __name__ == "__main__":
    chess_board = initialize_board()
    print(chess_board)
