from const import Board
from heuristics import heurisitcTypes

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

def formatBoard(board: Board, additionalInfo: bool = False, heuristic: heurisitcTypes = None) -> str:
    formattedBoard = ""
    for (i, row) in enumerate(board.data):
        for piece in row:
            formattedBoard += convertPiecesToEmoji(piece.value)
        if additionalInfo and i == 0:
            formattedBoard += " " + additionalInfoRowOne(not board.player1, heuristic)
        formattedBoard += "\n"
    return formattedBoard

def additionalInfoRowOne(player1, heuristic: heurisitcTypes = None) -> str:
    if player1:
        return "Player 1 (⚫, 🔴" + ((", " + heuristic.name + ")") if heuristic != None else ")")
    else:
        return "Player 2 (⚪, 🔵" + ((", " + heuristic.name + ")") if heuristic != None else ")")

def formatBoardWithCoords(board: Board) -> str:
    formattedBoard = ""
    for i, row in enumerate(board.data):
        formattedBoard += f"{i} "
        for piece in row:
            formattedBoard += convertPiecesToEmoji(piece.value)
        formattedBoard += "\n"
    formattedBoard += "  0 1 2 3 4 5 6 7\n"
    return formattedBoard