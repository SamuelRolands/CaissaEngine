import pandas as pd

def save_move(piece, start, end, filename="data/board.xlsx"):
    """Logs a move into an Excel sheet."""
    df = pd.DataFrame([[piece, start, end]], columns=["Piece", "Start", "End"])
    
    try:
        existing = pd.read_excel(filename)
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_excel(filename, index=False)
