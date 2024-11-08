from typing import List, Tuple
from const import Board, EPiece
from enum import Enum

class Direction(Enum):
    Up_Right = 1
    Up_Left = 2
    Down_Left = 3
    Down_Right = 4

###
# Piece
# @return Possible Moves, isWinningMove
###
def getMoves(board: Board, player1: bool) -> Tuple[List[Board], bool]:
    # TODO: Implement
    # Lars
    return [], False

# Player1 is odd  numbers (1 and 3) (Black)
# Player2 is even numbers (2 and 4) (White)

# Player1 moves in positive direction (down)
# Player2 moves in negative direction (up)
def getMovesForPosition(board: Board, x: int, y: int) -> List[Board]:
    possibleMoves: List[Board] = List()
    pieceToMove: EPiece = EPiece(board.data[x][y])
    # if pieceToMove == EPiece.DEFAULT_P1:
    return possibleMoves

def contentOfDiagonals(direction: Direction) -> List[EPiece]:
    contentInDir: List[EPiece] = List()
    xSearchModifyer: int = 1
    ySearchModifyer: int = 1
    if direction == Direction.Up_Right or direction == Direction.Up_Left:
        ySearchModifyer = -1
    if direction == Direction.Up_Left or direction == Direction.Down_Left:
        xSearchModifyer = -1

    return contentInDir
