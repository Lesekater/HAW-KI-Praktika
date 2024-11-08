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

def CustomDiagonals(board: Board, directions: List[Direction], startX: int, startY:int) -> dict(Direction, List[EPiece]):
    return "test"

def contentOfDiagonals(board: Board, direction: Direction, startX: int, startY: int) -> List[EPiece]:
    contentInDir: List[EPiece] = List()
    xSearchModifyer: int = 1
    ySearchModifyer: int = 1

    x: int = startX
    y: int = startY

    if direction == Direction.Up_Right or direction == Direction.Up_Left:
        ySearchModifyer = -1
    if direction == Direction.Up_Left or direction == Direction.Down_Left:
        xSearchModifyer = -1

    x += xSearchModifyer
    y += ySearchModifyer
    while (x > -1 and x < 8 and y > -1 and y < 8):
        contentInDir.append(EPiece(board.data[x][y]))
        x += xSearchModifyer
        y += ySearchModifyer
        print(x)
        print(y)

    return contentInDir
