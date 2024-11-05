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


def solve_board_optimized(game: LazorGame) -> bool:
    """
    Solve the Lazor game recursively.

    Args:
        LazorGame: The game to solve
        
    Returns:
        bool: True if a solution was found, False otherwise
    """
    # Get all possible positions for blocks
    available_positions = []
    for y in range(len(game.grid)):
        for x in range(len(game.grid[0])):
            if game.grid[y][x] == 'o':
                available_positions.append((x, y))
    
    # For each block type, get the number of blocks needed
    blocks_needed = []
    for block_type, count in game.blocks.items():
        blocks_needed.extend([block_type] * count)
    
    if not blocks_needed:
        # If no blocks needed, check if current configuration works
        game.propogate()
        return game.validate()
    
    # Get all possible combinations of positions for the blocks
    num_positions_needed = len(blocks_needed)
    if num_positions_needed > len(available_positions):
        return False
    
    def check_block_effect(test_game: LazorGame, pos: tuple, block_type: str, 
                          current_blocks: list) -> bool:
        """
        Check if placing a block actually changes the laser path.
        
        Args:
            test_game: Current game state
            pos: Position to place block
            block_type: Type of block to place
            current_blocks: List of currently placed blocks
        
        Returns:
            True if block placement changes path, False otherwise
        """
        # First propagate with current blocks
        for placed_pos, placed_type in current_blocks:
            test_game.add_block(placed_type, placed_pos)
        test_game.propogate()
        original_path = test_game.path.copy()
        
        # Reset and add new block
        test_game.reset()
        for placed_pos, placed_type in current_blocks:
            test_game.add_block(placed_type, placed_pos)
        test_game.add_block(block_type, pos)
        test_game.propogate()
        new_path = test_game.path
        
        # Check if path changed
        return original_path != new_path
    
    def solve_recursive(positions_left, blocks_left, placed_blocks=None):
        """
        Recursive function 
        
        Args:
            positions_left : Available positions remaining
            blocks_left : Blocks still to be placed
            placed_blocks : Blocks already placed [(pos, type), ...]
        
        Returns:
            bool: True if solution found, False otherwise
        """
        if placed_blocks is None:
            placed_blocks = []
            
        # Base case: if we've placed all blocks, check if it's a solution
        if not blocks_left:
            test_game = LazorGame(game.filename)
            for pos, block_type in placed_blocks:
                test_game.add_block(block_type, pos)
            test_game.propogate()
            if test_game.validate():
                # Apply solution to original game
                for pos, block_type in placed_blocks:
                    game.add_block(block_type, pos)
                return True
            return False
        
        # Try each position for the next block
        
        for i, pos in enumerate(positions_left):
            for block_type in set(blocks_left):  # Only try each block type once per position          
                # Check if this block placement actually affects the path
                test_game = LazorGame(game.filename)
                if not check_block_effect(test_game, pos, block_type, placed_blocks):
                    if not test_game.validate():
                        # Skip this placement if it doesn't change the path and it is not the solution
                        continue

                # Remove the block type we're using
                new_blocks = list(blocks_left)
                new_blocks.remove(block_type)
                
                # Remove the position we're using
                new_positions = positions_left[:i] + positions_left[i+1:]
                
                # Try this configuration
                if solve_recursive(new_positions, new_blocks, 
                                placed_blocks + [(pos, block_type)]):
                    return True
        return False
    

    result = solve_recursive(available_positions, blocks_needed)
 
    return result


        
            