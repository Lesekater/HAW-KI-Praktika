import copy
import signal
import sys
from typing import List, Tuple
import uuid

from algorithm import makeMove, checkForStaleMateByRepetition
from const import Board, testBoard1
from heuristics import heurisitcTypes
from util import formatBoard, printWinningPath, writeStatsToFile, signal_handler, signalCtlC

def main(openList: List[Board] = [testBoard1],
         closedList: List[Board] = [], 
         usedHeuristicPlayer1: heurisitcTypes = heurisitcTypes.CountOfPieces,
         usedHeuristicPlayer2: heurisitcTypes = heurisitcTypes.CountOfPieces,
         debug: bool = False) -> Tuple[bool, List[Board], List[Board]]:
    foundGoal = False
    highestG = 0
    initalBoard = copy.copy(openList[0])

    # increase recursion limit
    # print(print(sys.getrecursionlimit()))
    sys.setrecursionlimit(2000)

    # register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    runId: int = uuid.uuid4()

    while not foundGoal and len(openList) > 0:
        nodeToExpand = openList.pop()
        usedHeuristic = usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2

        # check for stalemate
        if nodeToExpand.g > 150 or checkForStaleMateByRepetition(nodeToExpand):
            print("Stalemate detected!")
            break
        
        # expand node
        (foundGoal, winningBoard) = makeMove(nodeToExpand, openList, closedList, usedHeuristic)

        highestG = max(highestG, nodeToExpand.g)

        if debug:
            # print("Player 1 (⚫, 🔴): " + usedHeuristicPlayer1.name)
            # print("Player 2 (⚪, 🔵): " + usedHeuristicPlayer2.name)
            print("Latest board:")
            print("position in tree: " + str(nodeToExpand.g) + " (current highest: " + str(highestG) + ")")
            print("size ol: " + str(len(openList)) + " size cl: " + str(len(closedList)))
            print(formatBoard(nodeToExpand, True, usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2))

        # on ctl+c print winning path
        if signalCtlC:
            winningBoard = nodeToExpand
            printWinningPath(winningBoard, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)
            return foundGoal, openList, closedList

    if foundGoal:
        print("Goal found!")
        printWinningPath(winningBoard, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)
        writeStatsToFile(winningBoard, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)
    else:
        print("Goal not found!")
        print("Game up to now:")
        printWinningPath(nodeToExpand, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)
        writeStatsToFile(nodeToExpand, initalBoard, usedHeuristicPlayer1, usedHeuristicPlayer2)

    return foundGoal, openList, closedList