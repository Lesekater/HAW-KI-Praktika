from typing import List, Tuple
from const import Board
from heuristics import calculateHeuristic, heurisitcTypes
from piece import getMoves

def makeMove(nodeToExpand: Board, 
             openList: List[Board], 
             closedList: List[Board],
             usedHeuristic: heurisitcTypes = heurisitcTypes.CountOfPieces
             ) -> Board:
    possibleMoves = getMoves(board=nodeToExpand, player1=nodeToExpand.player1)

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