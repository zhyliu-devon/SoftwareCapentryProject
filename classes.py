import os
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

class Lazor:
    def __init__(self, position: Tuple[int, int], direction: Tuple[int, int]):
        """
        Initialize a Lazor for the game. During the propagation, each lazor will propogate
        
        Args:
            position : The (x, y) starting position of the Lazor.
            direction : The (vx, vy) direction of the Lazor.
            end : Whether to further propagate
        """
        self.position = position
        self.direction = direction
        self.end = False
    
    def __str__(self) -> str:
        return f"Lazor at Position: {self.position}, Direction: {self.direction}, End: {self.end}"


class Block:
    def __init__(self, block_type: str, position: Tuple[int, int]):
        """
        Initialize a block for the Lazor game.
        
        Args:
            block_type : The type of block ('A', 'B', 'C').
            position : The (x, y) position of the block.
        """
        self.block_type = block_type
        self.position = position

    def __str__(self) -> str:
        return f"Block Type: {self.block_type}, Position: {self.position}"

class LazorGame:
    def __init__(self, filename: str):
        """
        Initialize the Lazor board from a .bff file
        
        Args:
            filename (str): Path to the .bff file
        """
        self.filename = filename
        self.grid = []  # The game grid
        self.blocks = {}  # Dictionary to store block requirements
        self.block_objects = []  # List of block objects
        self.lazor_objects = []  # List of lazor objects when reading the document
        self.points = []  # List of points to intersect
        self.read_board()
    
    def read_board(self) -> None:
        """Read and parse the .bff file"""
        try:
            with open(self.filename, 'r') as f:
                lines = [line.strip() for line in f.readlines()]
                
            reading_grid = False # Change to true after reading the GRID START
            for line in lines:
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                    
                if line == 'GRID START':
                    reading_grid = True
                    continue
                elif line == 'GRID STOP':
                    reading_grid = False
                    continue
                    
                if reading_grid:
                    # Add grid row, splitting by spaces
                    self.grid.append(line.split()) #nested list
                else:
                    # Parse other elements when not readiong grid
                    parts = line.split()
                    if not parts:
                        continue
                        
                    if parts[0] in ['A', 'B', 'C']: #blocks
                        # Block specifications
                        self.blocks[parts[0]] = int(parts[1])
                    elif parts[0] == 'L': #lazers
                        # Lazor specification
                        lazor = Lazor(position=(int(parts[1]), int(parts[2])), direction=(int(parts[3]), int(parts[4])))
                        self.lazor_objects.append(lazor)
                    elif parts[0] == 'P':
                        # Point specification: x, y
                        self.points.append(tuple(map(int, parts[1:])))


        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find file: {self.filename}")
        except Exception as e:
            raise ValueError(f"Error parsing board file: {str(e)}")
    
    def initialize_blocks(self) -> None:
        """
        Creat block object and put it into the list
        """
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in ['A', 'B', 'C']:
                    block = Block(block_type=cell, position=(x, y))
                    self.block_objects.append(block)

    def visualize(self, address = None, file_name = None) -> None:
        """
        Visualize the Lazor board using matplotlib
        Args
            address : The adress to save the plot
            file_name : The file_name to save the plot
            if exist, then save
        """            
 
        fig, ax = plt.subplots(figsize=(10, 10))
        
        rows = len(self.grid)
        cols = len(self.grid[0])
        
        # Define colors
        block_styles = {
            'x': {'color': 'gray', 'label': 'No Block Allowed'},
            'o': {'color': 'white', 'label': 'Block Allowed'},
            'A': {'color': 'blue', 'label': 'Reflect Block'},
            'B': {'color': 'black', 'label': 'Opaque Block'},
            'C': {'color': 'yellow', 'label': 'Refract Block'}
        }
        
        # Create base grid
        legend_handles = []
        for i in range(rows):
            for j in range(cols):
                cell = self.grid[i][j]
                style = block_styles[cell]
                patch = plt.Rectangle((j, rows-1-i), 1, 1, 
                                   facecolor=style['color'],
                                   edgecolor='black')
                ax.add_patch(patch)
                
                # Add to legend if not already added
                if style['label'] not in [h.get_label() for h in legend_handles]:
                    legend_handles.append(plt.Rectangle((0,0), 1, 1, 
                                                     facecolor=style['color'],
                                                     edgecolor='black',
                                                     label=style['label']))

        # Add legend
        ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.title(f'Lazor Board: {os.path.basename(self.filename)}')

        if address is not None:
            print("Saving the solution for :" , file_name)
            plt.savefig(os.path.join(address, f"{file_name}_solution.png"))
            plt.close()
        else:
            plt.show()
