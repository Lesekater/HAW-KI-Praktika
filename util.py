from const import Board

def formatBoard(board: Board) -> str:
    formattedBoard = ""
    for row in board.data:
        formattedBoard += str(row) + "\n"
    return formattedBoard