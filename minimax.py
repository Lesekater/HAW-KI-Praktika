from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

initialDepth = 10
evaluatedNodes = 0  # Counter for evaluated nodes
MAX_THREADS = 4  # Limit the number of threads

import concurrent.futures

def minimax(node: Board, depth: int, maximizingPlayer: bool, usedHeuristic: heurisitcTypes) -> Tuple[float, Board, bool]:
    global evaluatedNodes
    evaluatedNodes += 1  # Increment the counter for each node evaluated

    possibleMoves, isWinningMove = getMoves(node, maximizingPlayer)
    if depth == 0 or isWinningMove:
        global initialDepth
        return calculateHeuristic(node, usedHeuristic), node, (isWinningMove and depth == initialDepth)

    def evaluate_move(child):
        return minimax(child, depth - 1, not maximizingPlayer, usedHeuristic)

    if maximizingPlayer:
        minEval = float('inf')  # Initialize to positive infinity for minimizing heuristic
        bestMove = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(evaluate_move, child): child for child in possibleMoves}
            for future in concurrent.futures.as_completed(futures):
                eval, _, childIsWinning = future.result()
                if eval < minEval:  # Lower heuristic value is better
                    minEval = eval
                    bestMove = futures[future]
                if childIsWinning:
                    return minEval, bestMove, True
        return minEval, bestMove, False
    else:
        maxEval = float('-inf')  # Initialize to negative infinity for maximizing heuristic
        bestMove = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(evaluate_move, child): child for child in possibleMoves}
            for future in concurrent.futures.as_completed(futures):
                eval, _, childIsWinning = future.result()
                if eval > maxEval:  # Higher heuristic value is worse
                    maxEval = eval
                    bestMove = futures[future]
                if childIsWinning:
                    return maxEval, bestMove, True
        return maxEval, bestMove, False

def makeMove(nodeToExpand: Board, usedHeuristic) -> Tuple[bool, Board, int]:
    global initialDepth, evaluatedNodes
    initialDepth = 5
    evaluatedNodes = 0  # Reset the counter before starting the minimax
    _, bestMove, isWinningMove = minimax(nodeToExpand, initialDepth, nodeToExpand.player1, usedHeuristic)
    print(f"Number of evaluated nodes: {evaluatedNodes} (for player {1 if nodeToExpand.player1 else 2})")

    # if no moves are found, the board is in a winning state (no moves left)
    if bestMove is None:
        return True, nodeToExpand, evaluatedNodes

    return isWinningMove, bestMove, evaluatedNodes