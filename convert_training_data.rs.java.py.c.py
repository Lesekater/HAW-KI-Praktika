import json
import os
from os import listdir
from os.path import isfile, join
import heuristics
from heuristics import heurisitcTypes
from const import Board, EPiece
import uuid

# The Path is modeled after what mcgs.py generates.
# substitue path_specific for each subfolder.
# This is not a problem, as it is fast to generate the data.
training_path_base = "./training_data/"
path_specific = "2025-01-09-8/"


training_path = training_path_base + path_specific

new_path_base = "./new_training_data/"
new_path = new_path_base + path_specific


onlyfiles = [f for f in listdir(training_path) if isfile(join(training_path, f))]


heuristics_to_use = [
    heurisitcTypes.CountOfPieces,
    heurisitcTypes.CountOfDames,
    heurisitcTypes.CountOfPiecesAndDames,
    heurisitcTypes.CountOfPiecesAtEndOfBoard,
    heurisitcTypes.ProgressPiecesOnBoard,
    heurisitcTypes.CountOfPiecesOfOtherPlayer,
    heurisitcTypes.CountOfDamesOfOtherPlayer,
    heurisitcTypes.CountOfPiecesAndDamesOfOtherPlayer,
]

for heuristic in heuristics_to_use:
    path_for_heuristic = new_path + heuristic.name + "/"
    if not os.path.isdir(path_for_heuristic):
        os.makedirs(path_for_heuristic)

def save_scores_for_board(board: Board):
    for heuristic in heuristics_to_use:
        calculated_heuristic = heuristics.calculateHeuristic(board, heuristic)

        path_for_heuristic = new_path + heuristic.name + "/"
        filename = f"{path_for_heuristic}{uuid.uuid4()}.json"
        with open(filename, "w") as f:
            json.dump({"move": board.toIntList(), "score": calculated_heuristic}, f)


for file in onlyfiles:
    with open(training_path+file) as f:
        content = json.load(f)
        move = content["move"]
        board = Board.fromIntList(move)
        save_scores_for_board(board)