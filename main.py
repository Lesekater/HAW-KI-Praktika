import copy
import signal
import sys
from algorithm import makeMove
from const import Board, EPiece
from typing import List, Tuple
from enum import Enum

from heuristics import calculateHeuristic, heurisitcTypes
from piece import checkForWinningBoard
from util import convertPiecesToEmoji, formatBoard, formatBoardWithCoords, printWinningPath, writeStatsToFile

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
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 2]])

testBoard3 = Board.fromIntList([
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 2]])

testBoard4 = Board.fromIntList([
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0],
    [2, 0, 2, 0, 2]])

testBoard5 = Board.fromIntList([
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 2, 0, 2],
    [2, 0, 2, 0]])

testBoards = [testBoard1, testBoard2, testBoard3, testBoard4, testBoard5]

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
            print("Latest board:")
            print("position in tree: " + str(nodeToExpand.g) + " (current highest: " + str(highestG) + ")")
            print("size ol: " + str(len(openList)) + " size cl: " + str(len(closedList)))
            print(formatBoard(nodeToExpand))

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

def checkForHeuristicValidity(heuristic):
    # check if heuristic is valid & implemented
        if int(heuristic) >= len(heurisitcTypes) or calculateHeuristic(testBoard1, heurisitcTypes(int(heuristic))) == "unimplemented":
            print("Heuristic not implemented or invalid.")
            sys.exit(1)

if __name__ == "__main__":
    debug = False

    # skip via arguments
    if len(sys.argv) > 1:
        # if first argument is help output possible args
        if sys.argv[1] == "help":
            print("Usage: python3 main.py [board number] [heuristic1] [heuristic2] or just python3 main.py for interactive mode.")
            print("Use --debug flag to enable debug mode.")
        elif sys.argv[1] == "--debug":
            debug = True
            main([testBoards[int(sys.argv[2])]], [], heurisitcTypes(int(sys.argv[3])), heurisitcTypes(int(sys.argv[4])), debug=debug)
        else:
            main([testBoards[int(sys.argv[1])]], [], heurisitcTypes(int(sys.argv[2])), heurisitcTypes(int(sys.argv[3])), debug=debug)
        sys.exit(0)

    print("Choose mode to start (1: interactive, 2: automatic):")
    mode = input("Enter mode: ")
    if mode == "1":
        interactiveMain()
    else:
        print("Choose heuristic to use for Player 1 (colors: " + convertPiecesToEmoji(EPiece.DEFAULT_P1.value) + ", " + convertPiecesToEmoji(EPiece.DAME_P1.value) + "):")
        for i, heuristic in enumerate(heurisitcTypes):
            print(str(i) + ": " + heuristic.name)
        heuristic1 = input("Enter heuristic: ")
        checkForHeuristicValidity(heuristic1)

        print("Choose heuristic to use for Player 2 (colors: " + convertPiecesToEmoji(EPiece.DEFAULT_P2.value) + ", " + convertPiecesToEmoji(EPiece.DAME_P2.value) + "):")
        for i, heuristic in enumerate(heurisitcTypes):
            print(str(i) + ": " + heuristic.name)
        heuristic2 = input("Enter heuristic: ")
        checkForHeuristicValidity(heuristic2)

        # choose test board
        print("Choose test board to use.")
        for i, board in enumerate(testBoards):
            print(str(i) + ": \n" + formatBoard(board))
        board = input("Enter board: ")

        main([testBoards[int(board)]], [], heurisitcTypes(int(heuristic1)), heurisitcTypes(int(heuristic2)), debug=True)
