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
    
