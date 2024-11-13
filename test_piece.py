from typing import List
import copy

from const import Board, EPiece
from piece import Direction, contentOfDiagonals, getDiagonalContent, getMovesForPosition, getMoves
from util import formatBoard

def test_contentOfDiagonals():
    testBoard = Board.fromIntList([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1]])
    
    result = contentOfDiagonals(testBoard, Direction.Down_Right, 0, 0)

    # assert
    assert result == [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]

    testBoard = Board.fromIntList([[1, 1, 1, 1, 1, 1],
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
    testBoard = Board.fromIntList([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1]])
    
    result = getDiagonalContent(testBoard, [Direction.Down_Right], 0, 0)

    # assert
    assert result == {Direction.Down_Right: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]}

    testBoard = Board.fromIntList([[1, 1, 1, 1, 1, 1],
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
    
    ## test with unporportional board
    testBoard = Board.fromIntList([[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1]])
    
    testBoard2 = Board.fromIntList([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])
    
    result = getDiagonalContent(testBoard, [Direction.Down_Right], 3, 0)
    result2 = getDiagonalContent(testBoard2, [Direction.Down_Right], 0, 3)

    # assert
    assert result == {Direction.Down_Right: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]}
    assert result2 == {Direction.Down_Right: [EPiece.DEFAULT_P1, EPiece.DEFAULT_P1]}

####################################
## moving pieces
####################################

def test_getMovesForPosition_simple():
    testBoard = Board.fromIntList([[1, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]])
    
    result = getMovesForPosition(testBoard, 0, 0)

    # assert
    assert result == [Board.fromIntList([[0, 0, 0],
                                        [0, 1, 0],
                                        [0, 0, 0]])]

def test_getMovesForPosition_invalid():
    testBoard = Board.fromIntList([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 1]])
    
    result = getMovesForPosition(testBoard, 2, 2)

    # assert
    assert result == []
    
def test_getMovesForPosition_strike():
    testBoard = Board.fromIntList([[1, 0, 0],
                                [0, 2, 0],
                                [0, 0, 0]])
    
    result = getMovesForPosition(testBoard, 0, 0)

    # assert
    assert result == [Board.fromIntList([[0, 0, 0],
                                        [0, 0, 0],
                                        [0, 0, 1]])]
    
def test_getMovesForPosition_dame():
    testBoard = Board.fromIntList([[0, 0, 0],
                                [0, 3, 0],
                                [0, 0, 0]])
    
    result = getMovesForPosition(testBoard, 1, 1)

    # assert
    board1 = Board.fromIntList([[3, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]])
    board2 = Board.fromIntList([[0, 0, 3],
                                [0, 0, 0],
                                [0, 0, 0]])
    board3 = Board.fromIntList([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 3]])
    board4 = Board.fromIntList([[0, 0, 0],
                                [0, 0, 0],
                                [3, 0, 0]])
    
    assert result == [board1, board2, board3, board4]

def test_getMovesForPosition_dame_strike():
    testBoard = Board.fromIntList([[3, 0, 0],
                                [0, 2, 0],
                                [0, 0, 0]])
    
    result = getMovesForPosition(testBoard, 0, 0)

    # assert
    board1 = Board.fromIntList([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 3]])
    
    assert result == [board1]

####################################
## moving pieces -- multiple moves
####################################

# def test_getMoves_simple():
#     testBoard = Board.fromIntList([[0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [1, 0, 1, 0, 1]])
    
#     result = getMoves(testBoard, False)

#     # assert
#     board1 = Board.fromIntList([[0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 1, 0, 0, 0],
#                                 [0, 0, 1, 0, 1]])
    
#     board2 = Board.fromIntList([[0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 1, 0, 0, 0],
#                                 [1, 0, 0, 0, 1]])
    
#     board3 = Board.fromIntList([[0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 1, 0],
#                                 [1, 0, 0, 0, 1]])
    
#     board4 = Board.fromIntList([[0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 0, 0],
#                                 [0, 0, 0, 1, 0],
#                                 [1, 0, 1, 0, 0]])
    
#     assert result == [board1, board2, board3, board4]
