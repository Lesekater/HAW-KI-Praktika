import random
from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves
import uuid
import json
import os
import time

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

initialDepth = 10

def makeRandomMoves(node: Board, timeout: int = 200) -> bool:
    isWinning = False
    move = 0
    while not isWinning and (move < timeout or timeout == -1):
        possibleMoves, isWinning = getMoves(node, node.player1)
        if not possibleMoves:
            return isWinning
        node = random.choice(possibleMoves)
        node.player1 = not node.player1
        move += 1

        # cache the moves with scores in files
        # training_data/<timestamp>/uuid.json
        if (node.player1):
            for i, tempmove in enumerate(possibleMoves):
                tempmove = tempmove.toIntList()
                score = -1
                # print(f"Move {i+1}/{len(possibleMoves)}: {score}")

                # create folder if not exists
                os.makedirs("training_data", exist_ok=True)
                # create subfolder with timestamp (only day-precision)
                timestamp = time.strftime("%Y-%m-%d")
                os.makedirs(f"training_data/{timestamp}-{len(tempmove)}", exist_ok=True)

                # save to file
                filename = f"training_data/{timestamp}-{len(tempmove)}/{uuid.uuid4()}.json"
                with open(filename, "w") as f:
                    json.dump({"move": tempmove, "score": score}, f)
    return isWinning

## return how many times the board is randomly won
def simulatePlays(node: Board, times: int, move: int) -> int:
    wins = 0
    for i in range(times):
        if i == 0:
            print(f"{move} Simulating game {i+1}/{times}")
        else:
            print(CURSOR_UP_ONE + ERASE_LINE + f"{move} Simulating game {i+1}/{times}")
        if makeRandomMoves(node): ## set to -1 to disable timeout
            wins += 1
    return wins

def mcgs(node: Board) -> Tuple[bool, Board]:
    possibleMoves, isWinningMove = getMoves(node, node.player1)
    if not possibleMoves:
        return True, None
    
    bestMove = None
    bestScore = -1
    
    moves_with_scores = []

    i = 0
    move = possibleMoves[0]
    # print(f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
    # else:
    #     # print(CURSOR_UP_ONE + ERASE_LINE + f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
    score = simulatePlays(move, 100, i)

    moves_with_scores.append((move.toIntList(), score))

    bestScore = score
    bestMove = move

    # for i, move in enumerate(possibleMoves):
    #     if i == 0:
    #         print("Possible moves: ", len(possibleMoves))
    #         # print(f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
    #     # else:
    #     #     # print(CURSOR_UP_ONE + ERASE_LINE + f"Checking move {i+1}/{len(possibleMoves)} (possible moves)")
    #     score = simulatePlays(move, 100, i)

    #     moves_with_scores.append((move.toIntList(), score))

    #     print(f"Score: {score}")
    #     if score > bestScore:
    #         bestScore = score
    #         bestMove = move

    # cache the moves with scores in files
    # training_data/<timestamp>/uuid.json
    if (node.player1):
        for i, (move, score) in enumerate(moves_with_scores):
            print(f"Move {i+1}/{len(moves_with_scores)}: {score}")

            # create folder if not exists
            os.makedirs("training_data", exist_ok=True)
            # create subfolder with timestamp (only day-precision)
            timestamp = time.strftime("%Y-%m-%d")
            os.makedirs(f"training_data/{timestamp}-{len(move)}", exist_ok=True)

            # save to file
            filename = f"training_data/{timestamp}-{len(move)}/{uuid.uuid4()}.json"
            with open(filename, "w") as f:
                json.dump({"move": move, "score": score}, f)

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