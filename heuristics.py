from const import Board, EPiece
from enum import Enum

class heurisitcTypes(Enum):
    CountOfPieces = 0
    CountOfDames = 1
    CountOfPiecesAndDames = 2
    CountOfPiecesToEliminate = 3
    CountOfPiecesAtEndOfBoard = 4
    ProgressPiecesOnBoard = 5
    CountOfPicesNotInDraw = 6
    CountOfPiecesOfOtherPlayer = 7
    CountOfDamesOfOtherPlayer = 8
    CountOfPiecesAndDamesOfOtherPlayer = 9
    Random = 7

def calculateHeuristic(board: Board, usedHeuristic: heurisitcTypes) -> float:
    match usedHeuristic:
        case heurisitcTypes.CountOfPieces:
            return countOfPieces(board)
        case heurisitcTypes.CountOfDames:
            return countOfDames(board)
        case heurisitcTypes.CountOfPiecesAndDames:
            return countOfPiecesAndDames(board)
        case heurisitcTypes.CountOfPiecesOfOtherPlayer:
            return countOfPiecesOfOtherPlayer(board)
        case heurisitcTypes.CountOfDamesOfOtherPlayer:
            return countOfDamesOfOtherPlayer(board)
        case heurisitcTypes.CountOfPiecesAndDamesOfOtherPlayer:
            return countOfPiecesAndDamesOfOtherPlayer(board)
        # case heurisitcTypes.CountOfPiecesToEliminate:
        #     return countOfPiecesToEliminate(board)
        case heurisitcTypes.CountOfPiecesAtEndOfBoard:
            return countOfPiecesAtEndOfBoard(board)
        case heurisitcTypes.ProgressPiecesOnBoard:
            return progressPiecesOnBoard(board)
        # case heurisitcTypes.CountOfPicesNotInDraw:
        #     return countOfPicesNotInDraw(board)
        case heurisitcTypes.Random:
            return random(board)
        case _:
            return 0.0

def countOfPieces(board: Board) -> float:
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1 and currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2 and not currentPlayer:
                count += 1

    return count

def countOfDames(board):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DAME_P1 and currentPlayer:
                count += 1
            elif piece == EPiece.DAME_P2 and not currentPlayer:
                count += 1

    return count

def countOfPiecesAndDames(board):
    return countOfPieces(board) + countOfDames(board)

def countOfPiecesAtEndOfBoard(board):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        if currentPlayer:
            if row[0] == EPiece.DEFAULT_P1:
                count += 1
            if row[-1] == EPiece.DEFAULT_P1:
                count += 1
        else:
            if row[0] == EPiece.DEFAULT_P2:
                count += 1
            if row[-1] == EPiece.DEFAULT_P2:
                count += 1

    return count

# for each pice on the board count how many moves it took to the end of the board and sum them
# (if piece is at first row it gets 0 points, if it is at the last row it gets 7 points)
def progressPiecesOnBoard(board):
    currentPlayer = board.player1
    count = 0
    for y, row in enumerate(board.data):
        for x, piece in enumerate(row):
            if currentPlayer:
                if piece == EPiece.DEFAULT_P1:
                    count += y
            else:
                if piece == EPiece.DEFAULT_P2:
                    count += 7 - y

    return count

# the less pieces the other player has the more points we get
def countOfPiecesOfOtherPlayer(board, maxPieces=12):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1 and not currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2 and currentPlayer:
                count += 1

    return maxPieces - count

def countOfDamesOfOtherPlayer(board, maxPieces=12):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DAME_P1 and not currentPlayer:
                count += 1
            elif piece == EPiece.DAME_P2 and currentPlayer:
                count += 1

    return maxPieces - count

def countOfPiecesAndDamesOfOtherPlayer(board):
    return countOfPiecesOfOtherPlayer(board) + countOfDamesOfOtherPlayer(board)

def random(board):
    return random.random() * 10