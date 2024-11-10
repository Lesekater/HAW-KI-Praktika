from typing import List
from const import Board
from main import main, countOfPieces, makeMove
import copy

board = Board([
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0]
])

def test_expandLastNode(mocker):
    # mocker.patch('main.openList', [board])
    mocker.patch('main.getMoves', return_value=([board], True))

    (foundGoal, openList, closedList) = main([board], [])

    # assert
    assert len(openList) == 0
    assert len(closedList) == 0
    assert foundGoal is True

def test_noGoalFound(mocker):
    # mocker.patch('main.openList', [board])
    mocker.patch('main.getMoves', return_value=([], False))

    (foundGoal, openList, closedList) = main([board], [])

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
            
    mocker.patch('main.getMoves', return_value=([board1], True))

    (foundGoal, openList, closedList) = main(openListMock, [])

    # assert
    assert len(openList) == 2
    assert openList[0].f == 2
    assert openList[1].f == 1

def test_countPiecesHeuristic():
    testBoard = Board([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    testBoard.player1 = True
    testBoard2 = Board([[2, 2, 2], [2, 2, 2], [2, 2, 2]])
    testBoard2.player1 = False
    testBoard3 = Board([[1, 1, 1], [1, 2, 2], [3, 3, 3]])
    testBoard3.player1 = True

    result = countOfPieces(testBoard)
    result2 = countOfPieces(testBoard2)
    result3 = countOfPieces(testBoard3)
    
    # assert
    assert result == 9
    assert result2 == 9
    assert result3 == 4

def test_hardcodedGame(mocker):

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

    def mockHeuristic(board):
        if board.id == bL.id:
            return heuristic_bL
        if board.id == bL1.id:
            return heuristic_bL1
        if board.id == bR.id:
            return heuristic_bR
        if board.id == bR1.id:
            return heuristic_bR1
        print("Error: Board not found")

    mocker.patch('main.calculateHeuristic', mockHeuristic)

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

    mocker.patch('main.getMoves', mockGetMoves)

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

