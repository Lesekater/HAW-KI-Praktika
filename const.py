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

    def __swapOnSelf(self, firstX: int, firstY: int, secondX: int, secondY: int):
        firstPiece: EPiece = self.data[firstY][firstX]
        secondPiece: EPiece = self.data[secondY][secondX]
        self.data[firstY][firstX] = secondPiece
        self.data[secondY][secondX] = firstPiece

    def swap(self, firstX: int, firstY: int, secondX: int, secondY: int) -> 'Board':
        nB: 'Board' = copy.deepcopy(self)
        nB.__swapOnSelf(firstX, firstY, secondX, secondY)
        return nB

    def __strikePieceOnSelf(self, x: int, y:int):
        self.data[y][x] = EPiece.EMPTY

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

testBoard1 = Board.fromIntList([
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2]])

testBoard2 = Board.fromIntList([
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 2]])

testBoard3 = Board.fromIntList([
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 2]])

testBoard4 = Board.fromIntList([
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0],
    [2, 0, 2, 0, 2]])

testBoard5 = Board.fromIntList([
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 2, 0, 2],
    [2, 0, 2, 0]])

testBoards = [testBoard1, testBoard2, testBoard3, testBoard4, testBoard5]
