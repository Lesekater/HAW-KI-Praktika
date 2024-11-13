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
def getMoves(board: Board, player1: bool) -> tuple[list[Board], bool]:
    """Returns all possible moves for a player, given a specifiv board. Also specifies if a move would be a winning one"""
    # TODO: Implement
    # Lars
    return [], False

# Player1 is odd  numbers (1 and 3) (Black)
# Player2 is even numbers (2 and 4) (White)

# Player1 moves in positive direction (down)
# Player2 moves in negative direction (up)
def getMovesForPosition(board: Board, x: int, y: int) -> list[Board]:
    """Returns the possible Moves for a single piece on a board"""
    possibleMoves: list[Board] = list()
    pieceToMove: EPiece = board.data[x][y]
    directionsToCheck: list[Direction] = list()

    # TODO: Move all this crap into the getDiagonalContent() function. Its is clutter that is ugly and i hate it.
    # I REAAALY WANT TO DO THIS RIGHT KNOW. BUT I AM VERY EEPY. THE DUALITY OF EEPYNESS :3

    # Create a list with all the diagonal directions we need to check for a given piece
    if pieceToMove == EPiece.EMPTY:
        print("Cannot check moves for an empty spot")
        return possibleMoves
    if pieceToMove == EPiece.DEFAULT_P1 or pieceToMove.value > 2: # Check for these Directions if it's a player 1 piece or a dame
        directionsToCheck.append(Direction.Down_Left)
        directionsToCheck.append(Direction.Down_Right)
    if pieceToMove == EPiece.DEFAULT_P2 or pieceToMove.value > 2: # Check for these Directions if it's a player 2 piece or a dame
        directionsToCheck.append(Direction.Up_Left)
        directionsToCheck.append(Direction.Up_Right)

    # Check those diagonals
    diaToCheck: dict[Direction, list[EPiece]] = getDiagonalContent(board, directionsToCheck, x, y)

    return possibleMoves

def getDiagonalContent(board: Board, directions: list[Direction], startX: int, startY: int) -> dict[Direction, list[EPiece]]:
    """Returns a dict with a direction as a key and the contents of the to the direction appropriate diagonal line"""
    movesForDir: dict[Direction, list[EPiece]] = {}
    for dir in directions:
        movesForDir[dir] = contentOfDiagonals(board, dir, startX, startY)
    return movesForDir


def contentOfDiagonals(board: Board, direction: Direction, startX: int, startY: int) -> list[EPiece]:
    """Returns a list of pieces that represent the contents of a diagonal from a given start point"""
    contentInDir: list[EPiece] = list()
    xSearchModifyer: int = 1
    ySearchModifyer: int = 1

    x: int = startX
    y: int = startY

    size_x = len(board.data[0])
    size_y = len(board.data)

    if direction == Direction.Up_Right or direction == Direction.Up_Left:
        ySearchModifyer = -1
    if direction == Direction.Up_Left or direction == Direction.Down_Left:
        xSearchModifyer = -1

    print("ySearchModifyer: " + str(ySearchModifyer))
    print("xSearchModifyer: " + str(xSearchModifyer))

    x += xSearchModifyer
    y += ySearchModifyer
    while (x > -1 and x < size_x) and (y > -1 and y < size_y):
        contentInDir.append(EPiece(board.data[y][x]))
        print("x: " + str(x), "y: " + str(y) + " | " + str(EPiece(board.data[y][x])))
        x += xSearchModifyer
        y += ySearchModifyer

    return contentInDir
