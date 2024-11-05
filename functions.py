from classes import *
import os
import math
import itertools

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

def solve_board(game: LazorGame) -> bool:
    """
    Solve the Lazor game by trying different block configurations.
    Shows progress with a progress bar.
    
    Args:
        game (LazorGame): The game to solve
        
    Returns:
        bool: True if a solution was found, False otherwise
    """
    # 1 Get all possible positions for blocks   
    available_positions = []
    for y in range(len(game.grid)):
        for x in range(len(game.grid[0])):
            if game.grid[y][x] == 'o':
                available_positions.append((x, y))
    
    # 2 For each block type, get the number of blocks needed
    blocks_needed = []
    for block_type, count in game.blocks.items():
        blocks_needed.extend([block_type] * count)

    # If no blocks needed, check if current configuration works
    if not blocks_needed:
        game.propogate()
        return game.validate()
    
    # 3 Get all possible combinations of positions for the blocks
    num_positions_needed = len(blocks_needed)
    if num_positions_needed > len(available_positions):
        return False
    # 4 Calculate total number of combinations to try
    n_c = math.comb(len(available_positions), num_positions_needed)
    n_p = math.factorial(num_positions_needed)
    total_it = n_c * n_p
    
    print(f"In total {total_it:,} possibilities")
    
    # 5 Try each permutation of block types in these positions
    for positions in itertools.combinations(available_positions, num_positions_needed):
        for block_arrangement in itertools.permutations(blocks_needed):

            # 6 Create a copy of the game to test this configuration
            test_game = LazorGame(game.filename)

            # 7 Place blocks according to this arrangement
            valid = True
            for (x, y), block_type in zip(positions, block_arrangement):
                if not test_game.add_block(block_type, (x, y)):
                    valid = False
                    break
    # 8 check if this is a solution
            test_game.propogate()
            if test_game.validate():
    # 9 If solution found, apply it to the original game
                for (x, y), block_type in zip(positions, block_arrangement):
                    game.add_block(block_type, (x, y))
                return True
    return False