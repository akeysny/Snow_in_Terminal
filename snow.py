import curses
import random
import time


def max_dimensions(window):
	height, width = window.getmaxyx()
	return height - 2, width



def create_snowflake(window):
	width = max_dimensions(window)[1]
	char = random.choice(['*', '+', '.'])
	column = random.randrange(0, width)
	return 0, column, char

def move_snowflakes(prev, window):
	new = {}
	for (row, column), char in prev.items():
		height, _ = max_dimensions(window)
		new_row = row + 1
		if new_row > height or prev.get((new_row, column)):
			new_row -= 1
		new[(new_row, column)] = char
	return new

def draw_snowflakes(snowflakes, window):
	for (row, column), char in snowflakes.items():
		height, width = max_dimensions(window)
		if row > height or column > width:
			continue
		window.addch(row, column, char)

def draw_moon(window):
	moon = [
		' **    ',
		'  ***  ',
		'   *** ',
		'   *** ',
		'  *** ',
		' **  ',
	]
	start_column = max_dimensions(window)[1] - 10
	window.attrset(curses.color_pair(1))
	for row, line in enumerate(moon, start=1):
		for column, sym in enumerate(line, start=start_column):
			window.addch(row, column, sym)
	window.attrset(curses.color_pair(0))


def main(window):
	curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
	curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
	curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
	curses.init_pair(1, curses.COLOR_YELLOW, 0)
	curses.curs_set(0)
	snowflakes = {}
	while True:
		window.clear()
		draw_moon(window)
		snowflakes = move_snowflakes(snowflakes, window)
		snowflake = create_snowflake(window)
		snowflakes[(snowflake[0], snowflake[1])] = snowflake[2]
		draw_snowflakes(snowflakes, window)
		window.refresh()
		time.sleep(0.1)

if __name__=='__main__':
	curses.wrapper(main)
