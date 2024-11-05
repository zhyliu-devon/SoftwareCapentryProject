from classes import *
import os

def read_and_visualize_board(filename: str) -> LazorGame:
    """
    Function to read and visualize a board file
    
    Args
        filename : Path to the .bff file
        
    Returns:
        LazorBoard: The  board object
    """
    board = LazorGame(filename)
    print(f"Board for {os.path.basename(filename)}:")
    print(board)
    board.visualize()
    return board
