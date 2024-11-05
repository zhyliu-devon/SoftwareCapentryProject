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


