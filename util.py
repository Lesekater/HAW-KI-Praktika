from const import Board

def convertPiecesToEmoji(piece: int) -> str:
    if piece == 0:
        return "🏻"
    if piece == 1:
        return "⚫"
    if piece == 2:
        return "⚪"
    if piece == 3:
        return "🔴"
    if piece == 4:
        return "🔵"
    return "❔"

def formatBoard(board: Board) -> str:
    formattedBoard = ""
    for row in board.data:
        for piece in row:
            formattedBoard += convertPiecesToEmoji(piece.value)
        formattedBoard += "\n"
    return formattedBoard

def formatBoardWithCoords(board: Board) -> str:
    formattedBoard = ""
    for i, row in enumerate(board.data):
        formattedBoard += f"{i} "
        for piece in row:
            formattedBoard += convertPiecesToEmoji(piece.value)
        formattedBoard += "\n"
    formattedBoard += "  0 1 2 3 4 5 6 7\n"
    return formattedBoard