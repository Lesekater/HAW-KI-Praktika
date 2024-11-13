import copy
from enum import Enum
from typing import List
from uuid import UUID
import uuid

class EPiece(Enum):
    EMPTY = 0
    DEFAULT_P1 = 1
    DEFAULT_P2 = 2
    DAME_P1 = 3
    DAME_P2 = 4
    
class Board:
    def __init__(self, boardArray: List[List[int]]):
        self.id = uuid.uuid1()
        self.data = boardArray
        self.f = 0.0
        self.g = 0.0
        self.player1 = True

    def __swapOnSelf(self, firstX: int, firstY: int, secondX: int, secondY: int):
        firstPiece: EPiece = self.data[firstX][firstY]
        secondPiece: EPiece = self.data[secondX][secondY]
        self.data[firstX][firstY] = secondPiece
        self.data[secondX][secondY] = firstPiece

    def swap(self, firstX: int, firstY: int, secondX: int, secondY: int) -> 'Board':
        nB: 'Board' = copy.deepcopy(self)
        nB.__swapOnSelf(firstX, firstY, secondX, secondY)
        return nB

    def __strikePieceOnSelf(self, x: int, y:int):
        self.data[x][y] = EPiece.EMPTY

    def strikePiece(self, x: int, y:int) -> 'Board':
        nB: 'Board' = copy.deepcopy(self)
        nB.__strikePieceOnSelf(x,y)
        return nB


    id: UUID = None
    data: List[List[EPiece]] = []
    f: float = 0.0
    g: float = 0.0
    player1: bool = True
    parent: 'Board' = None
