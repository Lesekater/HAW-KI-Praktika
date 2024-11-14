import copy
import sys
from const import Board, EPiece
from typing import List, Tuple
from enum import Enum

from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves
from util import formatBoard

# testBoard1 = Board.fromIntList([
#     [1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [2, 0, 2, 0, 2, 0, 2, 0],
#     [0, 2, 0, 2, 0, 2, 0, 2]])

# testBoard1 = Board.fromIntList([
#     [1, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 2]])

testBoard1 = Board.fromIntList([
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 2]])

# testBoard1 = Board.fromIntList([
#     [1, 0, 1, 0, 1],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [2, 0, 2, 0, 2],
#     [0, 2, 0, 2, 0]])

def main(openList: List[Board] = [testBoard1],
         closedList: List[Board] = [], 
         usedHeuristic: heurisitcTypes = heurisitcTypes.CountOfPiecesAtEndOfBoard
         ) -> Tuple[bool, List[Board], List[Board]]:
    foundGoal = False
    initalBoard = copy.copy(openList[0])

    # increase recursion limit
    # print(print(sys.getrecursionlimit()))
    sys.setrecursionlimit(2000)

    while not foundGoal and len(openList) > 0:
        # i += 1
        nodeToExpand = openList.pop()
        (foundGoal, winningBoard) = makeMove(nodeToExpand, openList, closedList, usedHeuristic)

        print("Latest board:")
        print("position in tree: " + str(nodeToExpand.g))
        print("size ol: " + str(len(openList)) + " size cl: " + str(len(closedList)))
        print(formatBoard(nodeToExpand))

    if foundGoal:
        print("\n")
        print("Goal found!")
        print(formatBoard(winningBoard))
        print("Total moves: " + str(winningBoard.g))
        print ("Full Game: ")
        print("---END---")
        while winningBoard.parent is not None and winningBoard.g != 0.0:
            print(formatBoard(winningBoard))
            winningBoard = winningBoard.parent
        print(formatBoard(initalBoard))
        print("---START---")
    else:
        print("Goal not found!")

    return foundGoal, openList, closedList

def makeMove(nodeToExpand: Board, 
             openList: List[Board], 
             closedList: List[Board],
             usedHeuristic: heurisitcTypes = heurisitcTypes.CountOfPieces
             ) -> Tuple[bool, Board]:
    (possibleMoves, isWinningMove) = getMoves(
        board=nodeToExpand, player1=nodeToExpand.player1
    )

    if isWinningMove:
        # found goal
        winningBoard = possibleMoves[0]
        winningBoard.parent = nodeToExpand
        return True, winningBoard

    for move in possibleMoves:
        move.player1 = not nodeToExpand.player1
        move.parent = nodeToExpand

        # calculate g
        move.g = nodeToExpand.g + 1

        # calculate f
        heuristic = calculateHeuristic(move, usedHeuristic)
        move.f = move.g + heuristic

        # check open list
        for openNode in openList:
            if move.g == openNode.g and move.f > openNode.f:
                continue

        # check closed list
        for closedNode in closedList:
            if move.g == closedNode.g and move.f > closedNode.f:
                continue

        # add to open list at position relative to f
        openList.append(move)
        openList.sort(key=lambda x: x.f)

    closedList.append(nodeToExpand)

    # did not find goal
    return False, None   

if __name__ == "__main__":
    main()