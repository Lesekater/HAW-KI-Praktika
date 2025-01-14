import signal
import sys
from typing import Callable, List, Tuple
import uuid
import numpy as np

from const import Board, testBoard1, EPiece
from heuristics import heurisitcTypes
from util import formatBoard, writeMiniMaxStatsToCSV, writeStatsToFile, signal_handler, signalCtlC, writeStatsToCSV

from piece import getMoves
import tensorflow as tf
from tensorflow import keras

def main(algorithm: Callable[[Board, heurisitcTypes], Tuple[bool, Board, int]],
        initalBoard: Board = testBoard1,
        debug: bool = False) -> bool:
    foundGoal = False
    draw = False

    # increase recursion limit
    # print(print(sys.getrecursionlimit()))
    sys.setrecursionlimit(2000)

    # register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    runId: int = uuid.uuid4()

    checkedBoards = 0
    nextBoard = initalBoard

    # load model
    model = keras.models.load_model("model_CountOfPiecesAndDames.keras")

    while not foundGoal and nextBoard is not None:
        nodeToExpand = nextBoard
        nextBoard = None

        # # check for stalemate
        # if nodeToExpand.g > 150 or checkForStaleMateByRepetition(nodeToExpand):
        #     print("Stalemate detected!")
        #     break
        
        # expand node
        possibleMoves, isWinningMove = getMoves(nodeToExpand, nodeToExpand.player1)
        if not possibleMoves:
            print("No possible moves left!")
            break
        
        scores = []
        # for player 2 predict random scores between 0 and 1
        if not nodeToExpand.player1:
            for board in possibleMoves:
                scores.append(np.random.rand())
        
        # for player 1 predict scores with model
        else:
            for board in possibleMoves:
                board_array = np.array(board.toIntList()).reshape((1, 8, 8))
                scores.append(model.predict(board_array)[0][0])
                print(scores[-1])

        winningBoard = None
        min = 10000
        for i in range(len(possibleMoves)):
            if scores[i] < min:
                min = scores[i]
                winningBoard = possibleMoves[i]

        # check if goal is reached
        if isWinningMove:
            foundGoal = True
            break

        # append board to closed list
        # and flip player and add to open list
        winningBoard.player1 = not winningBoard.player1
        checkedBoards += 1
        nextBoard = winningBoard

        # type in string
        # type = "minimax" if algorithm.__name__ == "minimax" else "minimax_abp"
        # type = str(runId) + "_" + type
        # writeMiniMaxStatsToCSV(type, nodeToExpand.player1, heuristic, evaluatedNodes, winningBoard.g)

        if True:
            # print("Player 1 (⚫, 🔴): " + usedHeuristicPlayer1.name)
            # print("Player 2 (⚪, 🔵): " + usedHeuristicPlayer2.name)
            print("Latest board:")
            print(formatBoard(winningBoard, True))
            print("move: " + str(checkedBoards))
            print("checked boards: " + str(checkedBoards))

        # on ctl+c print winning path
        if signalCtlC:
            return foundGoal

    if foundGoal:
        # if both players only have one dame left --> draw
        damesP1 = 0
        damesP2 = 0
        for row in winningBoard.toIntList():    
            for cell in row:
                if cell == EPiece.DAME_P1.value:
                    damesP1 += 1
                elif cell == EPiece.DAME_P2.value:
                    damesP2 += 1

        if damesP1 == 1 and damesP2 == 1:
            draw = True
            print("Draw detected!")

        print("Goal found!")
        print("winner: " + ("Draw" if draw else ("Player 1" if winningBoard.player1 else "Player 2")))
        writeStatsToFile(winningBoard, initalBoard, "", "")
        winningBoard.g = checkedBoards
        writeStatsToCSV(draw, winningBoard, initalBoard)
    else:
        print("Goal not found!")
        writeStatsToFile(nodeToExpand, initalBoard, "", "")

    return foundGoal