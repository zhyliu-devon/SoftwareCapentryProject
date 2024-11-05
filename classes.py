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
        self.path = [] # list of path travelled by lazor
        self.created_lazors = []
        self.lazors = []
        self.read_board()
        self.initialize_lazors()
        self.initialize_blocks()
    
    def reset(self):
        self.grid = []  # The game grid
        self.blocks = {}  # Dictionary to store block requirements
        self.block_objects = []  # List of block objects
        self.lazor_objects = []  # List of lazor objects
        self.points = []  # List of points to intersect
        self.path = [] # list of path travelled by lazor
        self.created_lazors = []
        self.lazors = []
        self.read_board()
        self.initialize_lazors()
        self.initialize_blocks()

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

    def initialize_lazors(self) -> None:
        """
        Initialize the list of all lazors in the game.
        """
        for lazor in self.lazor_objects:
            self.lazors.append(Lazor(lazor.position, lazor.direction))

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
                patch = plt.Rectangle((j, rows-1-i), 1, 1, facecolor=style['color'],edgecolor='black')
                ax.add_patch(patch)
                
                # Add to legend if not already added
                if style['label'] not in [h.get_label() for h in legend_handles]:
                    legend_handles.append(plt.Rectangle((0,0), 1, 1, facecolor=style['color'],edgecolor='black',label=style['label']))
        
        # Plot points to intersect
        for x, y in self.points:
            point = ax.plot(x/2, rows-y/2, 'ro', markersize=10)[0]
            if 'Target Points' not in [h.get_label() for h in legend_handles]:
                legend_handles.append(point)
                point.set_label('Target Points')
         # Plot initial lazor positions and directions
        for lazor in self.lazor_objects:
            x, y = lazor.position
            vx, vy = lazor.direction
            ax.plot(x / 2, rows - y / 2, 'go', markersize=10, label='Lazor Start')
            ax.arrow(x / 2, rows - y / 2, vx / 4, -vy / 4, head_width=0.1, head_length=0.1, fc='g', ec='g')
        
        # Plot laser paths based on path
        for segment in self.path:
            (x1, y1), (x2, y2) = segment
            ax.plot([x1 / 2, x2 / 2], [rows - y1 / 2, rows - y2 / 2], 'r-', linewidth=2)

        ax.set_xticks(range(cols + 1))
        ax.set_yticks(range(rows + 1))
        ax.grid(True)
        ax.set_aspect('equal')
        # Add legend
        ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.title(f'Lazor Board: {os.path.basename(self.filename)}')
        plt.tight_layout()
        
        if address is not None:
            print("Saving the solution for :" , file_name)
            plt.savefig(os.path.join(address, f"{file_name}_solution.png"))
            plt.close()
        else:
            plt.show()

    def propagate(self) -> None:
        """
        Propagate all lazors until all of them have ended.
        """
        self.path = []
        while any(not lazor.end for lazor in self.lazors):
            #print(self.lazors)
            for lazor in self.lazors:
                if lazor.end:
                    #print("continue 1")
                    continue
                
                # 1 Check if the lazor hits a block before moving to the new position
                if lazor.position[0] % 2 == 0:  # Check x direction
                    check_x = (lazor.position[0] + lazor.direction[0]) // 2
                    check_y = lazor.position[1] // 2
                    if self.grid[check_y][check_x] not in ['o', 'x']:
                        self.interact_with_block(lazor, check_x, check_y)
                        
                elif lazor.position[1] % 2 == 0:  # Check y direction
                    check_x = lazor.position[0] // 2
                    check_y = (lazor.position[1] + lazor.direction[1]) // 2
                    if self.grid[check_y][check_x] not in ['o', 'x']:
                        self.interact_with_block(lazor, check_x, check_y)
                        
                new_x = lazor.position[0] + lazor.direction[0]
                new_y = lazor.position[1] + lazor.direction[1]
                # 2 Check if the lazor hits a boundary
                if new_x <= 0 or new_x >= len(self.grid[0]) * 2 or new_y <= 0 or new_y >= len(self.grid) * 2:
                    lazor.end = True
                    path_segment = (lazor.position, (new_x, new_y))
                    lazor.position = (new_x, new_y)
                    if path_segment not in self.path:
                        self.path.append(path_segment)
                    #print("continue 2")
                    continue
                
                # 3 Update path
                path_segment = (lazor.position, (new_x, new_y))
                if path_segment not in self.path:
                    self.path.append(path_segment)
                else:
                    lazor.end = True
                    #print("continue 3")
                    continue
                
                # 4 Update lazor position
                if self.grid[check_y][check_x] not in ['B']:
                    lazor.position = (new_x, new_y)
                #print(lazor.position)
    
    def interact_with_block(self, lazor: Lazor, x: int, y: int) -> None:
        """
        Handle the interaction of a lazor with a block.
        
        Args:
            lazor (Lazor): The lazor interacting with the block.
            x (int): The x-coordinate of the block.
            y (int): The y-coordinate of the block.
        """
        #print("Interact")
        for block in self.block_objects:
            #print(block)
            if block.position == (x, y):
                #print(block)
                if block.block_type == 'A':
                    #print("Reflect!")
                    # Reflect lazor
                    if lazor.position[0] % 2 == 0:  # Hitting in x direction
                        lazor.direction = (-lazor.direction[0], lazor.direction[1])
                    elif lazor.position[1] % 2 == 0:  # Hitting in y direction
                        lazor.direction = (lazor.direction[0], -lazor.direction[1])
                elif block.block_type == 'B':
                    #print("Opague!")
                    # Opaque block, lazor ends
                    lazor.direction = (0,0)
                    lazor.end = True
                    
                elif block.block_type == 'C':
                    #print("Refract!")
                    # Refract block, lazor continues and a new lazor is created
                    if lazor.position[0] % 2 == 0:  # Hitting in x direction
                        new_direction = (-lazor.direction[0], lazor.direction[1])
                    elif lazor.position[1] % 2 == 0:  # Hitting in y direction
                        new_direction = (lazor.direction[0], -lazor.direction[1])
                    new_lazor = Lazor(position=lazor.position, direction=new_direction)
                    if ([ lazor.position, new_direction] not in self.created_lazors):
                        self.created_lazors.append([lazor.position, new_direction])
                        self.lazors.append(new_lazor)
                    #print(self.lazors)
