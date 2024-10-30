from enum import Enum
from typing import List

from piece import getMoves

class EPiece(Enum):
    EMPTY = 0
    DEFAULT_P1 = 1
    DEFAULT_P2 = 2
    DAME_P1 = 3
    DAME_P2 = 4

class Board:
    data: List[List[int]] = []

openList: List[Board] = []
closedList: List[Board] = []

def main():
    while(True):
        #algo stuff
        possibleMoves = getMoves(Board(), True)

        # TODO: Implement
        # Elias
        
    return
