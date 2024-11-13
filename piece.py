import copy
from const import Board, EPiece
from enum import Enum

from util import formatBoard

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

    hypotheticalPiece: EPiece = EPiece.DEFAULT_P2
    if player1:
        hypotheticalPiece = EPiece.DEFAULT_P1

    highestKDRList: list[Board] = []
    highestKDR: int = -1
    for yIdx, y in enumerate(board.data):
        for xIdx, p in enumerate(y):
            if not checkIfPiecesOppose(p ,hypotheticalPiece):
                mFP = getMovesForPosition(board, xIdx, yIdx)
                if mFP[1] > highestKDR:
                    highestKDRList = []
                if mFP[1] >= highestKDR:
                    for m in mFP[0]:
                        highestKDRList.append(m)


    for m in highestKDRList:
        if checkForWinningBoard(m):
            return [m], True



    return highestKDRList, False

def checkForWinningBoard(b: Board) -> bool:
    foundP1: bool = False
    foundP2: bool = False
    for y in b.data:
        for x in y:
            if x == EPiece.DEFAULT_P1 or x == EPiece.DAME_P1:
                foundP1 = True
            if x == EPiece.DEFAULT_P2 or x == EPiece.DAME_P2:
                foundP2 = True

    return not(foundP1 and foundP2)
# Player1 is odd  numbers (1 and 3) (Black)
# Player2 is even numbers (2 and 4) (White)

# Player1 moves in positive direction (down)
# Player2 moves in negative direction (up)
def getMovesForPosition(board: Board, x: int, y: int) -> tuple[list[Board], int]:
    """Returns the possible Moves for a single piece on a board"""
    possibleMoves: list[Board] = []
    pieceToMove: EPiece = board.data[y][x]
    directionsToCheck: list[Direction] = []

    # TODO: Move all this crap into the getDiagonalContent() function. Its is clutter that is ugly and i hate it.
    # I REAAALY WANT TO DO THIS RIGHT KNOW. BUT I AM VERY EEPY. THE DUALITY OF EEPYNESS :3

    # Create a list with all the diagonal directions we need to check for a given piece
    print("pieceToMove: " + str(pieceToMove))
    if pieceToMove == EPiece.EMPTY:
        print("Cannot check moves for an empty spot")
        return possibleMoves, -1
    if pieceToMove == EPiece.DEFAULT_P1 or pieceToMove.value > 2: #Check for these Directions if it's a player 1 piece or a dame
        directionsToCheck.append(Direction.Down_Left)
        directionsToCheck.append(Direction.Down_Right)
    if pieceToMove == EPiece.DEFAULT_P2 or pieceToMove.value > 2: #Check for these Directions if it's a player 2 piece or a dame
        directionsToCheck.append(Direction.Up_Left)
        directionsToCheck.append(Direction.Up_Right)

    print("x: " + str(x) + " y: " + str(y))
    print("directionsToCheck: " + str(directionsToCheck))

    # Check those diagonals
    diaToCheck: dict[Direction, list[EPiece]] = getDiagonalContent(board, directionsToCheck, x, y)

    # remove empty lists from diaToCheck dict
    diaToCheck = {k: v for k, v in diaToCheck.items() if v}

    if not diaToCheck:
        return possibleMoves, -1
    
    print("diaToCheck: " + str(diaToCheck))

    # Do sick moves
    map: dict[int, list[Board]] = {}
    highestKDR: int = -1
    for d in diaToCheck:
        moves: tuple[list[Board], int] = checkDirection(board, d, diaToCheck[d], pieceToMove, x, y)

        print("moves: " + str(moves))

        if moves[1] > highestKDR:
            highestKDR = moves[1]
        if moves[1] not in map:
            map[moves[1]]=[]
        for m in moves[0]:
            map[moves[1]].append(m)


    return map[highestKDR], highestKDR

def checkDirection(board: Board, direction: Direction, dia: list[EPiece], piece: EPiece, x: int, y: int) -> tuple[list[Board], int]:
    moves: list[Board] = []
    capturedPieces: int = 0

    print("self: " + str(piece) + ", opponent: " + str(dia[0]))
    print("checkIfPiecesOppose(piece, dia[0]): " + str(checkIfPiecesOppose(piece, dia[0])))

    # TODO: check -> I removed the if "not" -- is this correct?
    if checkIfPiecesOppose(piece, dia[0]):
        return moves, 0

    searchMods: tuple[int, int] = getSearchModifiyerForDirection(direction)
    xMod: int = searchMods[0]
    yMod: int = searchMods[1]

    newPosX: int = -1
    newPosY: int = -1
    furtherMoves: tuple[list[Board], int] = ([], -1)
    move: Board = board

    print("piece: " + str(piece))

    # Default
    if piece.value < 3 and piece.value > 0:
        newPosX = x+xMod+xMod
        newPosY = y+yMod+yMod
        # WALK
        if dia[0] == EPiece.EMPTY:
            move = board.swap(x, y, x+xMod, y+yMod)
            moves.append(move)
            return moves, 0
        # FIGHT
        elif checkForInBounds(board, newPosX, newPosY) and dia[1] == EPiece.EMPTY:
            capturedPieces += 1
            move = board.swap(x, y, newPosX, newPosY).strikePiece(x+xMod, y+yMod)
            furtherMoves = getMovesForPosition(move,newPosX, newPosY)
        # ???
        else:
            return moves, -1
    # Dame
    elif piece.value > 2 and piece.value < 5:
        firstPiece: tuple[int, EPiece] = getFirstNonEmpty(dia)
        newPosX = x+firstPiece[0]*xMod+xMod
        newPosY = y+firstPiece[0]*yMod+yMod
        # The next Piece on diagonal is friendly or only empty, WALK
        if (firstPiece[0] > 0 or firstPiece[1] == EPiece.EMPTY) and not checkIfPiecesOppose(piece, firstPiece[1]):
            print("WALK")
            rangeToEnd = len(dia) if firstPiece[0] == -1 else firstPiece[0]
            print("rangeToEnd: " + str(rangeToEnd))
            for i in range(rangeToEnd):
                i += 1
                print("i: " + str(i) + " xMod: " + str(xMod) + " yMod: " + str(yMod))
                print("x: " + str(x+i*xMod) + " y: " + str(y+i*yMod))
                move = board.swap(x, y, x+i*xMod, y+i*yMod)
                moves.append(move)
            return moves, 0
        # Next piece on diagonal is enemy, FIGHT
        elif checkForInBounds(board, newPosX, newPosY) and dia[firstPiece[0]+1] == EPiece.EMPTY and checkIfPiecesOppose(piece, firstPiece[1]):
            print("FIGHT")
            move = board.swap(x, y, newPosX, newPosY).strikePiece(newPosX - xMod, newPosY - yMod)
            capturedPieces += 1
            furtherMoves = getMovesForPosition(move,newPosX, newPosY)
        # ???
        else:
            print("??? 1")
            return moves, -1
    #???
    else:
        print("??? 2")
        return moves, -1


    # Look for further moves
    if furtherMoves[1] > 0 and capturedPieces > 0:
        capturedPieces += furtherMoves[1]
        for m in furtherMoves[0]:
            moves.append(m)
    else:
        moves.append(move)
    return moves, capturedPieces


def checkForInBounds(board: Board, x: int, y:int) -> bool:
    size_x = len(board.data[0])
    size_y = len(board.data)
    if (x >= size_x - 1) or (y >= size_y - 1):
        print("OUT OF BOUNDS")
        return True
    return False

def checkIfPiecesOppose(f: EPiece, s: EPiece) -> bool:
    print("f: " + str(f) + " s: " + str(s))
    if s == EPiece.EMPTY:
        return False
    elif (f in {EPiece.DEFAULT_P1, EPiece.DAME_P1} and s in {EPiece.DEFAULT_P1, EPiece.DAME_P1}) or \
         (f in {EPiece.DEFAULT_P2, EPiece.DAME_P2} and s in {EPiece.DEFAULT_P2, EPiece.DAME_P2}):
        return True
    else:
        return False

def getFirstNonEmpty(l: list[EPiece]) -> tuple[int, EPiece]:
    for idx, p in enumerate(l):
        if p != EPiece.EMPTY:
            return idx, p
    return -1, EPiece.EMPTY

def getSearchModifiyerForDirection(d: Direction) -> tuple[int, int]:
    xSearchModifyer: int = 1
    ySearchModifyer: int = 1

    if d == Direction.Up_Right or d == Direction.Up_Left:
        ySearchModifyer = -1
    if d == Direction.Up_Left or d == Direction.Down_Left:
        xSearchModifyer = -1

    return xSearchModifyer, ySearchModifyer
    

def getDiagonalContent(board: Board, directions: list[Direction], startX: int, startY: int) -> dict[Direction, list[EPiece]]:
    """Returns a dict with a direction as a key and the contents of the to the direction appropriate diagonal line"""
    movesForDir: dict[Direction, list[EPiece]] = {}
    for dir in directions:
        movesForDir[dir] = contentOfDiagonals(board, dir, startX, startY)
    return movesForDir


def contentOfDiagonals(board: Board, direction: Direction, startX: int, startY: int) -> list[EPiece]:
    """Returns a list of pieces that represent the contents of a diagonal from a given start point"""
    contentInDir: list[EPiece] = []

    searchMods: tuple[int, int] = getSearchModifiyerForDirection(direction)
    xSearchModifyer: int = searchMods[0]
    ySearchModifyer: int = searchMods[1]

    x: int = startX
    y: int = startY

    size_x = len(board.data[0])
    size_y = len(board.data)

    # print("ySearchModifyer: " + str(ySearchModifyer))
    # print("xSearchModifyer: " + str(xSearchModifyer))

    x += xSearchModifyer
    y += ySearchModifyer
    while (x > -1 and x < size_x) and (y > -1 and y < size_y):
        contentInDir.append(EPiece(board.data[y][x]))
        # print("x: " + str(x), "y: " + str(y) + " | " + str(EPiece(board.data[y][x])))
        x += xSearchModifyer
        y += ySearchModifyer

    return contentInDir
