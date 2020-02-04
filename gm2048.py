#!/usr/bin/python3

import sys
import random
import copy
import math

class Cell:
	def __init__(self):
                self._value = 0
                self._combined = False
                self._color_idx = 0;

	def add(self, v):
                self._value += v
                self._combined = True
                self._color_idx += 1

	def set(self, v):
                self._color_idx = math.log(v, 2)
                self._value = v

	def clear(self):
                self._value = 0
                self._combined = False
                self._color_idx = 0

	def value(self):
                return self._value

	def is_combined(self):
                return self._combined

	def clear_combined(self):
                self._combined = False

	def get_color_idx(self):
                return int(self._color_idx)

class GM2048:
	def __init__(self, size):
		self._is_moved = False
		self.row_count = size
		self.col_count = size
		self.val_count = 0
		self.init_board()
		self._points = 0

	def init_board(self):
		self.board = []
		row = []
		for i in range(self.col_count):
			row.append(Cell())

		for i in range(self.row_count):
			self.board.append(copy.deepcopy(row))

		self.put_new_value()
		self.put_new_value()

	def get_points(self):
                return self._points

	def debug(self, s):
		self.message(s)

	def is_moved(self):
                return self._is_moved

	def clear_moved(self):
		self._is_moved = False

	def get_cell(self, row, col):
		if row < 0 or row >= self.row_count :
			return None

		if col < 0 or col >= self.col_count :
			return None

		return self.board[row][col]

	def clear_combined(self):
                for i in range(0, self.row_count):
                        for j in range(0, self.col_count):
                                self.board[i][j].clear_combined()
                                
	def generate_value(self):
                if random.randint(0, 3) == 0:
                        return 4
                return 2

	def get_empty_cell(self):
                if self.val_count == self.row_count * self.col_count:
                        return [None, 0, 0]
                
                while True:
                        row = random.randint(0, self.row_count-1)
                        col = random.randint(0, self.col_count-1)
                        if self.board[row][col].value() == 0:
                                return [self.board[row][col], row, col]
                        
	def swap(self, row1, col1, row2, col2):
                a = self.get_cell(row1, col1)
                b = self.get_cell(row2, col2)

                if a == None:
                        return
                
                if b == None:
                        return

                self.board[row1][col1] = b
                self.board[row2][col2] = a

	def put_new_value(self, value = 0):
                [c, row, col] = self.get_empty_cell()
                if c == None:
                        self.message("Game over!")
                        return False
                
                if value == 0:
                        value = self.generate_value()
                c.set(value)
                self.val_count += 1
                self.update_cell(row, col)
                return True

	def get_prev_idx(self, idx, is_forward):
                if is_forward:
                        return idx - 1

                return idx + 1
        
	def get_next_idx(self, idx, is_forward):
                if is_forward:
                        return idx + 1

                return idx - 1

	def shift(self, row, col, is_vertical, is_forward):
                #self.debug("iter_column_updown:row="+str(idx)+", caol="+str(col))
                row_prev_idx = row
                row_next_idx = row
                col_prev_idx = col
                col_next_idx = col

                if is_vertical:
                        row_prev_idx = self.get_prev_idx(row, is_forward)
                        row_next_idx = self.get_next_idx(row, is_forward)
                else:
                        col_prev_idx = self.get_prev_idx(col, is_forward)
                        col_next_idx = self.get_next_idx(col, is_forward)
                
                prev = self.get_cell(row_prev_idx, col_prev_idx)
                cur = self.get_cell(row, col)

                if prev == None:
                        if cur != None:
                                self.shift(row_next_idx, col_next_idx, is_vertical, is_forward)
                        return

                if cur == None:
                        return

                if cur.value() == 0:
                        self.shift(row_next_idx, col_next_idx, is_vertical, is_forward)
                        return

                if prev.value() == 0:
                        self._is_moved = True
                        #self.debug("swap (" + str(row_prev_idx) + ", " + str(col_prev_idx) + ":"+str(prev.value())+") <--> (" + str(row) + ", " + str(col) + ":"+str(cur.value())+")")
                        self.swap(row_prev_idx, col_prev_idx, row, col)
                        self.update_cell(row_prev_idx, col_prev_idx)
                        self.update_cell(row, col)
                        self.shift(row_prev_idx, col_prev_idx, is_vertical, is_forward)
                        return

                if prev.is_combined():
                        self.shift(row_next_idx, col_next_idx, is_vertical, is_forward)
                        return
                
                if prev.value() == cur.value():
                        self._is_moved = True
                        self._points += cur.value()
                        prev.add(cur.value())
                        cur.clear()
                        self.update_cell(row_prev_idx, col_prev_idx)
                        self.update_cell(row, col)
                        self.val_count -= 1
                
                self.shift(row_next_idx, col_next_idx, is_vertical, is_forward)
                
	def move_up(self):
                self.clear_combined()
                self._is_moved = False
                for i in range(0, self.col_count):
                        self.shift(0, i, True, True)

	def move_down(self):
                self.clear_combined()
                self._is_moved = False
                for i in range(0, self.col_count):
                        self.shift(self.row_count-1, i, True, False)

	def move_left(self):
                self.clear_combined()
                self._is_moved = False
                for i in range(0, self.col_count):
                        self.shift(i, 0, False, True)

        
	def move_right(self):
                self.clear_combined()
                self._is_moved = False
                for i in range(0, self.col_count):
                        self.shift(i, self.col_count-1, False, False)


	def check_over(self):
                if self.get_empty_cell() == None:
                        return True
                return False

	def message(self, msg):
		raise NotImplementedError("Subclass must implement abstract method!!!")

	def update_cell(self, row, col):
		raise NotImplementedError("Subclass must implement abstract method!!!")


