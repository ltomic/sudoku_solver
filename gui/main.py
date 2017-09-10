from tkinter import *
import io
import subprocess
import sys
import time
import scripts
import os
import random
import shutil

def cell_position(x, y):
	addx = (x//3)*6
	addy = (y//3)*6
	return (x*50+5+addx, y*50+5+addy)

def get_cell_id(x, y):
	if x < 10 or y < 10:
		return (9, 9)
	return (int((y-10)/52), int((x-10)/52))

class Program(Frame):
	def __init__(self, prozor):
		self.prozor = prozor
		self.prozor.title("Zmijica")
		super().__init__(self.prozor)
		self.grid(rows=10, columns=10)
		self.KS()

	def KS(self):
		self.c = Canvas(self, width=472, height=472, bg="black")
		self.button_check_solution = Button(self, 
				text="Check", command=self.check_solution)	
		self.button_new = Button(self, text="New", command=self.new_sudoku, bg='Yellow')
		self.button_solve = Button(self, text="Solve", command=self.solve_sudoku, \
				bg='Yellow')
		self.button_clear = Button(self, text="Clear", command=self.clear_sudoku, \
				bg='Yellow')

		self.c.bind("<Button-1>", self.canvas_click)
		self.prozor.bind("<Key>", self.key_click)


		self.c.grid(row=1, column=1, rowspan=10)
		self.button_check_solution.grid(row=2, column=2)
		self.button_solve.grid(row=3, column=2)
		self.button_new.grid(row=1, column=2)
		self.button_clear.grid(row=4, column=2)
		
		self.DIR = os.getcwd()
		self.load()
		self.create_grid()
		self.new_sudoku()

	def load(self):
		self.cells = list([] for i in range(9))
		self.image_numbers = []
		self.image_locked_numbers = []
		self.image_selected_numbers = []
		self.image_wrong_numbers = []
	
		self.image_blank = PhotoImage(file = 'res/blank.png')
		self.image_selected_blank = PhotoImage(file = 'res/selected_blank.png')
		self.image_wrong_blank = PhotoImage(file='res/wrong_blank.png')

		self.image_numbers.append(self.image_blank)
		for i in range(9):
			self.image_numbers.append(
					PhotoImage(file='res/number{}.png'.format(i+1)))

		for i in range(9):
			self.image_locked_numbers.append(
					PhotoImage(file='res/locked_number{}.png'.format(i+1)))
	
		self.image_selected_numbers.append(self.image_selected_blank)	
		for i in range(9):
			self.image_selected_numbers.append(
					PhotoImage(file='res/selected_number{}.png'.format(i+1)))

		self.image_wrong_numbers.append(self.image_wrong_blank)
		for i in range(9):
			self.image_wrong_numbers.append(
					PhotoImage(file='res/wrong_number{}.png'.format(i+1)))

	def key_click(self, event):
		char = repr(event.char)[1]
		try:
			char = int(char)
		except ValueError:
			return
		
		if self.selected != 0:
			self.c.itemconfig(self.selected[0], 
					image=self.image_selected_numbers[char])
			self.sudokutxt[self.selected[1]][self.selected[2]] = str(char)

	def canvas_click(self, event):
		print("Canvas click")
		items = self.c.find_withtag(CURRENT)
		if len(items) == 0:
			return
		for i in range(9):
			for j in range(9):
				if self.cells[i][j][0] == items[0]:
					items = self.cells[i][j]
		if items:
			self.deselect_cell()
			if self.locked[items[1]][items[2]] == False:
				self.selected = items
				img = 0
				if self.sudokutxt[items[1]][items[2]] == '.':
					img = self.image_selected_blank
				else:
					img = self.image_selected_numbers[int(self.sudokutxt[items[1]][items[2]])]
				self.c.itemconfig(self.selected[0], image=img)

	def deselect_cell(self):
		if self.selected != 0:
			number = int(self.sudokutxt[self.selected[1]][self.selected[2]])
			self.c.itemconfig(self.selected[0], image=self.image_numbers[number])
		self.selected = 0

	def new_sudoku(self):
		sudokufilename = 'res/sudoku{}.txt'.format(random.randint(0, 20))
		sudokufile = open(file = sudokufilename)
		txt = sudokufile.readlines()[0].replace('.', '0')
		sudokufile.close()
		self.sudokutxt = list(list(txt[i:i+9]) for i in range(0, len(txt), 9))
		self.selected = 0
		self.update_sudoku()
	
	def create_grid(self):
		self.c.delete("all")
		for i in range(9):
			for j in range(9):
				posy, posx = cell_position(i, j)
				self.c.create_rectangle(posx, posy, posx+50, posy+50)	
				self.cells[i].append(
						(self.c.create_image(posx+25, posy+25, image=self.image_blank),
						 i, j))

	def clear_sudoku(self):
		for i in range(9):
			for j in range(9):
				self.sudokutxt[i][j] = '0'
		self.update_sudoku()

	def update_sudoku(self):
		self.locked = [list() for i in range(9)]
		for i in range(9):
			for j in range(9):
				self.locked[i].append(self.sudokutxt[i][j] != '0')
	
		print(self.sudokutxt)	
		for i in range(9):
			for j in range(9):
				t = self.sudokutxt[i][j]
				img = 0
				if t != '0':
					img = self.image_locked_numbers[int(t)-1]
				else:
					img = self.image_blank		
				self.c.itemconfig(self.cells[i][j][0], image=img)
		return


	def check_empty_cells(self, wrong):
		print("Check Empty")
		for i in range(9):
			for j in range(9):
				if self.sudokutxt[i][j] == '0':
					wrong[i][j] = True
		return wrong

	def check_repeating_numbers_in_row_column_region(self, wrong):
		print("Check Repeating")
		for i in range(9):
			for j in range(9):
				for k in range(j+1, 9):
					if self.sudokutxt[i][j] == self.sudokutxt[i][k] and \
																	 self.sudokutxt[i][j] != '0':
						wrong[i][j] = True
						wrong[i][k] = True
					if self.sudokutxt[j][i] == self.sudokutxt[k][i] and \
																	 self.sudokutxt[j][i] != '0':
						wrong[j][i] = True
						wrong[k][i] = True

		for i in range(9):
			for j in range(9):
				for k in range(j+1, 9):
					a = ((i//3)*3+j//3, (i%3)*3+j%3)
					b = ((i//3)*3+k//3, (i%3)*3+k%3)
					if self.sudokutxt[a[0]][a[1]] == '0':
						continue
					if self.sudokutxt[a[0]][a[1]] == self.sudokutxt[b[0]][b[1]]:
						wrong[a[0]][a[1]] = True
						wrong[b[0]][b[1]] = True
		return wrong

	def check_written(self, wrong):
		for i in range(9):
			for j in range(9):
				if self.sudokutxt[i][j] != '0':
					wrong[i][j] = True
		return wrong

	def check_solution(self, empty=True, repeating=True, written=False):
		self.deselect_cell()
		wrong = list(list(False for j in range(9)) for i in range(9))
		if empty == True:
			wrong = self.check_empty_cells(wrong)
		if repeating == True:
			wrong = self.check_repeating_numbers_in_row_column_region(wrong)
		if written == True:
			wrong = self.check_written(wrong)
		self.mark_wrong(wrong)
		return

	def mark_wrong(self, wrong):
		for i in range(9):
			for j in range(9):
				if wrong[i][j] == True and self.locked[i][j] == False:
					img = self.image_wrong_numbers[int(self.sudokutxt[i][j])]
					self.c.itemconfig(self.cells[i][j][0], image=img)

	def mark_written_wrong(self):
		self.check_solution(empty=False, repeating=False, written=True)

	def solve_sudoku(self):
		self.deselect_cell()
		txt = ''
		for i in self.sudokutxt:
			for j in i:
				txt += j
		print(txt)
		print(os.path.dirname(self.DIR))
		solvedsudokutxt = scripts.run_solver(os.path.dirname(self.DIR), txt)
		print(solvedsudokutxt)
		if '0' in solvedsudokutxt:
			self.mark_written_wrong()
			return
		for i in range(len(solvedsudokutxt)):
			self.sudokutxt[i//9][i%9] = solvedsudokutxt[i]
		self.update_sudoku() 
		return

p = Program(Tk())
mainloop()
