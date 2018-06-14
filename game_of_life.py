
import curses
import curses.ascii
import time
import random

# User selectable live / dead cell symbols
live = 'O'
dead = '.'

# global screen size of cell universe
height=10
width=40

universe = [[0 for y in range(width)] for x in range(height)]
next_universe = [[0 for y in range(width)] for x in range(height)]

def main(stdscr):

    global live, dead

    curses.cbreak()
    curses.noecho()

    stdscr.addstr(0, 0, '---------------------------')
    stdscr.addstr(1, 0, '       Game of life')
    stdscr.addstr(2, 0, '---------------------------')

    # Users may define the live and dead cells
    get_symbol(stdscr, 'live', 3)

    get_symbol(stdscr, 'dead', 5)

    init_universe()

    # Users may pick a number of seeds or their own
    get_seeds(stdscr)

    stdscr.refresh()
    time.sleep(1)

    # GOL is displayed on the terminal
    while True:
        stdscr.clear()
        show_universe(stdscr)

        key = stdscr.getch()
        if (chr(key) == 'x'):
            exit()

    # GOL goes on

def get_manual_seeds(stdscr):

    global height, width
    show_universe(stdscr)

    stdscr.addstr(height + 2, 0, 'Use keyboard to move.  Enter s to place a seed. Enter q to exit. ')
    stdscr.addstr(height + 3, 0, 'a / d for left / right, w / x for up / down.')

    x = 0
    y = 0

    key = ''

    while key != 'q':
        key = chr(stdscr.getch())

        if key == 'q': # Finish
            clear_display(stdscr)
            return

        elif key == 'a': # Left
            if x == 0:
                x = width - 1
            else:
                x = x - 1

        elif key == 'd': # Right
            if x >= width-1:
                x = 0
            else:
                x = x + 1

        elif key == 'w': # Up
            if y == 0:
                y = height - 1
            else:
                y = y - 1

        elif key == 'x': # Down
            if y >= height-1:
                y = 0
            else:
                y = y + 1

        # curses.setsyx(y, x)

        if key == 's': # Place Seed
            stdscr.addstr(y, x, live)
            stdscr.addstr(y, x, '')     # Moves back the cursor after write
            universe[y][x] = live

        else:
            stdscr.addstr(y, x, '')

        stdscr.refresh()


def get_seeds(stdscr):

    stdscr.addstr(7, 0, 'How many seeds would you like to randomly place?')
    stdscr.addstr(8, 0, 'Enter a number between 1 and 9 or 0 for manual placement: ')

    seeds = stdscr.getch()

    clear_display(stdscr)

    if curses.ascii.isdigit(seeds):
        stdscr.refresh()

    if seeds >= 49 and seeds <= 57:
        stdscr.addstr(9, 0, 'Randomly placing {} seeds'.format(seeds-48))
        random_seeds(seeds-48)

    elif seeds == 48:
        stdscr.addstr(9, 0, 'Manual input selected')
        get_manual_seeds(stdscr)

    else:
        stdscr.addstr(9, 0, 'Sorry, wrong input')
        exit()

    clear_display(stdscr)

def clear_display(stdscr):
    height, width = stdscr.getmaxyx()

    blankline = ' ' * (width-1)

    for line in range(height):
        stdscr.addstr(line, 0, blankline)


def init_universe():
    for i in range(height):
        for j in range(width):
            universe[i][j] = dead


def random_seeds(seeds):
    for seed in range(seeds):
        rand_y = random.randint(0, height-1)
        rand_x = random.randint(0, width-1)

        while (universe[rand_y][rand_x] != dead):
            rand_y = random.randint(0, height-1)
            rand_x = random.randint(0, width-1)

        universe[rand_y][rand_x] = live


def show_universe(stdscr):
    for i in range(height):
        for j in range(width):
            stdscr.addstr(i, j, universe[i][j])


def get_symbol(stdscr, target, y):

    global dead, live

    stdscr.addstr(y, 0, 'Enter a symbol for a {} cell: '.format(target))
    c = stdscr.getch()

    if curses.ascii.isalnum(c):
        stdscr.addstr(y+1, 0, chr(c))
        if target == 'live':
            live = chr(c)
        elif target == 'dead':
            dead = chr(c)


if __name__ == '__main__':
    curses.wrapper(main)