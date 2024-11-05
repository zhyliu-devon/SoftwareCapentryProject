# For a single file
from functions import *
from classes import *
import time
from typing import Dict

def solve_boards(directory_path):
    # Get all .bff files in the directory
    bff_files = [file for file in os.listdir(directory_path) if file.endswith('.bff')]
    solution_times = {}
    
    print("Number of files in the directory:", len(bff_files))
    print("========")
    
    for file_name in bff_files:
        file_path = os.path.join(directory_path, file_name)
        print("Attempting to solve", file_name)
        
        try:
            start_time = time.time()
            
            # Create and attempt to solve the board
            board = LazorGame(file_path)
            if solve_board_optimized(board):
                elapsed_time = time.time() - start_time
                solution_times[file_name] = elapsed_time
                print("Solved in", elapsed_time, "seconds")
                
                board.propagate()
                board.visualize(directory_path, file_name)
            else:
                print("No solution found for", file_name)
                solution_times[file_name] = -1
                
        except Exception as error:
            print("Error while processing", file_name, ":", str(error))
            solution_times[file_name] = -2
            
        print("========")
    
    # Print summary of results
    print("Summary of results:")
    for file_name, solve_time in solution_times.items():
        if solve_time > 0:
            print(file_name, "solved in", solve_time, "seconds")
        elif solve_time == -1:
            print(file_name, "no solution found")
        else:
            print(file_name, "error during processing")
            
    return solution_times


directory = r".\bff_files"
solve_boards(directory)

