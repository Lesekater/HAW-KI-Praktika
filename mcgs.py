import random
from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

initialDepth = 10

def makeRandomMoves(node: Board, timout: int = 200) -> bool:
    isWinning = False
    move = 0
    while not isWinning and move < timout:
        possibleMoves, isWinning = getMoves(node, node.player1)
        if not possibleMoves:
            return isWinning
        node = random.choice(possibleMoves)
        move += 1
    return isWinning

## return how many times the board is randomly won
def simulatePlays(node: Board, times: int) -> float:
    wins = 0
    for i in range(times):
        if i == 0:
            print(f"Simulating game {i+1}/{times}")
        else:
            print(CURSOR_UP_ONE + ERASE_LINE + f"Simulating game {i+1}/{times}")
        if makeRandomMoves(node):
            wins += 1
    return wins

def mcgs(node: Board) -> Tuple[bool, Board]:
    possibleMoves, isWinningMove = getMoves(node, node.player1)
    if not possibleMoves:
        return True, None
    
    bestMove = None
    bestScore = -1

    for i, move in enumerate(possibleMoves):
        # if i == 0:
        #     # print(f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
        # else:
        #     # print(CURSOR_UP_ONE + ERASE_LINE + f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
        score = simulatePlays(move, 100)
        if score > bestScore:
            bestScore = score
            bestMove = move

    return isWinningMove, bestMove

def makeMove(nodeToExpand: Board) -> Tuple[bool, Board, int]:
    global initialDepth, evaluatedNodes
    initialDepth = 5
    evaluatedNodes = 0  # Reset the counter before starting the minimax
    isWinningMove, bestMove = mcgs(nodeToExpand)

    # if no moves are found, the board is in a winning state (no moves left)
    if bestMove is None:
        return True, nodeToExpand

    return isWinningMove, bestMove