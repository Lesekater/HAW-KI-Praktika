import copy
import signal
import sys
from const import Board, EPiece
from typing import List, Tuple
from enum import Enum

from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves
from util import formatBoard, formatBoardWithCoords

signalCtlC = False

def signal_handler(sig, frame):
    global signalCtlC
    signalCtlC = True

testBoard1 = Board.fromIntList([
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2]])

testBoard2 = Board.fromIntList([
    [1, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 0, 2]])

testBoard3 = Board.fromIntList([
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 2]])

testBoard4 = Board.fromIntList([
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2],
    [0, 2, 0, 2, 0]])

testBoards = [testBoard1, testBoard2, testBoard3, testBoard4]

def main(openList: List[Board] = [testBoard1],
         closedList: List[Board] = [], 
         usedHeuristicPlayer1: heurisitcTypes = heurisitcTypes.CountOfPieces,
         usedHeuristicPlayer2: heurisitcTypes = heurisitcTypes.CountOfPieces
         ) -> Tuple[bool, List[Board], List[Board]]:
    foundGoal = False
    highestG = 0
    initalBoard = copy.copy(openList[0])

    # increase recursion limit
    # print(print(sys.getrecursionlimit()))
    sys.setrecursionlimit(2000)

    # register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    while not foundGoal and len(openList) > 0:
        nodeToExpand = openList.pop()
        usedHeuristic = usedHeuristicPlayer1 if nodeToExpand.player1 else usedHeuristicPlayer2
        (foundGoal, winningBoard) = makeMove(nodeToExpand, openList, closedList, usedHeuristic)
        highestG = max(highestG, nodeToExpand.g)

        # check for stalemate
        if nodeToExpand.g > 100 or checkForStaleMateByRepetition(nodeToExpand):
            print("Stalemate detected!")
            break

        print("Latest board:")
        print("position in tree: " + str(nodeToExpand.g) + " (current highest: " + str(highestG) + ")")
        print("size ol: " + str(len(openList)) + " size cl: " + str(len(closedList)))
        print(formatBoard(nodeToExpand))

        # on ctl+c print winning path
        if signalCtlC:
            winningBoard = nodeToExpand
            printWinningPath(winningBoard, initalBoard)
            return foundGoal, openList, closedList

    if foundGoal:
        print("Goal found!")
        printWinningPath(winningBoard, initalBoard)
    else:
        print("Goal not found!")
        print("Game up to now:")
        printWinningPath(nodeToExpand, initalBoard)

    return foundGoal, openList, closedList

def interactiveMain():
    openList = [testBoard1]
    closedList = []
    usedHeuristic = heurisitcTypes.CountOfPieces
    while True:
        userMove = letUserChooseMove(openList[0])
        userMove.player1 = not openList[0].player1
        userMove.parent = None
        openList = [userMove]
        # make 60 moves via ai and backtrack to the first move
        for i in range(0, 60):
            nodeToExpand = openList.pop()
            (foundGoal, winningBoard) = makeMove(nodeToExpand, openList, closedList, usedHeuristic)
            if foundGoal:
                break
        currentMove = openList[0]
        while currentMove.parent is not userMove:
            currentMove = currentMove.parent
        openList = [currentMove]

def letUserChooseMove(board: Board) -> Board:
    print("current Board:")
    print(formatBoardWithCoords(board))
    print("Choose a move:")
    print("Choose a piece to move:")
    x = input("Enter x: ")
    y = input("Enter y: ")
    print("Choose a target:")
    xTarget = input("Enter x: ")
    yTarget = input("Enter y: ")
    board = board.swap(int(x), int(y), int(xTarget), int(yTarget))

    # check if move was a strike
    if abs(int(x) - int(xTarget)) == 2:
        strikeX = (int(x) + int(xTarget)) // 2
        strikeY = (int(y) + int(yTarget)) // 2
        board = board.strikePiece(strikeX, strikeY)

    return board

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

def checkForStaleMateByRepetition(currentMove: Board) -> bool:
    hasStaleMate = False
    repeatedMove = 0
    # check if move has been repeated 2 times by the same player
    for i in range(1, 10):
        if currentMove.parent is None or currentMove.parent.parent is None \
            or currentMove.parent.parent.parent is None or currentMove.parent.parent.parent.parent is None:
            break
        if currentMove.player1:
            # check for every piece of player 1 if it has the same position has 4 moves ago
            for y in range(0, len(currentMove.data)):
                for x in range(0, len(currentMove.data[y])):
                    if currentMove.data[y][x] != currentMove.parent.parent.parent.parent.data[y][x]:
                        repeatedMove = 0
                        break
                    repeatedMove += 1
        else:
            # check for every piece of player 2 if it has the same position has 4 moves ago
            for y in range(0, len(currentMove.data)):
                for x in range(0, len(currentMove.data[y])):
                    if currentMove.data[y][x] != currentMove.parent.parent.parent.parent.data[y][x]:
                        repeatedMove = 0
                        break
                    repeatedMove += 1
        currentMove = currentMove.parent
    
    return repeatedMove == 2

def printWinningPath(winningBoard: Board, initalBoard: Board):
    print("\n")
    print("Total moves: " + str(winningBoard.g))
    print ("Full Game: ")
    print("---END---")
    while winningBoard.parent is not None and winningBoard.g != 0.0:
        print(formatBoard(winningBoard))
        winningBoard = winningBoard.parent
    print(formatBoard(initalBoard))
    print("---START---")

def checkForHeuristicValidity(heuristic):
    # check if heuristic is valid & implemented
        if int(heuristic) >= len(heurisitcTypes) or calculateHeuristic(testBoard1, heurisitcTypes(int(heuristic))) == "unimplemented":
            print("Heuristic not implemented or invalid.")
            sys.exit(1)

if __name__ == "__main__":
    print("Choose mode to start (1: interactive, 2: automatic):")
    mode = input("Enter mode: ")
    if mode == "1":
        interactiveMain()
    else:
        print("Choose heuristic to use for Player 1:")
        for i, heuristic in enumerate(heurisitcTypes):
            print(str(i) + ": " + heuristic.name)
        heuristic1 = input("Enter heuristic: ")
        checkForHeuristicValidity(heuristic1)

        print("Choose heuristic to use for Player 2:")
        for i, heuristic in enumerate(heurisitcTypes):
            print(str(i) + ": " + heuristic.name)
        heuristic2 = input("Enter heuristic: ")
        checkForHeuristicValidity(heuristic2)

        # choose test board
        print("Choose test board to use.")
        for i, board in enumerate(testBoards):
            print(str(i) + ": \n" + formatBoard(board))
        board = input("Enter board: ")

        main([testBoards[int(board)]], [], heurisitcTypes(int(heuristic1)), heurisitcTypes(int(heuristic2)))
