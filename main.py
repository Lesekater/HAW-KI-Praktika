from const import Board, EPiece
from typing import List, Tuple
from enum import Enum

from piece import getMoves

# openList: List[Board] = []
# closedList: List[Board] = []

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

def main(openList: List[Board] = [], closedList: List[Board] = []):
    foundGoal = False

    while not foundGoal and len(openList) > 0:
        nodeToExpand = openList.pop()
        (foundGoal, winningBoard) = makeMove(nodeToExpand, openList, closedList)

    if foundGoal:
        print("Goal found!")
        print(formatBoard(winningBoard))
        print("Total moves: " + str(winningBoard.g))
        print ("Full Game: ")
        while winningBoard.parent is not None and winningBoard.g != 0.0:
            print(formatBoard(winningBoard))
            winningBoard = winningBoard.parent
    else:
        print("Goal not found!")

    return foundGoal, openList, closedList

def makeMove(nodeToExpand: Board, 
             openList: List[Board], 
             closedList: List[Board]
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
        heuristic = calculateHeuristic(move)
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
