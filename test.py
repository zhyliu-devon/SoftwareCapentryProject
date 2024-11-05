# For a single file
from functions import *
from classes import *

def solve_all_boards_optimized(directory_path: str) -> Dict[str, float]:
    """
    Solve all .bff files in the specified directory.
    
    Args:
        directory_path (str): Path to directory containing .bff files
        
    Returns:
        Dict[str, float]: Dictionary mapping file names to solution times
    """
    # Get all .bff files in directory
    bff_files = [f for f in os.listdir(directory_path) if f.endswith('.bff')]
    solution_times = {}
    
    print(f"\nFound {len(bff_files)} .bff files to solve.\n")
    print("=" * 50)
    
    # Process each file
    for file_name in bff_files:
        full_path = os.path.join(directory_path, file_name)
        print(f"\nAttempting to solve: {file_name}")
        
        try:
            # Time the solution
            start_time = time.time()
            
            # Create and solve the board
            board = LazorGame(full_path)
            if solve_board_optimized(board):
                solution_time = time.time() - start_time
                solution_times[file_name] = solution_time
                
                print(f"\nSolution found in {solution_time:.2f} seconds!")
                #print_solution(board)
                board.propogate()
                board.visualize(directory_path, file_name)
                
     
            else:
                print(f"\nNo solution found for {file_name}")
                solution_times[file_name] = -1
                
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
            solution_times[file_name] = -2
            
        print("\n" + "=" * 50)
    
    # Print summary
    print("\nSummary of results:")
    print("=" * 50)
    for file_name, solve_time in solution_times.items():
        if solve_time > 0:
            print(f"{file_name}: Solved in {solve_time:.2f} seconds")
        elif solve_time == -1:
            print(f"{file_name}: No solution found")
        else:
            print(f"{file_name}: Error during processing")
            
    return solution_times

directory = r".\bff_files"
solve_all_boards_optimized(directory)

