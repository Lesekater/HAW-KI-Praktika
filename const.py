from enum import Enum
from typing import List

class EPiece(Enum):
    EMPTY = 0
    DEFAULT_P1 = 1
    DEFAULT_P2 = 2
    DAME_P1 = 3
    DAME_P2 = 4
    
class Board:
    def __init__(self, boardArray: List[List[int]]):
        self.data = boardArray
        self.f = 0.0
        self.g = 0.0
        self.player1 = True

    data: List[List[int]] = []
    f: float = 0.0
    g: float = 0.0
    player1: bool = True
