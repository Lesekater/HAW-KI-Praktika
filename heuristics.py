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

def normalizeTo100(value: float, max_value: float) -> float:
    """Normalizes the value to a range between 0 and 100."""
    return min(max(value / max_value * 100, 0), 100)

def calculateHeuristic(board: Board, usedHeuristic: heurisitcTypes) -> float:
    match usedHeuristic:
        case heurisitcTypes.CountOfPieces:
            return normalizeTo100(countOfPieces(board), 8)
        case heurisitcTypes.CountOfDames:
            return normalizeTo100(countOfDames(board), 8)
        case heurisitcTypes.CountOfPiecesAndDames:
            # return countOfPiecesAndDames(board)
            return normalizeTo100(countOfPiecesAndDames(board), 8)
        case heurisitcTypes.CountOfPiecesOfOtherPlayer:
            return normalizeTo100(countOfPiecesOfOtherPlayer(board), 8)
        case heurisitcTypes.CountOfDamesOfOtherPlayer:
            return normalizeTo100(countOfDamesOfOtherPlayer(board), 8)
        case heurisitcTypes.CountOfPiecesAndDamesOfOtherPlayer:
            return normalizeTo100(countOfPiecesAndDamesOfOtherPlayer(board), 8)
        case heurisitcTypes.CountOfPiecesToEliminate:
            return "unimplemented"
            # return normalizeTo100(countOfPiecesToEliminate(board), 12)  # assuming 12 is the maximum number of pieces to eliminate
        case heurisitcTypes.CountOfPiecesAtEndOfBoard:
            return normalizeTo100(countOfPiecesAtEndOfBoard(board), 4)
        case heurisitcTypes.ProgressPiecesOnBoard:
            return progressPiecesOnBoard(board)
        case heurisitcTypes.CountOfPicesNotInDraw:
            return "unimplemented"
            # return normalizeTo100(countOfPicesNotInDraw(board), 12)
        case heurisitcTypes.Random:
            return randomHeuristic(board)
        case _:
            return 0.0

def countOfPieces(board: Board, maxPieces=8):
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1 and currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2 and not currentPlayer:
                count += 1
    return maxPieces - count

def countOfDames(board, maxPieces=8):
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
    return countOfPieces(board) + countOfDames(board) - 8

def countOfPiecesAtEndOfBoard(board):
    currentPlayer = board.player1
    count = 0

    maxPiecesAtEnd = len(board.data[0])/2

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
    lengthOfBoard = len(board.data[0])  # 8 for an 8x8 board
    currentPlayer = board.player1
    count = 0
    total_pieces = 0

    # Iterate through all rows and pieces to calculate progress
    for row in board.data:
        for i, piece in enumerate(row):
            if currentPlayer:
                if piece == EPiece.DEFAULT_P1:
                    # Add distance from the start of the board (i + 1) to the score
                    count += (i + 1)
                    total_pieces += 1
            else:
                if piece == EPiece.DEFAULT_P2:
                    # Add distance from the start of the board (i + 1) to the score
                    count += (i + 1)
                    total_pieces += 1

    # If there are no pieces, return a default value (e.g., 0)
    if total_pieces == 0:
        return 0

    # Normalize the heuristic to be in a range [0, max_score]
    max_possible_score = total_pieces * lengthOfBoard  # Max possible score when all pieces are at the start
    progress_heuristic = (count / max_possible_score) * 100  # Scale it to a 0-100 range

    return progress_heuristic

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

def randomHeuristic(board: Board):
    random.seed(
        hash(str(board.data))
    )
    return random.randint(0, 100)