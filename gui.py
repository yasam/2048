#!/usr/bin/python3

import argparse
from appJar import gui
from tkinter import messagebox

from gm2048 import *

def mouse_left_click( event ):
	game.mouse_left_click(event)

def mouse_right_click( event ):
	game.mouse_right_click(event)

def verbose_left_click( event ):
	game.verbose(True)

def verbose_right_click( event ):
	game.verbose(False)

class GameGui(MineSweeper):
	def __init__(self, size):
		return GM2048.__init__(self, size)

	def get_cell_name(self, row, col):
		return str(row).zfill(2) + "-" + str(col).zfill(2)

	def message(self, msg):
		messagebox.showinfo("2048", msg)

	def update_cell(self, row, col):
		fgcolors = ["","green", "yellow", "blue", "purple", "navy", "orange", "maroon", "red"]
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
		lbl.config(text = str(val))

	def verbose(self, enable):
		self.draw_board(enable)

	def finalize_event(self):
                if self.is_moved():
                        self.put_new_value()

                if self.check_over() == True:
                        self.message("You won!!!")
                        self.app.stop()

	def mouse_left_click(self, event):
		self.move_up()
		self.finalize_event()


	def mouse_right_click(self, event):
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
				lbl.bind( "<Button-1>", mouse_left_click )
				lbl.bind( "<Button-3>", mouse_right_click )
				lbl.row = i
				lbl.col = j


	def draw_board(self, is_real = False):
		self.update_count()
		for i in range(self.row_count):
			for j in range(self.col_count):
				self.update_cell(i, j)
	def play(self):
		width = (self.col_count + 4) * 40
		height = (self.row_count) * 40
		self.app = gui("2048 by yasam", str(width)+"x"+str(height), handleArgs=False)
		self.app.setSticky("news")
		self.app.setExpand("both")
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

