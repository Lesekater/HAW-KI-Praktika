from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

initialDepth = 10
evaluatedNodes = 0

def minimax(node: Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool, usedHeuristic: heurisitcTypes) -> Tuple[float, Board, bool]:
    global evaluatedNodes
    evaluatedNodes += 1
    
    possibleMoves, isWinningMove = getMoves(node, maximizingPlayer)
    if depth == 0 or isWinningMove:
        global initialDepth
        return calculateHeuristic(node, usedHeuristic), node, (isWinningMove and depth == initialDepth)

    if maximizingPlayer:
        minEval = float('inf')  # Initialize to positive infinity for minimizing heuristic
        bestMove = None
        for child in possibleMoves:
            eval, _, childIsWinning = minimax(child, depth - 1, alpha, beta, False, usedHeuristic)
            if eval < minEval:  # Lower heuristic value is better
                minEval = eval
                bestMove = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
            if childIsWinning:
                return minEval, bestMove, True
        return minEval, bestMove, False
    else:
        maxEval = float('-inf')  # Initialize to negative infinity for maximizing heuristic
        bestMove = None
        for child in possibleMoves:
            eval, _, childIsWinning = minimax(child, depth - 1, alpha, beta, True, usedHeuristic)
            if eval > maxEval:  # Higher heuristic value is worse
                maxEval = eval
                bestMove = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            if childIsWinning:
                return maxEval, bestMove, True
        return maxEval, bestMove, False

def makeMove(nodeToExpand: Board, usedHeuristic) -> Tuple[bool, Board, int]:
    global initialDepth, evaluatedNodes
    initialDepth = 5
    evaluatedNodes = 0
    _, bestMove, isWinningMove = minimax(nodeToExpand, initialDepth, float('-inf'), float('inf'), nodeToExpand.player1, usedHeuristic)
    print(f"Number of evaluated nodes: {evaluatedNodes} (for player {1 if nodeToExpand.player1 else 2})")

    # if no moves are found, the board is in a winning state (no moves left)
    if bestMove is None:
        return True, nodeToExpand, evaluatedNodes

    return isWinningMove, bestMove, evaluatedNodes
