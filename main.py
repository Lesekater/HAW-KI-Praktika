import copy
import signal
import sys
from uuid import UUID
import uuid
from typing import List, Tuple
from enum import Enum

from algorithm import makeMove
from minimax import makeMove as makeMMMove
from minimax_abp import makeMove as makeMMABP
from const import Board, EPiece, testBoard1, testBoards
from heuristics import calculateHeuristic, heurisitcTypes
from piece import checkForWinningBoard
from util import convertPiecesToEmoji, formatBoard, formatBoardWithCoords, printWinningPath, writeMiniMaxStatsToCSV, writeStatsToFile
from main_a_star import main as main_a_star
from main_minimax import main as main_minimax
from main_mcgs import main as main_mcgs

usedAlgorithm = None

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

def checkForHeuristicValidity(heuristic):
    # check if heuristic is valid & implemented
        if int(heuristic) >= len(heurisitcTypes) or calculateHeuristic(testBoard1, heurisitcTypes(int(heuristic))) == "unimplemented":
            print("Heuristic not implemented or invalid.")
            sys.exit(1)

def runMain(algorithm: int, board_number: int, heuristic1: int, heuristic2: int, debug: bool):
    if (algorithm == 1): # minimax without alpha beta pruning
        main_minimax(makeMMMove, testBoards[board_number], heurisitcTypes(heuristic1), heurisitcTypes(heuristic2), debug=debug)
    elif (algorithm == 2): # minimax with alpha beta pruning
        print("inital board: " + str(testBoards[board_number]))
        main_minimax(makeMMABP, testBoards[board_number], heurisitcTypes(heuristic1), heurisitcTypes(heuristic2), debug=debug)
    elif (algorithm == 3): # a*
        main_a_star([testBoards[board_number]], [], heurisitcTypes(heuristic1), heurisitcTypes(heuristic2), debug=debug)
    elif (algorithm == 4): # mcgs
        main_mcgs(makeMove, testBoards[board_number], debug=debug)

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
            runMain(int(sys.argv[5]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), debug)
        else:
            runMain(int(sys.argv[4]), int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), debug)
        sys.exit(0)

    print("Choose mode to start (1: interactive, 2: automatic):")
    mode = input("Enter mode: ")
    if mode == "1":
        interactiveMain()
    else:
        debug = input("Enable debug mode? (y/n): ") == "y"
        print("Choose algorithm to use (1: minimax, 2: minimax with alpha beta pruning, 3: a*, 4: mcgs):")
        algorithm = input("Enter algorithm: ")
        if int(algorithm) < 1 or int(algorithm) > 4:
            print("Invalid algorithm.")
            sys.exit(1)

        heuristic1 = -1
        if int(algorithm) != 4:
            print("Choose heuristic to use for Player 1 (colors: " + convertPiecesToEmoji(EPiece.DEFAULT_P1.value) + ", " + convertPiecesToEmoji(EPiece.DAME_P1.value) + "):")
            for i, heuristic in enumerate(heurisitcTypes):
                print(str(i) + ": " + heuristic.name)
            heuristic1 = input("Enter heuristic: ")
            checkForHeuristicValidity(heuristic1)

        heuristic2 = -1
        if int(algorithm) != 4:
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

        runMain(int(algorithm), int(board), int(heuristic1), int(heuristic2), debug)
