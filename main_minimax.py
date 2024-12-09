import signal
import sys
from typing import Callable, List, Tuple
import uuid

from const import Board, testBoard1
from heuristics import heurisitcTypes
from util import formatBoard, writeMiniMaxStatsToCSV, writeStatsToFile, signal_handler, signalCtlC

def main(algorithm: Callable[[Board, heurisitcTypes], Tuple[bool, Board, int]],
        initalBoard: Board = testBoard1,
         usedHeuristicPlayer1: heurisitcTypes = heurisitcTypes.CountOfPieces,
         usedHeuristicPlayer2: heurisitcTypes = heurisitcTypes.CountOfPieces,
         debug: bool = False) -> bool:
    foundGoal = False

    # increase recursion limit
    # print(print(sys.getrecursionlimit()))
    sys.setrecursionlimit(2000)

    # register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    runId: int = uuid.uuid4()

    checkedBoards = 0
    nextBoard = initalBoard

    while not foundGoal and nextBoard is not None:
        nodeToExpand = nextBoard
        nextBoard = None
        usedHeuristic = usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2

        # # check for stalemate
        # if nodeToExpand.g > 150 or checkForStaleMateByRepetition(nodeToExpand):
        #     print("Stalemate detected!")
        #     break
        
        # expand node
        heuristic = usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2
        (foundGoal, winningBoard, evaluatedNodes) = algorithm(nodeToExpand, heuristic)

        # append board to closed list
        # and flip player and add to open list
        winningBoard.player1 = not winningBoard.player1
        checkedBoards += 1
        nextBoard = winningBoard

        # type in string
        type = "minimax" if algorithm.__name__ == "minimax" else "minimax_abp"
        type = str(runId) + "_" + type
        writeMiniMaxStatsToCSV(type, nodeToExpand.player1, heuristic, evaluatedNodes, winningBoard.g)

        if debug:
            # print("Player 1 (⚫, 🔴): " + usedHeuristicPlayer1.name)
            # print("Player 2 (⚪, 🔵): " + usedHeuristicPlayer2.name)
            print("Latest board:")
            print("position in tree: " + str(nodeToExpand.g))
            print("checked boards: " + str(checkedBoards))
            print(formatBoard(nodeToExpand, True, usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2))

        # on ctl+c print winning path
        if signalCtlC:
            return foundGoal

    if foundGoal:
        print("Goal found!")
        writeStatsToFile(winningBoard, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)
    else:
        print("Goal not found!")
        print("Game up to now:")
        writeStatsToFile(nodeToExpand, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)

    return foundGoal