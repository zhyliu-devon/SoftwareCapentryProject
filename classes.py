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

