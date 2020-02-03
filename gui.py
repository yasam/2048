#!/usr/bin/python3

import argparse
from appJar import gui
from tkinter import messagebox

from gm2048 import *


def rightKey(key):
	game.right_key()

def leftKey(key):
	game.left_key()

def upKey(key):
	game.up_key()

def downKey(key):
	game.down_key()

class GameGui(GM2048):
	def __init__(self, size):
		self.app = None
		return GM2048.__init__(self, size)

	def get_cell_name(self, row, col):
		return str(row).zfill(2) + "-" + str(col).zfill(2)

	def message(self, msg):
		messagebox.showinfo("2048", msg)

	def update_cell(self, row, col):
		if self.app == None:
			return
		fgcolors = ["","green", "yellow", "blue", "purple", "navy", "orange", "maroon", "red", "green", "yellow", "blue", "purple", "navy", "orange", "maroon", "red"]
		cell = self.get_cell(row, col)

		# default state is closed
		bgcolor = "DarkGrey"
		relief = "raised"
		val = cell.value()

		bgcolor = "LightGrey"
		relief = "sunken"

		l = self.get_cell_name(row, col)
		lbl = self.app.getLabelWidget(l)

		fgcolor = fgcolors[cell.get_color_idx()]
		if fgcolor != "":
			self.app.setLabelFg(l, fgcolor)

		self.app.setLabelBg(l, bgcolor)
		lbl.config(relief=relief)
		if val == 0:
			lbl.config(text = "")
		else:
			lbl.config(text = str(val))

		self.app.setTitle(str(self.get_points()))

	def verbose(self, enable):
		self.draw_board(enable)

	def finalize_event(self):
                if self.is_moved():
                        self.put_new_value()

                if self.check_over() == True:
                        self.message("You won!!!")
                        self.app.stop()

	def left_key(self):
		self.move_left()
		self.finalize_event()

	def right_key(self):
		self.move_right()
		self.finalize_event()

	def up_key(self):
		self.move_up()
		self.finalize_event()


	def down_key(self):
		self.move_down()
		self.finalize_event()

	def create_board(self):
		#create the cells
		for i in range(self.row_count):
			for j in range(self.col_count):
				l = self.get_cell_name(i, j)
				lbl = self.app.addLabel(l, " ", i, j)
				self.app.setLabelBg(l, "DarkGrey")
				self.app.setLabelWidth(l, 40)
				self.app.setLabelHeight(l, 40)

				lbl.config(borderwidth=2, relief="raised")
				lbl.row = i
				lbl.col = j


	def draw_board(self, is_real = False):
		for i in range(self.row_count):
			for j in range(self.col_count):
				self.update_cell(i, j)
	def play(self):
		width = (self.col_count) * 40
		height = (self.row_count) * 40
		self.app = gui("2048 by yasam", str(width)+"x"+str(height), handleArgs=False)
		self.app.setSticky("news")
		self.app.setExpand("both")
		self.app.bindKey('<Left>', leftKey)
		self.app.bindKey('<Right>', rightKey)
		self.app.bindKey('<Up>', upKey)
		self.app.bindKey('<Down>', downKey)
		self.create_board()
		self.draw_board()
		self.app.go()

def main():
	global game
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-s", "--size", help="size", type=int, default=4)

	args = argparser.parse_args()

	game = GameGui(args.size)
	game.play()

if __name__ == "__main__":
	main()

