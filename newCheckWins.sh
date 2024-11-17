#!/bin/bash

player1_wins=0
player2_wins=0

# Default number of iterations
iterations=${1:-100}

trap "echo 'Script interrupted. Exiting...'; exit 1" SIGINT

# Make the parent directory for storing custom stats files
mkdir -p /home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/stats_custom

# Function to run each iteration in parallel
run_iteration() {
    local heuristic=$1
    local iteration=$2
    local iteration_dir="/home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/iteration_${heuristic}_${iteration}"
    
    # Create a new directory for the iteration
    mkdir -p $iteration_dir
    
    # Run the main.py script in the new directory and wait for it to generate stats.txt
    (cd $iteration_dir && python3.10 /home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/main.py 4 $heuristic 10)
}

# Function to parse results after all iterations are complete
parse_results() {
    local heuristic=$1
    player1_wins=0
    player2_wins=0
    
    # Loop through each iteration's directory and read the stats.txt file
    for i in $(seq 1 $iterations); do
        local iteration_dir="/home/elias/Coding/training/Studium/KI/HAW-KI-Praktika/iteration_${heuristic}_${i}"
        
        # Check if stats.txt exists
        if [ -f "$iteration_dir/stats.txt" ]; then
            # Read the winner from stats.txt (trim spaces)
            winner=$(head -n 1 "$iteration_dir/stats.txt" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            echo "Iteration $i, Heuristic $heuristic, Winner: $winner"
            
            # Increment win counters based on winner
            if [ "$winner" == "Winner: Player 1" ]; then
                ((player1_wins++))
            elif [ "$winner" == "Winner: Player 2" ]; then
                ((player2_wins++))
            fi
        else
            echo "Error: stats.txt not found in $iteration_dir"
        fi
        
        # Clean up by removing the iteration directory after parsing
        rm -rf "$iteration_dir"
    done
    
    # Store the results for the current heuristic
    echo "Heuristic $heuristic against: 10 | Player 1 wins: $player1_wins, Player 2 wins: $player2_wins" >> results.txt
}

# Main loop for running and parsing results
for heuristic in {10..10}; do
    if [ "$heuristic" -eq 3 ] || [ "$heuristic" -eq 6 ]; then
        continue
    fi

    # Run all iterations in parallel for the current heuristic
    for i in $(seq 1 $iterations); do
        run_iteration $heuristic $i &
    done
    
    # Wait for all parallel tasks to finish
    wait
    
    # Parse results after all iterations have completed
    parse_results $heuristic
done

