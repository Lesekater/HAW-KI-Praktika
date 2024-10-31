from const import Board
from main import main
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
    mocker.patch('main.openList', [board])
    mocker.patch('main.getMoves', return_value=(board, True))

    (foundGoal, openList, closedList) = main()

    # assert
    assert len(openList) == 0
    assert len(closedList) == 0
    assert foundGoal is True

def test_noGoalFound(mocker):
    mocker.patch('main.openList', [board])
    mocker.patch('main.getMoves', return_value=([], False))

    (foundGoal, openList, closedList) = main()

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

    mocker.patch('main.openList', openListMock)
    mocker.patch('main.getMoves', return_value=([], True))

    (foundGoal, openList, closedList) = main()

    # assert
    assert len(openList) == 2
    assert openList[0].f == 2
    assert openList[1].f == 1
