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
    def __init__(self, boardArray: List[List[EPiece]]):
        self.id = uuid.uuid1()
        self.data = boardArray
        self.f = 0.0
        self.g = 0.0
        self.player1 = True

    def fromIntList(boardArray: List[List[int]]) -> 'Board':
        self = Board([])
        self.data = []
        for row in boardArray:
            newRow = []
            for piece in row:
                newRow.append(EPiece(piece))
            self.data.append(newRow)
        return self

    id: UUID = None
    data: List[List[EPiece]] = []
    f: float = 0.0
    g: float = 0.0
    player1: bool = True
    parent: 'Board' = None
