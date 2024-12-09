from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

def makeMove(nodeToExpand: Board, 
             openList: List[Board], 
             closedList: List[Board],
             usedHeuristic: heurisitcTypes = heurisitcTypes.CountOfPieces
             ) -> tuple[Board, bool]:
    (possibleMoves, isWinningMove) = getMoves(board=nodeToExpand, player1=nodeToExpand.player1)

    if isWinningMove:
        return isWinningMove, possibleMoves[0]

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
        openList.sort(key=lambda x: x.f, reverse=True)

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