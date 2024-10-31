from const import Board, EPiece
from typing import List

from piece import getMoves

openList: List[Board] = []
closedList: List[Board] = []


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
    # TODO: Implement
    return 0.0


def formatBoard(board: Board) -> str:
    formattedBoard = ""
    for row in board.data:
        formattedBoard += str(row) + "\n"
    return formattedBoard
