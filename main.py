from enum import Enum
from typing import List

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
    # do stuff
    return
