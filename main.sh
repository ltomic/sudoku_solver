#!bin/bash

mkdir -p tmp

./bin/sudoku_to_matrix < tmp/sudoku.txt > tmp/matrix.txt
./bin/dlx < tmp/matrix.txt > tmp/log.txt
./bin/rows_to_solution < tmp/rows.txt > tmp/sol.txt
./bin/solution_to_solvedsudoku < tmp/sol.txt > tmp/solvedsudoku.txt
