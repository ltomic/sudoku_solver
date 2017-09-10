import subprocess
import os
import fnmatch

def test(msg):
	print(msg)
	return

def find_file(pattern, path):
	result = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))
	return result

def run_process(DIR, cmdname, infilepath, outfilepath):
	cmd = find_file(cmdname, DIR)[0]
	infile = open(DIR + infilepath, 'r')
	outfile = open(DIR + outfilepath, 'w')
	process = subprocess.Popen(cmd, stdin=infile, stdout=outfile, cwd=DIR)
	process.wait()
	infile.close()
	outfile.close()

def run_solver(DIR, sudokutxt):
	sudokufile = open(DIR + '/sudoku.txt', 'w')
	sudokufile.write(sudokutxt)
	sudokufile.close()
	run_process(DIR, 'sudoku_to_matrix', '/sudoku.txt', '/matrix.txt')
	run_process(DIR, 'dlx', '/matrix.txt', '/log.txt')
	run_process(DIR, 'rows_to_solution', '/rows.txt', '/sol.txt')
	run_process(DIR, 'solution_to_solvedsudoku', '/sol.txt', '/solvedsudoku.txt')
	solvedsudokufile = open(DIR + '/solvedsudoku.txt', 'r')
	solvedsudokutxt = solvedsudokufile.readlines()[0]
	return solvedsudokutxt

#DIR = os.getcwd()
#f = open('sudoku.txt')
#sudoku = f.readlines()[0]
#f.close()
#run_solver(sudoku)
