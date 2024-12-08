from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

# Board:
# id: UUID = None
# data: List[List[EPiece]] = []
# f: float = 0.0
# g: float = 0.0
# player1: bool = True
# parent: 'Board' = None

# calculates all possible moves for a given board state
### Params:
# board: Board (current board state)
# player1: bool (current player)
#
# Returns:
# tuple[List[Board], bool] (list of possible moves, is winning move)
# getMoves(<Board>, <bool>) -> Tuple[List[Board], bool]

# minimax implementation
### Params:
# nodeToExpand: Board (current board state)
# usedHeuristic: heurisitcTypes (heuristic to use)
#
# Returns:
# tuple[Board, bool] (new board state, is winning move)
# def makeMove(nodeToExpand: Board,
#              usedHeuristic: heurisitcTypes = heurisitcTypes.CountOfPieces
#              ) -> tuple[Board, bool]:

initialDepth = 10

def minimax(node: Board, depth: int, maximizingPlayer: bool, usedHeuristic: heurisitcTypes) -> Tuple[float, Board, bool]:
    possibleMoves, isWinningMove = getMoves(node, maximizingPlayer)
    if depth == 0 or isWinningMove:
        global initialDepth
        return calculateHeuristic(node, usedHeuristic), node, (isWinningMove and depth == initialDepth)

    if maximizingPlayer:
        minEval = float('inf')  # Initialize to positive infinity for minimizing heuristic
        bestMove = None
        for child in possibleMoves:
            eval, _, childIsWinning = minimax(child, depth - 1, False, usedHeuristic)
            if eval < minEval:  # Lower heuristic value is better
                minEval = eval
                bestMove = child
            if childIsWinning:
                return minEval, bestMove, True
        return minEval, bestMove, False
    else:
        maxEval = float('-inf')  # Initialize to negative infinity for maximizing heuristic
        bestMove = None
        for child in possibleMoves:
            eval, _, childIsWinning = minimax(child, depth - 1, True, usedHeuristic)
            if eval > maxEval:  # Higher heuristic value is worse
                maxEval = eval
                bestMove = child
            if childIsWinning:
                return maxEval, bestMove, True
        return maxEval, bestMove, False

def makeMove(nodeToExpand: Board, usedHeuristic) -> Tuple[bool, Board]:
    global initialDepth
    initialDepth = 5
    _, bestMove, isWinningMove = minimax(nodeToExpand, initialDepth, nodeToExpand.player1, usedHeuristic)
    return isWinningMove, bestMove