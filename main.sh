#!bin/bash

./sudoku_to_matrix < sudoku.txt > matrix.txt
./dlx < matrix.txt > log.txt
./rows_to_solution < rows.txt > sol.txt
./solution_to_solvedsudoku < sol.txt > solvedsudoku.txt
