from typing import List
import copy

from const import Board, EPiece
from heuristics import countOfPieces, countOfDames
from main import main, makeMove

# Player1 is odd  numbers (1 and 3) (Black)
# Player2 is even numbers (2 and 4) (White)

# Player1 moves in positive direction (down)
# Player2 moves in negative direction (up)
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

####################################
## Test main algorithm
####################################

def test_expandLastNode(mocker):
    # mocker.patch('main.openList', [board])
    mocker.patch('algorithm.getMoves', return_value=([board], True))

    (foundGoal, openList, closedList) = main([board])

    # assert
    assert len(openList) == 0
    assert len(closedList) == 0
    assert foundGoal is True

def test_noGoalFound(mocker):
    # mocker.patch('main.openList', [board])
    mocker.patch('algorithm.getMoves', return_value=([], False))

    (foundGoal, openList, closedList) = main([board])

    # assert
    assert len(openList) == 0
    assert len(closedList) == 1
    assert foundGoal is False

def test_correctSortedList(mocker):
    board1 = copy.copy(board)
    board1.f = 2
    board2 = copy.copy(board)
    board2.f = 1
    board3 = copy.copy(board)
    board3.f = 0

    openListMock = [board1, board2, board3]
            
    mocker.patch('algorithm.getMoves', return_value=([board1], True))

    (foundGoal, openList, closedList) = main(openListMock)

    # assert
    assert len(openList) == 2
    assert openList[0].f == 2
    assert openList[1].f == 1

def test_hardcodedGame(mocker):

    # Tree representation:
    #   initalBoard
    #     /     \
    #    bL      bR
    #     |       |
    #    bL1     bR1

    # Heuristic values:
    #       1
    #     /    \
    #    1      1
    #    |      |
    #    0      0


    # hardcoded boards
    initalBoard = Board([])

    heuristic_bL = 1
    bL = Board([])
    
    heuristic_bL1 = 0
    bL1 = Board([])

    heuristic_bR = 1
    bR = Board([])

    heuristic_bR1 = 1
    bR1 = Board([])

    def mockHeuristic(board, _):
        if board.id == bL.id:
            return heuristic_bL
        if board.id == bL1.id:
            return heuristic_bL1
        if board.id == bR.id:
            return heuristic_bR
        if board.id == bR1.id:
            return heuristic_bR1
        print("Error: Board not found")

    mocker.patch('algorithm.calculateHeuristic', mockHeuristic)

    # hardcoded move results
    def mockGetMoves(board, player1):
        if board.id == initalBoard.id:
            return [bR, bL], False
        if board.id == bL.id:
            return [bL1], False
        if board.id == bL1.id:
            return [], False
        if board.id == bR.id:
            return [bR1], True
        print("Error: Board not found")

    mocker.patch('algorithm.getMoves', mockGetMoves)

    openList = [initalBoard]
    closedList: List[Board] = []
    hasWon = False

    while not hasWon:
        nodeToExpand = openList.pop()
        (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

    # assert
    assert hasWon is True
    assert len(openList) == 0
    assert closedList == [initalBoard, bL, bL1] # bR is not in closedList because the program exits before adding it

def test_hardcodedGame3(mocker):
        
        # Tree representation:
        #   initalBoard
        #     /     \
        #    bL      bR
        #   /  \      |
        # bLL  bLR   bR1
        #       |     |
        #      bLR1  bR2
        #             |
        #            bR3

        # Heuristic values:
        #       2
        #     /    \
        #    2      2
        #   /  \    |
        #  1    2   2
        #       |   |
        #       2   2
        #           |
        #           2


        # hardcoded boards
        initalBoard = Board([])
        
        heuristic_bL = 2
        bL = Board.fromIntList([[1]])

        heuristic_bLL = 1
        bLL = Board.fromIntList([[2]])

        heuristic_bLR = 2
        bLR = Board.fromIntList([[3]])

        herustic_bLR1 = 2
        bLR1 = Board.fromIntList([[4]])

        heuristic_bR = 2
        bR = Board.fromIntList([[1, 1]])

        heuristic_bR1 = 2
        bR1 = Board.fromIntList([[1, 2]])
        
        heuristic_bR2 = 2
        bR2 = Board.fromIntList([[1, 3]])

        heuristic_bR3 = 2
        bR3 = Board.fromIntList([[1, 4]])

        def mockHeuristic(board, _):
            if board.id == bL.id:
                return heuristic_bL
            if board.id == bLL.id:
                return heuristic_bLL
            if board.id == bLR.id:
                return heuristic_bLR
            if board.id == bLR1.id:
                return herustic_bLR1
            if board.id == bR.id:
                return heuristic_bR
            if board.id == bR1.id:
                return heuristic_bR1
            if board.id == bR2.id:
                return heuristic_bR2
            if board.id == bR3.id:
                return heuristic_bR3
            print("Error: Board not found")

        mocker.patch('algorithm.calculateHeuristic', mockHeuristic)

        # hardcoded move results
        def mockGetMoves(board, player1):
            if board.id == initalBoard.id:
                return [bR, bL], False
            if board.id == bL.id:
                return [bLL, bLR], False
            if board.id == bLL.id:
                return [], False
            if board.id == bLR.id:
                return [bLR1], False
            if board.id == bLR1.id:
                return [bLR1], True
            if board.id == bR.id:
                return [bR1], False
            if board.id == bR1.id:
                return [bR2], False
            if board.id == bR2.id:
                return [bR3], False
            if board.id == bR3.id:
                return [], False
            print("Error: Board not found")

        mocker.patch('algorithm.getMoves', mockGetMoves)

        openList = [initalBoard]
        closedList: List[Board] = []
        hasWon = False

        while not hasWon:
            nodeToExpand = openList.pop()
            (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

        # assert
        assert hasWon is True

        assert openList == [bR2]
        testClosed = [initalBoard, bL, bR, bR1, bR2, bLL, bLR]
        for board in closedList:
            assert board in testClosed, f"Board {board.data} not in testClosed"
####################################
## Test heuristics
####################################

# DEPRECATED: TODO: renew
# def test_countPiecesHeuristic():
#     testBoard = Board.fromIntList([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
#     testBoard.player1 = True
#     testBoard2 = Board.fromIntList([[2, 2, 2], [2, 2, 2], [2, 2, 2]])
#     testBoard2.player1 = False
#     testBoard3 = Board.fromIntList([[1, 1, 1], [1, 2, 2], [3, 3, 3]])
#     testBoard3.player1 = True

#     result = countOfPieces(testBoard)
#     result2 = countOfPieces(testBoard2)
#     result3 = countOfPieces(testBoard3)
    
#     # assert
#     assert result == 9
#     assert result2 == 9
#     assert result3 == 4

# def test_countOfDamesHeuristic():
#     testBoard = Board.fromIntList([[3, 3, 3], [3, 3, 3], [3, 3, 3]])
#     testBoard.player1 = True
#     testBoard2 = Board.fromIntList([[4, 4, 4], [4, 4, 4], [4, 4, 4]])
#     testBoard2.player1 = False
#     testBoard3 = Board.fromIntList([[3, 3, 3], [3, 4, 4], [1, 1, 1]])
#     testBoard3.player1 = True

#     result = countOfDames(testBoard)
#     result2 = countOfDames(testBoard2)
#     result3 = countOfDames(testBoard3)
    
#     # assert
#     assert result == 9
#     assert result2 == 9
#     assert result3 == 4