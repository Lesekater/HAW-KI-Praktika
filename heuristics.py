import random
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
    Random = 10

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
        case heurisitcTypes.CountOfPiecesToEliminate:
            return "unimplemented"
            # return countOfPiecesToEliminate(board)
        case heurisitcTypes.CountOfPiecesAtEndOfBoard:
            return countOfPiecesAtEndOfBoard(board)
        case heurisitcTypes.ProgressPiecesOnBoard:
            return progressPiecesOnBoard(board)
        case heurisitcTypes.CountOfPicesNotInDraw:
            return "unimplemented"
            # return countOfPicesNotInDraw(board)
        case heurisitcTypes.Random:
            return randomHeuristic(board)
        case _:
            return 0.0

def countOfPieces(board: Board, maxPieces=12):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1 and currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2 and not currentPlayer:
                count += 1
    return maxPieces - count

def countOfDames(board, maxPieces=12):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DAME_P1 and currentPlayer:
                count += 1
            elif piece == EPiece.DAME_P2 and not currentPlayer:
                count += 1

    return maxPieces - count

def countOfPiecesAndDames(board):
    return countOfPieces(board) + countOfDames(board)

def countOfPiecesAtEndOfBoard(board):
    currentPlayer = board.player1
    count = 0

    maxPiecesAtEnd = len(board.data[0])

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

    return maxPiecesAtEnd - count

def progressPiecesOnBoard(board):
    lengthOfBoard = len(board.data[0])

    currentPlayer = board.player1
    count = 0

    for row in board.data:
        for (i, piece) in enumerate(row):
            if currentPlayer:
                if piece == EPiece.DEFAULT_P1:
                    count += lengthOfBoard - i
            else:
                if piece == EPiece.DEFAULT_P2:
                    count += lengthOfBoard - i

    return count

def countOfPiecesOfOtherPlayer(board):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1 and not currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2 and currentPlayer:
                count += 1

    return count

def countOfDamesOfOtherPlayer(board):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DAME_P1 and not currentPlayer:
                count += 1
            elif piece == EPiece.DAME_P2 and currentPlayer:
                count += 1

    return count

def countOfPiecesAndDamesOfOtherPlayer(board):
    return countOfPiecesOfOtherPlayer(board) + countOfDamesOfOtherPlayer(board)

def randomHeuristic(board):
    return random.randint(0, 10)