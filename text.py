#!/usr/bin/python3

import sys
import random
import json
import argparse

from gm2048 import *
import sys, tty, termios

def getch(char_width=1):
        '''get a fixed number of typed characters from the terminal.
        Linux / Mac only'''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(fd)
                ch = sys.stdin.read(3)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

ACTION_UP 	= 'U'
ACTION_DOWN 	= 'D'
ACTION_LEFT 	= 'L'
ACTION_RIGHT 	= 'R'
ACTION_EXIT 	= 'E'


class GameText(GM2048):
	def __init__(self, size):
		return GM2048.__init__(self, size)

	def message(self, msg):
		print(msg)


	def update_cell(self, row, col, is_real=False):
		#do nothing in text mode
		return


	def print_board(self):
		# default, "green", "yellow", "blue", "magenta", "cyan", "light red", "light magenta", "red", "dark gray"
		colors = ['\033[39m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\33[36m', '\033[91m', '\033[95m' , '\033[31m']
		bgnormal = '\033[49m'
		bgclosed = '\033[100m'
		bgopen = '\033[47m'

		print("Points:"+str(self.get_points()))

		for i in range(self.row_count):
			row = ""
			for j in range(self.col_count):
				cell = self.get_cell(i, j)
				val = cell.value()
				color_idx = cell.get_color_idx()
				# default is closed
				color = colors[color_idx]
				bgcolor = bgopen
				v = str(val)
				if val == 0:
                                        v = "."
				row += bgcolor+color + " " + "{:^5}".format(v) + " " + colors[0] + bgnormal

			print(row)

	def read_action_arrows(self):
                while True:
                	print("Use arrows(<ESC><ESC><ESC> to exit):")
                	keycode = getch()
                	if keycode == '\x1b[A':
                                return ACTION_UP
                	if keycode == '\x1b[B':
                                return ACTION_DOWN
                	if keycode == '\x1b[C':
                                return ACTION_RIGHT
                	if keycode == '\x1b[D':
                                return ACTION_LEFT
                	if keycode == '\x1b\x1b\x1b':
                                return ACTION_EXIT
                	print("Invalid keycode:"+keycode)

	def read_action(self):
		actions = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_EXIT]
		while True:
			action = input("Use Arrows:")
			if len(action) <= 0:
				continue

			if action[0] in actions :
				return action[0]
			self.message("Invalid action:"+action)

	def play(self):
		while True:
			self.print_board()
			action = self.read_action_arrows();

			if action == ACTION_UP:
                                self.move_up()
			elif action == ACTION_DOWN:
                                self.move_down()
			elif action == ACTION_LEFT:
				self.move_left()
			elif action == ACTION_RIGHT:
				self.move_right()
			elif action == ACTION_EXIT:
				break
			else:
				self.message("Unknown action:"+action)

			if self.check_over() == True:
                                self.message("Game Over, total points:"+str(self.get_points()))
                                break

		self.print_board()


def main():
	global game
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-s", "--size", help="size of the boards", type=int, default=4)

	args = argparser.parse_args()

	game = GameText(args.size)
	game.play()

if __name__ == "__main__":
	main()

