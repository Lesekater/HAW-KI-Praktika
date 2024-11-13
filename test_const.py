from typing import List
import copy

from const import Board, EPiece
from heuristics import countOfPieces, countOfDames
from main import main, makeMove

####################################
## Test board implementation
####################################

board = Board.fromIntList([
    # 0                     7
    # |------- X-Axis -------|    _
        [0, 1, 0, 1, 0, 1, 0, 1], # | 0
        [1, 0, 1, 0, 1, 0, 1, 0], # |
        [0, 1, 0, 1, 0, 1, 0, 1], # |
        [0, 0, 0, 0, 0, 0, 0, 0], # Y-Axis
        [0, 0, 0, 0, 0, 0, 0, 0], # |
        [2, 0, 2, 0, 2, 0, 2, 0], # |
        [0, 2, 0, 2, 0, 2, 0, 2], # |
        [2, 0, 2, 0, 2, 0, 2, 0]  # | 7
                                # -
    ])
board.player1 = True

def test_board():
    board = Board([
        [EPiece.EMPTY, EPiece.EMPTY, EPiece.EMPTY],
        [EPiece.EMPTY, EPiece.EMPTY, EPiece.EMPTY],
        [EPiece.EMPTY, EPiece.EMPTY, EPiece.EMPTY]])
    board.player1 = True

    # assert
    assert board.data == Board.fromIntList([[0, 0, 0], [0, 0, 0], [0, 0, 0]]).data

def test_board_swap():
    test_board = Board.fromIntList([
        [1, 2, 3],
        [4, 4, 4],
        [4, 4, 4]
    ])
    
    newBoard = test_board.swap(0, 0, 1, 0)

    # assert
    assert newBoard.data == Board.fromIntList([
        [2, 1, 3],
        [4, 4, 4],
        [4, 4, 4]
    ]).data