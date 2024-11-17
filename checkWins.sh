#!/bin/bash

player1_wins=0
player2_wins=0

# Default number of iterations
iterations=${1:-100}

trap "echo 'Script interrupted. Exiting...'; exit 1" SIGINT

for heuristic in {0..9}; do
    if [ "$heuristic" -eq 3 ] || [ "$heuristic" -eq 6 ]; then
        continue
    fi
    player1_wins=0
    player2_wins=0
    for i in $(seq 1 $iterations); do
        python3.10 main.py 4 $heuristic 10
        if [ ! -f /home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/stats.txt ]; then
            echo "stats.txt not found!"
            exit 1
        fi
        winner=$(head -n 1 /home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/stats.txt)
        echo "Iteration $i, Heuristic $heuristic, Winner: $winner"
        if [ "$winner" == "Winner: Player 1" ]; then
            ((player1_wins++))
        elif [ "$winner" == "Winner: Player 2" ]; then
            ((player2_wins++))
        fi
    done
    wait
    echo "heuristic: $heuristic against: 10: result player1: $player1_wins result player2: $player2_wins" >> results.txt
done
