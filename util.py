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