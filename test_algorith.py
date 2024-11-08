from const import Board
from main import main, countOfPieces
import copy

# Player1 is odd  numbers (1 and 3) (Black)
# Player2 is even numbers (2 and 4) (White)

# Player1 moves in positive direction (down)
# Player2 moves in negative direction (up)
board = Board([
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
