from const import Board, EPiece
from typing import List
from enum import Enum

from piece import getMoves

openList: List[Board] = []
closedList: List[Board] = []

class heurisitcTypes(Enum):
    CountOfPieces = 0
    CountOfDames = 1
    CountOfPiecesAndDames = 2
    CountOfPiecesToEliminate = 3
    CountOfPiecesAtEndOfBoard = 4
    ProgressPiecesOnBoard = 5
    CountOfPicesNotInDraw = 6
    Random = 7

usedHeuristic = heurisitcTypes.CountOfPieces

def main():
    foundGoal = False

    while not foundGoal and len(openList) > 0:
        nodeToExpand = openList.pop()

        (possibleMoves, isWinningMove) = getMoves(
            board=nodeToExpand, player1=nodeToExpand.player1
        )

        if isWinningMove:
            foundGoal = True
            break

        for move in possibleMoves:
            newBoard = Board(move)
            newBoard.player1 = not nodeToExpand.player1

            # calculate g
            newBoard.g = nodeToExpand.g + 1

            # calculate f
            heristic = calculateHeuristic(newBoard)
            newBoard.f = newBoard.g + heristic

            # check open list
            for openNode in openList:
                if newBoard.g == openNode.g and newBoard.f > openNode.f:
                    continue

            # check closed list
            for closedNode in closedList:
                if newBoard.g == closedNode.g and newBoard.f > closedNode.f:
                    continue

            # add to open list at position relative to f
            openList.append(newBoard)
            openList.sort(key=lambda x: x.f)

        closedList.append(nodeToExpand)

    if foundGoal:
        print("Goal found!")
        print(formatBoard(nodeToExpand))
    else:
        print("Goal not found!")

    return foundGoal, openList, closedList


def calculateHeuristic(board: Board) -> float:
    match usedHeuristic:
        case heurisitcTypes.CountOfPieces:
            return countOfPieces(board)
        # case heurisitcTypes.CountOfDames:
        #     return countOfDames(board)
        # case heurisitcTypes.CountOfPiecesAndDames:
        #     return countOfPiecesAndDames(board)
        # case heurisitcTypes.CountOfPiecesToEliminate:
        #     return countOfPiecesToEliminate(board)
        # case heurisitcTypes.CountOfPiecesAtEndOfBoard:
        #     return countOfPiecesAtEndOfBoard(board)
        # case heurisitcTypes.ProgressPiecesOnBoard:
        #     return progressPiecesOnBoard(board)
        # case heurisitcTypes.CountOfPicesNotInDraw:
        #     return countOfPicesNotInDraw(board)
        # case heurisitcTypes.Random:
        #     return random(board)
        case _:
            return 0.0

def countOfPieces(board: Board) -> float:
    currentPlayer = board.player1
    count = 0
    for row in board.data:
        for piece in row:
            if piece == EPiece.DEFAULT_P1.value and currentPlayer:
                count += 1
            elif piece == EPiece.DEFAULT_P2.value and not currentPlayer:
                count += 1

    return count        

def formatBoard(board: Board) -> str:
    formattedBoard = ""
    for row in board.data:
        formattedBoard += str(row) + "\n"
    return formattedBoard
