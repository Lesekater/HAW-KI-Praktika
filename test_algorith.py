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

    initalBoard = Board([])

    heuristic_bL = 1
    bL = Board([])
    # bL.g = 1
    # bL.f = 1
    bL.parent = initalBoard
    
    heuristic_bL1 = 0
    bL1 = Board([])
    # bL1.g = 2
    # bL1.f = 0
    bL1.parent = bL

    heuristic_bR = 1
    bR = Board([])
    # bR.g = 1
    # bR.f = 1
    bR.parent = initalBoard

    heuristic_bR1 = 1
    bR1 = Board([])
    # bR1.g = 2
    # bR1.f = 1
    bR1.parent = bR

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
    openList: List[Board] = []
    closedList: List[Board] = []

    # step 1
    openList = [initalBoard]
    mocker.patch('main.getMoves', return_value=([bR, bL], False))

    nodeToExpand = openList.pop()
    assert nodeToExpand == initalBoard
    (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

    # assert
    assert hasWon is False
    assert len(openList) == 2
    assert openList == [bR, bL]

    # step 2
    mocker.patch('main.getMoves', return_value=([bL1], False))

    nodeToExpand = openList.pop()
    assert nodeToExpand == bL
    (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

    # assert
    assert hasWon is False
    assert openList[1].f == 2
    assert len(openList) == 2
    assert openList == [bR, bL1]

    # step 3
    mocker.patch('main.getMoves', return_value=([], False))
    nodeToExpand = openList.pop()
    assert nodeToExpand == bL1
    (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

    # assert
    assert hasWon is False
    assert len(openList) == 1
    assert openList == [bR]

    # step 4
    mocker.patch('main.getMoves', return_value=([bR1], True))
    nodeToExpand = openList.pop()
    assert nodeToExpand == bR
    (hasWon, _) = makeMove(nodeToExpand, openList, closedList)

    # assert
    assert hasWon is True
    assert len(openList) == 0