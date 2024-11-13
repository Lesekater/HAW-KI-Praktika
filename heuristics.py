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
    Random = 7

def calculateHeuristic(board: Board, usedHeuristic: heurisitcTypes) -> float:
    match usedHeuristic:
        case heurisitcTypes.CountOfPieces:
            return countOfPieces(board)
        # case heurisitcTypes.CountOfDames:
        #     return countOfDames(board)
        # case heurisitcTypes.CountOfPiecesAndDames:
        #     return countOfPiecesAndDames(board)
        # case heurisitcTypes.CountOfPiecesToEliminate:
        #     return countOfPiecesToEliminate(board)
        # case heurisitcTypes.CountOfPiecesAtEndOfBoard:
        #     return countOfPiecesAtEndOfBoard(board)
        # case heurisitcTypes.ProgressPiecesOnBoard:
        #     return progressPiecesOnBoard(board)
        # case heurisitcTypes.CountOfPicesNotInDraw:
        #     return countOfPicesNotInDraw(board)
        # case heurisitcTypes.Random:
        #     return random(board)
        case _:
            return 0.0

def countOfPieces(board: Board) -> float:
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1.value and currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2.value and not currentPlayer:
                count += 1

    return count

def countOfDames(board):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DAME_P1.value and currentPlayer:
                count += 1
            elif piece == EPiece.DAME_P2.value and not currentPlayer:
                count += 1

    return count