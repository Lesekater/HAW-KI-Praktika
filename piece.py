import copy
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
def getMovesForPosition(board: Board, x: int, y: int) -> tuple[list[Board], int]:
    """Returns the possible Moves for a single piece on a board"""
    possibleMoves: list[Board] = list()
    pieceToMove: EPiece = board.data[y][x]
    directionsToCheck: list[Direction] = list()

    # TODO: Move all this crap into the getDiagonalContent() function. Its is clutter that is ugly and i hate it.
    # I REAAALY WANT TO DO THIS RIGHT KNOW. BUT I AM VERY EEPY. THE DUALITY OF EEPYNESS :3

    # Create a list with all the diagonal directions we need to check for a given piece
    if pieceToMove == EPiece.EMPTY:
        print("Cannot check moves for an empty spot")
        return (possibleMoves, -1)
    if pieceToMove == EPiece.DEFAULT_P1 or pieceToMove.value > 2: #Check for these Directions if it's a player 1 piece or a dame
        directionsToCheck.append(Direction.Down_Left)
        directionsToCheck.append(Direction.Down_Right)
    if pieceToMove == EPiece.DEFAULT_P2 or pieceToMove.value > 2: #Check for these Directions if it's a player 2 piece or a dame
        directionsToCheck.append(Direction.Up_Left)
        directionsToCheck.append(Direction.Up_Right)

    # Check those diagonals
    diaToCheck: dict[Direction, list[EPiece]] = getDiagonalContent(board, directionsToCheck, x, y)

    # Do sick moves
    for d in diaToCheck:
        movesForDir: list[Board] = checkDirection(board, d, diaToCheck[d], pieceToMove, x, y)
        for m in movesForDir:
            possibleMoves.append(m)

    return possibleMoves

def checkDirection(board: Board, direction: Direction, dia: list[EPiece], piece: EPiece, x: int, y: int) -> tuple[list[Board], int]:
    moves: list[Board] = list()
    capturedPieces: int = 0

    if not checkIfPiecesOppose(piece, dia[0]):
        return (moves, 0)

    searchMods: tuple[int, int] = getSearchModifiyerForDirection(direction)
    xMod: int = searchMods[0]
    yMod: int = searchMods[1]

    newPosX: int = -1
    newPosY: int = -1
    furtherMoves: tuple[list[Board], int] = (list(), -1)
    move: Board = board

    # Default
    if piece.value < 3 and piece.value > 0:
        # WALK
        if dia[0] == EPiece.EMPTY:
            move = board.swap(x, y, x+xMod, y+yMod)
            moves.append(move)
            return (moves, 0)
        # FIGHT
        elif dia[1] == EPiece.EMPTY:
            newPosX = x+xMod+xMod
            newPosY = y+yMod+yMod
            capturedPieces += 1
            move = board.swap(x, y, newPosX, newPosY).strikePiece(x+xMod, y+yMod)
            furtherMoves = getMovesForPosition(move,newPosX, newPosY)
        # ???
        else:
            return (moves, -1)
    # Dame
    else:
        firstPiece: tuple[int, EPiece] = getFirstNonEmpty(dia)
        # The next Piece on diagonal is friendly, only WALK
        if firstPiece[0] > 0 and not checkIfPiecesOppose(piece, firstPiece[1]):
            for i in range(firstPiece[0]):
                move = board.swap(x, y, x+i*xMod, y+i*yMod)
                moves.append(move)
                return (moves, 0)
        # Next piece on diagonal is enemy, FIGHT
        elif dia[firstPiece[0]+1] == EPiece.EMPTY and checkIfPiecesOppose(piece, firstPiece[1]):
            newPosX = x+firstPiece[0]*xMod+xMod
            newPosY = y+firstPiece[0]*yMod+yMod
            move = board.swap(x, y, newPosX, newPosY).strikePiece(newPosX - xMod, newPosY - yMod)
            capturedPieces += 1
            furtherMoves = getMovesForPosition(move,newPosX, newPosY)
        # ???
        else:
            return (moves, -1)


    # Look for further moves
    if furtherMoves[1] > 0 and capturedPieces > 0:
        for m in furtherMoves[0]:
            capturedPieces += furtherMoves[1]
            moves.append(m)
    else:
        moves.append(move)
    return (moves, capturedPieces)



def checkIfPiecesOppose(f: EPiece, s: EPiece) -> bool:
    if ((f == EPiece.DEFAULT_P1 or f == EPiece.DAME_P1) and (s == EPiece.DEFAULT_P2 or EPiece.DAME_P2)) or \
        ((f == EPiece.DEFAULT_P2 or f == EPiece.DAME_P2) and (s == EPiece.DEFAULT_P1 or EPiece.DAME_P1)):
        return True
    else:
        return False

def getFirstNonEmpty(l: list[EPiece]) -> tuple[int, EPiece]:
    for idx, p in enumerate(l):
        if p != EPiece.EMPTY:
            return (idx, p)
    return (-1, EPiece.EMPTY)

def getSearchModifiyerForDirection(d: Direction) -> tuple[int, int]:
    xSearchModifyer: int = 1
    ySearchModifyer: int = 1

    if d == Direction.Up_Right or d == Direction.Up_Left:
        ySearchModifyer = -1
    if d == Direction.Up_Left or d == Direction.Down_Left:
        xSearchModifyer = -1

    return (xSearchModifyer, ySearchModifyer)
    

def getDiagonalContent(board: Board, directions: list[Direction], startX: int, startY: int) -> dict[Direction, list[EPiece]]:
    """Returns a dict with a direction as a key and the contents of the to the direction appropriate diagonal line"""
    movesForDir: dict[Direction, list[EPiece]] = {}
    for dir in directions:
        movesForDir[dir] = contentOfDiagonals(board, dir, startX, startY)
    return movesForDir


def contentOfDiagonals(board: Board, direction: Direction, startX: int, startY: int) -> list[EPiece]:
    """Returns a list of pieces that represent the contents of a diagonal from a given start point"""
    contentInDir: list[EPiece] = list()

    searchMods: tuple[int, int] = getSearchModifiyerForDirection(direction)
    xSearchModifyer: int = searchMods[0]
    ySearchModifyer: int = searchMods[1]

    x: int = startX
    y: int = startY

    size_x = len(board.data[0])
    size_y = len(board.data)

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
