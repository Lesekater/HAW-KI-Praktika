from typing import List
import copy

from const import Board, EPiece
from heuristics import countOfPieces, countOfDames, countOfPiecesToEliminate
from piece import contentOfDiagonals, Direction
from main import main, makeMove

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