from typing import List
import copy

from const import Board, EPiece
from piece import Direction, contentOfDiagonals, getDiagonalContent 
from util import formatBoard

def test_contentOfDiagonals():
    testBoard = Board([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1]])
    
    result = contentOfDiagonals(testBoard, Direction.Down_Right, 0, 0)

    # assert
    assert result == [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]

    testBoard = Board([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 4, 1],
                       [1, 2, 1, 3, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [2, 1, 1, 1, 2, 1]])
    
    result = contentOfDiagonals(testBoard, Direction.Down_Right, 2, 3)
    result_2 = contentOfDiagonals(testBoard, Direction.Up_Left, 2, 3)
    result_3 = contentOfDiagonals(testBoard, Direction.Down_Left, 2, 3)
    result_4 = contentOfDiagonals(testBoard, Direction.Up_Right, 2, 3)

    # assert
    assert result == [EPiece.DEFAULT_P1, EPiece.DEFAULT_P2]
    assert result_2 == [EPiece.DEFAULT_P2, EPiece.DEFAULT_P1]
    assert result_3 == [EPiece.DEFAULT_P1, EPiece.DEFAULT_P2]
    assert result_4 == [EPiece.DAME_P1, EPiece.DAME_P2, EPiece.DEFAULT_P1]

def test_getDiagonalContent():
    testBoard = Board([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1]])
    
    result = getDiagonalContent(testBoard, [Direction.Down_Right], 0, 0)

    # assert
    assert result == {Direction.Down_Right: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]}

    testBoard = Board([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 4, 1],
                       [1, 2, 1, 3, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [2, 1, 1, 1, 2, 1]])
    
    result = getDiagonalContent(testBoard, [Direction.Down_Right, Direction.Up_Left, Direction.Down_Left, Direction.Up_Right], 2, 3)

    # assert
    assert result == {Direction.Down_Right: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P2],
                      Direction.Up_Left: [EPiece.DEFAULT_P2, EPiece.DEFAULT_P1],
                      Direction.Down_Left: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P2],
                      Direction.Up_Right: [EPiece.DAME_P1, EPiece.DAME_P2, EPiece.DEFAULT_P1]}